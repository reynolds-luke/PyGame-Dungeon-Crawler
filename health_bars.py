import pygame, time
from helpers import *
from settings import *

class HealthCounter(pygame.sprite.Sprite):
    def __init__(self, game, charector, type, health):
        super().__init__()
        self.charector = charector
        self.type = type
        self.game = game

        if type == "player":
            self.health_bar = PlayerHealthBar(game=self.game, counter=self,
                                              graphics_scaling=PLAYER_STATS_BAR_DIM)

        if type == "slime":
            self.health_bar = EnemyHealthBar(game=self.game, counter=self, enemy=self.charector,
                                             graphics_scaling=ENEMY_STATS_BAR_DIM, offset=pygame.math.Vector2(0, 40))
        if type == "dark_slime":
            self.health_bar = EnemyHealthBar(game=self.game, counter=self, enemy=self.charector,
                                             graphics_scaling=ENEMY_STATS_BAR_DIM, offset=pygame.math.Vector2(0, 80))

    def decrease_health(self, damage):
        self.health_bar.decrease(damage)

    def kill_charector(self):
        self.charector.is_dead = True

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, groups, counter, graphics_scaling):
        super().__init__(groups)
        self.frame_index = 0
        self.animation = import_folder("./graphics/health_bar/")
        self.graphics_scaling = graphics_scaling
        self.counter = counter

        self.image = pygame.image.load("./graphics/health_bar/sprite_0.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.graphics_scaling)
        self.rect = self.image.get_rect(topleft=(SPACING, SPACING))

    def decrease(self, damage):
        self.frame_index += damage

        self.image = self.animation[self.frame_index]
        self.image = pygame.transform.scale(self.image, self.graphics_scaling)
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

        if self.frame_index >= len(self.animation) - 1:
            self.counter.kill_charector()


class PlayerHealthBar(HealthBar):
    def __init__(self, game, counter, graphics_scaling):
        self.game = game
        groups = [self.game.camera_static_UI_sprites]
        super().__init__(groups=groups, counter=counter, graphics_scaling=graphics_scaling)
        self.rect.topleft = (10, 10)


class EnemyHealthBar(HealthBar):
    def __init__(self, game, counter, enemy, graphics_scaling, offset):
        self.game = game
        groups = [self.game.camera_dynamic_UI_sprites]
        super().__init__(groups=groups, counter=counter, graphics_scaling=graphics_scaling)
        self.offset = offset
        self.enemy = enemy

    def update(self):
        if time.time()-self.enemy.time_of_creation < self.enemy.time_before_attack:
            self.frame_index = int(4-4*((time.time()-self.enemy.time_of_creation) / self.enemy.time_before_attack))
            self.image = self.animation[self.frame_index]
            self.image = pygame.transform.scale(self.image, ENEMY_STATS_BAR_DIM)
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        self.rect.center = self.enemy.rect.center + self.offset