import pygame
from settings import *
from character import *
from slime import *


class DarkSlime(Charector):
    def __init__(self, game, groups, pos, collision_groups, time_before_attack):
        super().__init__(game = game, type="dark_slime", groups=groups, animations_names=DARK_SLIME_ANIMATION_NAMES,
                         animation_speed=DARK_SLIME_ANIMATION_SPEED, graphics_path=DARK_SLIME_GRAPHICS_PATH,
                         graphics_scaling=(2*TILE_DIM[0], 2*TILE_DIM[1]),
                         starting_graphic="./graphics/dark_slime/dark_slime_animation/sprite_0.png",
                         status="dark_slime_animation",
                         hitbox_scaling=(-4 * (TILE_DIM[0] / 16), -8 * (TILE_DIM[1] / 16)), pos=pos,
                         speed=DARK_SLIME_WALK_SPEED, health=DARK_SLIME_HEALTH,
                         damage_cooldown=DARK_SLIME_DAMAGE_COOLDOWN, collision_groups=collision_groups,
                         spawn_immunity_time=time_before_attack)
        self.groups = groups
        self.collision_groups = collision_groups
        self.player = self.game.player
        self.time_before_attack=time_before_attack
        self.hitbox.center = pos
        self.rect.center = self.hitbox.center
        self.move()

    def calculate_motion(self):
        if abs(self.rect.centerx - self.player.rect.centerx) < self.speed:
            self.direction.x = 0
        elif self.rect.centerx < self.player.rect.centerx:
            self.direction.x = 1
        else:
            self.direction.x = -1

        if abs(self.rect.centery - self.player.rect.centery) < self.speed:
            self.direction.y = 0
        elif self.rect.centery < self.player.rect.centery:
            self.direction.y = 1
        else:
            self.direction.y = -1

        if self.direction != (0,0):
            self.direction = self.direction.normalize()

    def check_player_collision(self):
        if self.player.rect.colliderect(self.hitbox):
            self.player.take_damage(2)

    def check_if_dead(self):
        if self.is_dead:
            self.game.score_counter.add_to_score(300)
            self.game.enemies_remaining -= 1
            for i in range(3):
                self.game.enemies_remaining += 1
                Slime(game=self.game, groups=self.groups, pos=self.rect.center,
                      collision_groups=self.collision_groups, time_before_attack=1)
            self.health_counter.health_bar.kill()
            self.health_counter.kill()
            self.kill()

    def update(self):
        if time.time()-self.time_of_creation >= self.time_before_attack:
            self.calculate_motion()
            self.move()
            self.check_player_collision()
            self.check_if_dead()
        self.animate()