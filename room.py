import pygame
from settings import *
from helpers import *


class StaticTile(pygame.sprite.Sprite):

    def __init__(self, groups, pos, pos_scaled, type, world):
        super().__init__(groups)
        self.pos = pos
        self.pos_scaled = pos_scaled
        self.type = type
        self.world = world

        self.tile_path = "./graphics/tiles/"
        self.image = pygame.image.load(self.tile_path + self.type + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, TILE_DIM)
        self.rect = self.image.get_rect(center=self.pos_scaled)

    def update(self):
        if self.world[self.pos] != self.type:
            self.type = self.world[self.pos]

    def update_type(self):
        self.image = pygame.image.load(self.tile_path + self.type + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, TILE_DIM)
