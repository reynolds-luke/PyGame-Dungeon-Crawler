import pygame
from settings import *
from character import *


class Slime(Charector):
    def __init__(self, game, groups, animations_names, animation_speed, graphics_path, graphics_scaling,
                 starting_graphic, hitbox_scaling, pos, speed, health, damage_cooldown, collision_groups):
        super().__init__(game = game, type="slime", groups=groups, animations_names=animations_names,
                         animation_speed=animation_speed, graphics_path=graphics_path,
                         graphics_scaling=graphics_scaling, starting_graphic=starting_graphic, status="slime_animation",
                         hitbox_scaling=hitbox_scaling, pos=pos, speed=speed, health=health,
                         damage_cooldown=damage_cooldown, collision_groups=collision_groups,
                         spawn_immunity_time=ENEMY_TIME_BEFORE_ATTACK)
        self.player = self.game.player
        self.hitbox.center = self.find_valid_spawn(self.game.world.map, self.player.rect.center)
        self.rect.center = self.hitbox.center

    def find_valid_spawn(self, world, player_pos):
        possible_locations = [pos for pos in world if world[pos] == "new_floor" and (pos[0]-player_pos[0])**2+(pos[1]-player_pos[1])**2 >= MIN_DIST]
        index = random.randint(1,len(possible_locations)-1)
        return possible_locations[index][0] * TILE_DIM[0], possible_locations[index][1] * TILE_DIM[1]

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
            self.player.take_damage()

    def check_if_dead(self):
        if self.is_dead:
            self.game.score_counter.add_to_score(100)
            self.game.enemies_remaining -= 1
            self.health_counter.health_bar.kill()
            self.health_counter.kill()
            self.kill()

    def update(self):
        if time.time()-self.time_of_creation >= ENEMY_TIME_BEFORE_ATTACK:
            self.calculate_motion()
            self.move()
            self.check_player_collision()
            self.check_if_dead()
        self.animate()