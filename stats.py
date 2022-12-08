import pygame
from settings import *
import time
from helpers import *



class Player_Health_Bar(pygame.sprite.Sprite):
    def __init__(self, groups, game):
        super().__init__(groups)
        self.animation = None
        self.image = pygame.image.load("./graphics/health_bar/sprite_0.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, PLAYER_STATS_BAR_DIM)
        self.rect = self.image.get_rect(topleft=(10,10))
        self.frame_index = 0
        self.import_graphics()

        self.game = game

        self.last_hit_time = time.time()

    def import_graphics(self):
        health_bar_path = "./graphics/health_bar/"
        self.animation = import_folder(health_bar_path)

    def decrease(self):
        if time.time() - self.last_hit_time >= HEALTHBAR_COOLDOWN:
            self.game.player.hurt_player()
            self.last_hit_time = time.time()
            self.frame_index += 1

            self.image = self.animation[self.frame_index]
            self.image = pygame.transform.scale(self.image, PLAYER_STATS_BAR_DIM)
            self.rect = self.image.get_rect(topleft=self.rect.topleft)

            self.rect = self.image.get_rect(topleft=(10, 10))

            if self.frame_index == len(self.animation) - 1:
                self.game.game_over()


class Enemy_Health_Bar(pygame.sprite.Sprite):
    def __init__(self, groups, enemy, game):
        super().__init__(groups)
        self.game = game
        self.offset = pygame.math.Vector2(0,40)
        self.animation = None
        self.image = pygame.image.load("./graphics/health_bar/sprite_0.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, ENEMY_STATS_BAR_DIM)
        self.rect = self.image.get_rect(topleft=(10,10))
        self.frame_index = 0
        self.import_graphics()

        self.enemy = enemy

        self.last_hit_time = time.time()

    def import_graphics(self):
        health_bar_path = "./graphics/health_bar/"
        self.animation = import_folder(health_bar_path)

    def decrease(self):
        if time.time() - self.last_hit_time >= HEALTHBAR_COOLDOWN:
            self.enemy.hurt_enemy()
            self.last_hit_time = time.time()
            self.frame_index += 1

            self.image = self.animation[self.frame_index]
            self.image = pygame.transform.scale(self.image, ENEMY_STATS_BAR_DIM)
            self.rect = self.image.get_rect(topleft=self.rect.topleft)

            self.rect = self.image.get_rect(topleft=(10, 10))

            if self.frame_index == len(self.animation) - 1:
                self.game.enemies_remaining -= 1
                self.enemy.kill()
                self.kill()

    def update(self):
        if time.time()-self.enemy.time_of_creation < ENEMY_TIME_BEFORE_ATTACK:
            self.frame_index = int(4-4*((time.time()-self.enemy.time_of_creation) / ENEMY_TIME_BEFORE_ATTACK))
            self.image = self.animation[self.frame_index]
            self.image = pygame.transform.scale(self.image, ENEMY_STATS_BAR_DIM)
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        self.rect.center = self.enemy.rect.center+self.offset

class Stamina_Bar(pygame.sprite.Sprite):
    def __init__(self, groups, game):
        super().__init__(groups)
        self.animation = None
        self.image = pygame.image.load("./graphics/stamina_bar/sprite_0.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, PLAYER_STATS_BAR_DIM)
        self.rect = self.image.get_rect(topleft=(10,10+PLAYER_STATS_BAR_DIM[1]+5))
        self.frame_index = 0
        self.import_graphics()

        self.game = game

        self.last_attack_time = time.time()

    def import_graphics(self):
        health_bar_path = "./graphics/stamina_bar/"
        self.animation = import_folder(health_bar_path)