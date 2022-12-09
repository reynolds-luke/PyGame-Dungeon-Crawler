import pygame
from character import *

class Player(Charector):
    def __init__(self, game, groups, pos, collision_groups):
        super().__init__(game = game, type="player", groups=groups, animations_names=PLAYER_ANIMATION_NAMES,
                         animation_speed=PLAYER_ANIMATION_SPEED, graphics_path=PLAYER_GRAPHICS_PATH,
                         graphics_scaling=TILE_DIM, starting_graphic="./graphics/player/down/down_0.png",
                         status="down_idle", hitbox_scaling=(-4 * (TILE_DIM[0] / 16), -8 * (TILE_DIM[1] / 16)),
                         pos=pos, speed=PLAYER_WALK_SPEED, health=PLAYER_HEALTH, damage_cooldown=PLAYER_DAMAGE_COOLDOWN,
                         collision_groups=collision_groups,spawn_immunity_time=PLAYER_SPAWN_IMMUNITY_TIME)

    def get_status(self):
        if self.direction.x == self.direction.y == 0:
            if not "idle" in self.status:
                self.status += "_idle"

    def inputs(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
            self.status = "up"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            self.status = "down"
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.status = "left"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.status = "right"
        else:
            self.direction.x = 0

        if self.direction != (0,0):
            self.direction = self.direction.normalize()

    def check_for_activation(self):
        for sprite in self.game.activation_sprites:
            if sprite.rect.colliderect(self.rect):
                self.game.begin_attack()

    def check_if_dead(self):
        if self.is_dead:
            self.game.alive = False

    def update(self):
        self.inputs()
        self.move()
        self.check_for_activation()
        self.check_if_dead()
        self.get_status()
        self.animate()