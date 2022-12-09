import pygame
from settings import *
from helpers import *


class Tile(pygame.sprite.Sprite):

    def __init__(self, pos, game):
        self.game = game
        super().__init__(self.game.background_sprites)
        self.map = self.game.world.map

        self.pos = pos
        self.pos_scaled = (TILE_DIM[0] * self.pos[0], TILE_DIM[1] * self.pos[1])

        self.type = "none"
        self.tile_path = "./graphics/tiles/"
        self.image = pygame.image.load("./graphics/tiles/floor.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, TILE_DIM)
        self.rect = self.image.get_rect(center=self.pos_scaled)
        self.groups = []

    def refresh_tile(self):
        if self.map[self.pos] != self.type:
            self.type = self.map[self.pos]
            self.update_type()

    def update_type(self):
        self.image = pygame.image.load(self.tile_path + self.type + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, TILE_DIM)
        for group in self.groups:
            group.remove(self)

        self.game.background_sprites.add(self)
        self.groups.append(self.game.background_sprites)

        if self.type in OBSTACLE_TILES:
            self.game.foreground_sprites.add(self)
            self.groups.append(self.game.foreground_sprites)
            self.game.obstacle_sprites.add(self)
            self.groups.append(self.game.obstacle_sprites)

        if self.type is "activation":
            self.game.activation_sprites.add(self)
            self.groups.append(self.game.activation_sprites)