import pygame
from settings import *

class Crosshair(pygame.sprite.Sprite):
    def __init__(self, groups, enemy_sprites, player, screen_dim, game):
        super().__init__(groups)
        self.player = player
        self.half_width = screen_dim[0] // 2
        self.half_height = screen_dim[1] // 2

        self.image = pygame.image.load("./graphics/aim/aim.png")
        self.image = pygame.transform.scale(self.image, CROSS_HAIR_DIM)
        self.rect = self.image.get_rect()
        self.adjusted_rect = self.rect

        self.enemy_sprites = enemy_sprites

        self.game = game

    def shoot(self):
        for sprite in self.enemy_sprites:
            if sprite.rect.colliderect(self.adjusted_rect):
                sprite.health_bar.decrease()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.adjusted_rect = self.rect.copy()
        self.adjusted_rect.centerx += self.player.rect.centerx-self.half_width
        self.adjusted_rect.centery += self.player.rect.centery-self.half_height