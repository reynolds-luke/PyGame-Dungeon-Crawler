import pygame
from settings import *
from helpers import *


class Tile(pygame.sprite.Sprite):
    """
    The Tile sprites are what make up the background map of the gap. The floor, wall, gate, etc. tiles are all objects
    from this class. It has an update method which causes it to check if it's type of tile has changed. If it has, it
    updates its image/groups accordingly.
    """

    def __init__(self, pos, game):
        self.game = game  # We just take in the whole game class, and later access which things we need
        super().__init__(self.game.background_sprites)  # We initialize as a pygame sprite with appropriate groups
        self.map = self.game.world.map  # We need access to the map dictionary, so we can tell what sort of tile to be

        self.pos = pos  # This is our position on the map
        self.pos_scaled = (TILE_DIM[0] * self.pos[0], TILE_DIM[1] * self.pos[1])  # This is our location on the screen

        self.type = "none"  # initially, we have no type
        self.tile_path = TILES_GRAPHICS_PATH  # The file path for the tiles
        self.image = pygame.image.load(TILES_STARTING_GRAPHIC_PATH).convert_alpha()  # We initialize an image
        self.image = pygame.transform.scale(self.image, TILE_DIM)  # We scale the image correctly
        self.rect = self.image.get_rect(center=self.pos_scaled)  # We get a rect, so pygame knows how to draw the image
        self.groups = [self.game.background_sprites]  # We initialize the groups we are in. This may change as we update

    def refresh_tile(self):
        """
        This function is called whenever the map updates. It checks to see if the type of tile associated with this tile
        differs from what the map says should be at its location. If there is a difference, it updates what type it is
        by calling the method update_type
        """
        if self.map[self.pos] != self.type:  # If the type of the tile changed...
            self.type = self.map[self.pos]  # Change the name of our type
            self.update_type()  # Call the update_type method, so we actually change the type of tile displayed

    def update_type(self):
        self.image = pygame.image.load(self.tile_path + self.type + ".png").convert_alpha()  # Load the new image
        self.image = pygame.transform.scale(self.image, TILE_DIM)  # Scale the image appropriately

        # First, we remove the sprite from all groups its in. We will add the ones we need back in soon.
        for group in self.groups:
            group.remove(self)
        self.groups = []  # We also update our memory of what groups we are in

        self.game.background_sprites.add(self)  # We add the sprite back into the "background sprites" group
        self.groups.append(self.game.background_sprites)  # We update our attribute as well

        if self.type in OBSTACLE_TILES:  # If it's an obstacle tile, we add it to the appropriate group
            self.game.foreground_sprites.add(self)  # Adding the sprite to the foreground sprites group
            self.groups.append(self.game.foreground_sprites)  # Updating our attribute

            self.game.obstacle_sprites.add(self)  # Adding the sprite to the obstacle sprites group
            self.groups.append(self.game.obstacle_sprites)  # Updating our attribute

        if self.type is "activation":  # If it's an obstacle tile, we also it to the activation group
            self.game.activation_sprites.add(self)  # Adding the sprite to the activation sprites group
            self.groups.append(self.game.activation_sprites)  # Updating our attribute
