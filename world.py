import pygame, random
from helpers import *
from settings import *
from tile import *


class World:
    """
    This class describes the world, which stores the world map as an attribute. The class also has various methods for
    creating new rooms, updating the room when an attack starts, adding new tile sprites, and recalculating all the
    tile sprites when the map is updated.
    """

    def __init__(self, game):
        self.game = game  # We need to access objects from the game quite a bit, so we just bring in the whole game.
        self.map = create_rect_room(dim=STARTING_ROOM_DIM, wall_name="wall", floor_name="floor")  # Initialized map
        self.generated_tiles = {pos: False for pos in self.map}  # Of format (tile_x, tile-y): is_already_created

    def add_tiles(self):
        """
        This method is called whenever a new room is added. It goes through each of the positions in the generated_tiles
        attribute, and checks to see if there is already a tile at that location. If there isn't a tile there, it makes
        one to fill in the gap.
        :return:
        """
        for pos in [pos for pos in self.generated_tiles.keys() if self.generated_tiles[pos] == False]:
            Tile(pos=pos, game=self.game)

    def recalculate_tiles(self):
        """
        This method is called whenever the world map changes (i.e. when there are new rooms created, or when the attack
        starts and some tiles on the map change.)
        """
        for sprite in iter(self.game.background_sprites):  # For each sprite we created...
            sprite.refresh_tile()  # Tell the sprite to update

    def create_room(self):
        """
        This function is called by the game when a new room needs to be created. It
        """

        direction = pygame.math.Vector2()  # This the direction to create the new room, relative to player

        if random.randint(0, 1):  # Pick either horizontal or vertical
            direction.x = 2 * random.randint(0, 1) - 1  # Random; either 1 or -1
        else:
            direction.y = 2 * random.randint(0, 1) - 1  # Random; either 1 or -1

        # We start creating the path where the player is, so we get the player's current position. We divide by the
        # TILE_DIM so that we get the player's true, unadjusted position.
        playerx = self.game.player.rect.centerx // TILE_DIM[0]
        playery = self.game.player.rect.centery // TILE_DIM[1]

        """
        Below is the code that actually creates the room.
        """

        new_room = generate_room()  # First, we get a zero-centered room. See helpers.py

        # Next, we center the room on the player's location
        new_room = {(posx + playerx, posy + playery): new_room[(posx, posy)] for posx, posy in new_room}
        new_hallway = dict()  # The new hallways is stored separately, as the room will constantly be moving
        d = 0  # This is the distance the room need to move before being in a valid location

        # We then continue to shift the room in the given direction until it doesn't overlap with previous generations
        while 0 != len([coordinate for coordinate in self.map.keys() if coordinate in new_room.keys()]):
            d += 1  # We increase the distance we have travelled, to tell the hallway where to generate

            # The following creates the first part of the hallway, creating a path where the player is and adding walls on
            # either side (either top/bottom or right/left, depending on the direction)
            new_hallway[(playerx + d * direction.x, playery + d * direction.y)] = "new_path"
            new_hallway[(playerx + d * direction.x + direction.y, playery + direction.x + d * direction.y)] = "wall"
            new_hallway[(playerx + d * direction.x - direction.y, playery + d * direction.y - direction.x)] = "wall"

            # Then we shift the room location over one tile in the desired direction
            new_room = {(posx + direction.x, posy + direction.y): new_room[(posx, posy)] for posx, posy in new_room}

        # To make things more interesting, we continue generating the hallway for another random amount
        extra_hallway_length = 3 * random.randint(2, 5)  # The extra length of the hallway
        for i in range(extra_hallway_length):
            d += 1  # We increase the distance we have travelled, to tell the hallway where to generate

            # We then generate a new segment of the hallway, with walls on either side
            new_hallway[(playerx + d * direction.x, playery + d * direction.y)] = "new_path"
            new_hallway[(playerx + d * direction.x + direction.y, playery + direction.x + d * direction.y)] = "wall"
            new_hallway[(playerx + d * direction.x - direction.y, playery + d * direction.y - direction.x)] = "wall"

            # Then we shift the room location over one tile in the desired directio
            new_room = {(posx + direction.x, posy + direction.y): new_room[(posx, posy)] for posx, posy in new_room}

        """
        Next is the code that creates the "world update" that updates the world dictionary. It is created by
        progressively updating itself, in order of what types of tile generation take priority. In general, walls have
        the lowest priority (this prevents passageways from being blocked off), and new_floor/new_path  tiles have top
        priority (they are needed so the player knows which direction to go)
        """

        world_update = dict()  # We initialize the world update to be nothing

        # First, we add all the walls which we created. This also adds some extra walls, but they are updated out later
        world_update.update({pos: "wall" for pos in new_hallway if new_hallway[pos] == "wall"})

        # We want the original world floor tiles to override new hallway walls, so we run the following update
        world_update.update({pos: "floor" for pos in self.map if self.map[pos] == "floor"})
        world_update.update({pos: "wall" for pos in new_room if new_room[pos] == "wall"})

        # Next, we make all of what were previously "new_floor", "gate", or "activation tiles" into regular floor tiles
        world_update.update({pos: "floor" for pos in self.map if self.map[pos] == "new_floor"})
        world_update.update({pos: "floor" for pos in self.map if self.map[pos] == "activation"})
        world_update.update({pos: "floor" for pos in self.map if self.map[pos] == "gate"})

        # Next, we add in all the new paths created as well as the new floor. Also adds the new activation tile.
        world_update.update({pos: "new_path" for pos in new_hallway if new_hallway[pos] == "new_path"})
        world_update.update({pos: "new_floor" for pos in new_room if new_room[pos] == "new_floor"})
        world_update.update({pos: "activation" for pos in new_room if new_room[pos] == "activation"})

        # Lastly, we add a deactive gate at the location where the path and the room intersect. This will close when
        # the enemies start attacking, trapping the player in the room
        world_update.update(
            {pos: "gate_deactive" for pos in new_room if
             new_room[pos] == "wall" and new_hallway.get(pos) == "new_path"})

        self.map.update(world_update)  # We update the map to reflect the changes to the world described above

        world_positions = {pos: False for pos in self.map}  # We initialize an update to what tiles to add
        world_positions.update(self.generated_tiles)  # We update to reflect which tiles have already been added

        self.generated_tiles = world_positions  # We apply our update to the generated_tiles attribute
        self.add_tiles()  # We add the new tiles that need to be added
        self.recalculate_tiles()  # Then, we recalculate each tile.

    def begin_attack(self):
        """
        This method is called when the player touches the activation tile. It closes the gate behind the player, removes
        the activation tile from the map, and removes the path from behind the player.
        """

        # As before, we first create a world update dictionary and then apply it to the actual map.
        world_update = {pos: "gate" for pos in self.map if self.map[pos] == "gate_deactive"}  # activate the gate
        world_update.update({pos: "new_floor" for pos in self.map if self.map[pos] == "activation"})  # kill activation
        world_update.update({pos: "floor" for pos in self.map if self.map[pos] == "new_path"})  # kill old path

        self.map.update(world_update)  # Apply the update to the actual map
        self.add_tiles()  # We add the new tiles that need to be added
        self.recalculate_tiles()  # Then, we recalculate each tile.
