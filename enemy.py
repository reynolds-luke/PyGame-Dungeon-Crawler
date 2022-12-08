import pygame, random, time
from settings import *
from helpers import *
from stats import *


# Define Player class
class Slime(pygame.sprite.Sprite):
    def __init__(self, groups, game):
        super().__init__(groups)
        self.game = game
        self.player = self.game.player
        self.obstacle_sprites = self.game.player_obstacle_sprites
        self.pos = self.find_valid_spawn(self.game.world, self.game.player.pos)
        self.image = pygame.image.load("./graphics/enemy/enemy_animation/enemy0.png").convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)
        self.time_of_creation = time.time()

        self.has_been_attacked = False
        self.last_hit_time = time.time()

        self.hitbox_scaling = (-4*(TILE_DIM[0]/16), -8*(TILE_DIM[1]/16))
        self.hitbox = self.rect.inflate(self.hitbox_scaling)

        self.health_bar = Enemy_Health_Bar(groups=[self.game.enemy_stats_sprites], enemy=self, game=self.game)

        self.direction = pygame.math.Vector2()
        self.speed = 0.8*self.game.player.speed

        self.import_graphics()
        self.frame_index = random.randint(1,5)
        self.animation_speed = 0.15

    def find_valid_spawn(self, world, player_pos):
        possible_locations = [pos for pos in world if world[pos] == "new_floor" and (pos[0]-player_pos[0])**2+(pos[1]-player_pos[1])**2 >= MIN_DIST]
        index = random.randint(1,len(possible_locations)-1)
        return (possible_locations[index][0]*TILE_DIM[0], possible_locations[index][1]*TILE_DIM[1])

    def import_graphics(self):
        enemy_path = "./graphics/enemy/"
        self.animations = {"enemy_animation": []}

        for animation in self.animations.keys():
            full_path = enemy_path + animation
            self.animations[animation] = import_folder(full_path)

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

    def hurt_enemy(self):
        self.has_been_attacked = True
        self.last_hit_time = time.time()

    def animate(self):
        animation = self.animations["enemy_animation"]

        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, TILE_DIM)

        if time.time()-self.last_hit_time <= 0.5 and self.has_been_attacked:
            if 20*(time.time()-self.last_hit_time) % 2 <= 1:
                self.image.fill((255, 100, 100), special_flags=pygame.BLEND_RGB_ADD)

        self.rect = self.image.get_rect(topleft=self.rect.topleft)
        self.hitbox = self.rect.inflate(self.hitbox_scaling)



    def move(self):
        self.hitbox.x += self.direction.x*self.speed
        self.collision("horizontal")

        self.hitbox.y += self.direction.y*self.speed
        self.collision("vertical")

        self.rect.center = self.hitbox.center
        self.pos = self.rect.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.game.enemy_obstacle_sprites:
                if sprite.rect.center == self.rect.center:
                    pass
                elif sprite.rect.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.rect.left
                    else:
                        self.hitbox.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.game.enemy_obstacle_sprites:
                if sprite.rect.center == self.rect.center:
                    pass
                elif sprite.rect.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.rect.top
                    else:
                        self.hitbox.top = sprite.rect.bottom


        if self.player.rect.colliderect(self.hitbox):
            self.game.health_bar.decrease()

    def update(self):
        if time.time()-self.time_of_creation >= ENEMY_TIME_BEFORE_ATTACK:
            self.calculate_motion()
            self.move()

        self.animate()