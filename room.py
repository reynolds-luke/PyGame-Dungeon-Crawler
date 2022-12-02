import pygame
from settings import *
from helpers import *


class StaticTile(pygame.sprite.Sprite):

    def __init__(self, groups, pos, type):
        super().__init__(groups)
        self.pos = pos

        tile_path = "./graphics/tiles/"
        self.image = pygame.image.load(tile_path + type + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, TILE_DIM)
        self.rect = self.image.get_rect(topleft=self.pos)
