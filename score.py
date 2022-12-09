import pygame
from settings import *
from helpers import *


class ScoreCounter(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.digit_sprites = pygame.sprite.Group()
        self.score = 0
        self.length = 0
        self.add_to_score(0)

    def add_to_score(self, bonus):
        self.score += bonus
        while self.length < len(str(self.score)):
            Digit(digit=self.length, groups=[self.digit_sprites, self.game.camera_static_UI_sprites],
                  real_screen_dim=self.game.real_screen_dim)
            self.length += 1

        self.update_digits()

    def update_digits(self):
        for sprite in self.digit_sprites:
            sprite.reset_digit(str(self.score))


class Digit(pygame.sprite.Sprite):
    def __init__(self, digit, groups, real_screen_dim):
        super().__init__(groups)
        self.digit = digit

        self.graphics = import_folder("./graphics/digits/")
        self.image = self.graphics[0]
        self.pos = real_screen_dim

        self.rect = self.image.get_rect(topright=(self.pos[0]-SPACING-digit*(SCORE_DIGITS_DIM[0]+SPACING/2), SPACING))

    def reset_digit(self, number):
        self.image = self.graphics[int(number[-(self.digit+1)])]
        self.image = pygame.transform.scale(self.image, SCORE_DIGITS_DIM)