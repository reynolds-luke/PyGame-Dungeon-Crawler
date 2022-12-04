import pygame
from settings import *

class Crosshair(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load("./graphics/aim/aim.png")
        self.image = pygame.transform.scale(self.image, CROSS_HAIR_DIM)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()