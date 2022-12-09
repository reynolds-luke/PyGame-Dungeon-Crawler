import pygame
from helpers import *
from settings import *
from tile import *


class World:
    def __init__(self, game):
        self.game = game
        self.map = create_starting_room(dim=STARTING_ROOM_DIM)  # Of format (tile_x, tile_y): tile_type
        self.generated_tiles = {pos: False for pos in self.map}  # Of format (tile_x, tile-y): is_already_created

    def add_tiles(self):
        for pos in [pos for pos in self.generated_tiles.keys() if self.generated_tiles[pos] == False]:
            Tile(pos=pos, game=self.game)

    def recalculate_tiles(self):
        for sprite in iter(self.game.background_sprites):
            sprite.refresh_tile()

    def create_room(self):
        self.game.enemies_remaining = -1
        self.game.difficulty += 1

        playerx = self.game.player.rect.centerx // TILE_DIM[0]
        playery = self.game.player.rect.centery // TILE_DIM[1]
        distance = 0
        while True:
            distance += 1
            if self.map.get((playerx + distance, playery)) is None:
                direction = pygame.math.Vector2(1, 0)
                break
            if self.map.get((playerx - distance, playery)) is None:
                direction = pygame.math.Vector2(-1, 0)
                break
            if self.map.get((playerx, playery + distance)) is None:
                direction = pygame.math.Vector2(0, 1)
                break
            if self.map.get((playerx, playery - distance)) is None:
                direction = pygame.math.Vector2(0, -1)
                break

        new_room = generate_room()
        new_room = {(posx + playerx, posy + playery): new_room[(posx, posy)] for posx, posy in new_room}
        new_hallway = dict()
        d = 0

        while 0 != len([coordinate for coordinate in self.map.keys() if coordinate in new_room.keys()]):
            d += 1
            new_hallway[(playerx + d * direction.x, playery + d * direction.y)] = "new_path"
            new_hallway[(playerx + d * direction.x + direction.y, playery + direction.x + d * direction.y)] = "wall"
            new_hallway[(playerx + d * direction.x - direction.y, playery + d * direction.y - direction.x)] = "wall"

            new_room = {(posx + direction.x, posy + direction.y): new_room[(posx, posy)] for posx, posy in new_room}

        extra_hallway_length = 3 * random.randint(2, 5)
        for i in range(extra_hallway_length):
            d += 1
            new_hallway[(playerx + d * direction.x, playery + d * direction.y)] = "new_path"
            new_hallway[(playerx + d * direction.x + direction.y, playery + direction.x + d * direction.y)] = "wall"
            new_hallway[(playerx + d * direction.x - direction.y, playery + d * direction.y - direction.x)] = "wall"

            new_room = {(posx + direction.x, posy + direction.y): new_room[(posx, posy)] for posx, posy in new_room}

        world_update = dict()
        world_update.update({pos: "wall" for pos in new_hallway if new_hallway[pos] == "wall"})
        world_update.update({pos: "wall" for pos in self.map if self.map[pos] == "wall"})
        world_update.update({pos: "floor" for pos in self.map if self.map[pos] == "floor"})
        world_update.update({pos: "wall" for pos in new_room if new_room[pos] == "wall"})

        world_update.update({pos: "floor" for pos in self.map if self.map[pos] == "new_floor"})
        world_update.update({pos: "floor" for pos in self.map if self.map[pos] == "activation"})
        world_update.update({pos: "floor" for pos in self.map if self.map[pos] == "gate"})
        world_update.update({pos: "new_path" for pos in new_hallway if new_hallway[pos] == "new_path"})
        world_update.update({pos: "new_floor" for pos in new_room if new_room[pos] == "new_floor"})
        world_update.update({pos: "activation" for pos in new_room if new_room[pos] == "activation"})

        world_update.update(
            {pos: "gate_deactive" for pos in new_room if
             new_room[pos] == "wall" and new_hallway.get(pos) == "new_path"})
        self.map.update(world_update)

        world_positions = {pos: False for pos in self.map}
        world_positions.update(self.generated_tiles)
        self.generated_tiles = world_positions
        self.add_tiles()
        self.recalculate_tiles()

    def begin_attack(self):
        world_update = {pos: "gate" for pos in self.map if self.map[pos] == "gate_deactive"}
        world_update.update({pos: "floor" for pos in self.map if self.map[pos] == "new_path"})
        world_update.update({pos: "new_floor" for pos in self.map if self.map[pos] == "activation"})

        self.map.update(world_update)
        self.add_tiles()
        self.recalculate_tiles()