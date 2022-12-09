import pygame, time
from helpers import *
from settings import *
from health_bars import *

class Charector(pygame.sprite.Sprite):
    def __init__(self, game, type, groups, animations_names, animation_speed, graphics_path, graphics_scaling,
                 starting_graphic, status, hitbox_scaling, pos, speed, health, damage_cooldown, collision_groups,
                 spawn_immunity_time):
        super().__init__(groups)
        self.game = game
        self.type = type
        self.time_of_creation = time.time()

        self.animations_names = animations_names
        self.animations = dict()
        self.animation_speed = animation_speed
        self.frame_index = self.frame_index = random.randint(1, len(animations_names))
        self.graphics_path = graphics_path
        self.graphics_scaling = graphics_scaling
        self.hitbox_scaling = hitbox_scaling
        self.status = status
        self.hurt_sound = pygame.mixer.Sound("./sounds/damage_sfx.wav")
        self.import_graphics()

        self.image = pygame.image.load(starting_graphic).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.graphics_scaling)
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(self.hitbox_scaling)

        self.speed = speed
        self.direction = pygame.math.Vector2()

        self.collision_groups = collision_groups

        self.health_counter = HealthCounter(game=self.game, charector=self, type=type, health=health)
        self.last_hit_time = time.time()
        self.damage_cooldown = damage_cooldown
        self.spawn_immunity_time = spawn_immunity_time
        self.has_been_attacked = False
        self.is_dead = False

    def import_graphics(self):
        for animation in self.animations_names:
            full_path = self.graphics_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        current_animation = self.animations[self.status]
        self.frame_index += self.animation_speed

        if self.frame_index >= len(current_animation):
            self.frame_index = 0

        self.image = current_animation[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, self.graphics_scaling)

        if time.time() - self.last_hit_time <= 0.5 and self.has_been_attacked:
            if 20 * (time.time() - self.last_hit_time) % 2 <= 1:
                self.image.fill((255, 100, 100), special_flags=pygame.BLEND_RGB_ADD)

    def take_damage(self, damage):
        self.has_been_attacked = True
        if time.time()-self.last_hit_time >= self.damage_cooldown:
            if time.time()-self.time_of_creation >= self.spawn_immunity_time:
                # self.hurt_sound.play()
                self.last_hit_time = time.time()
                self.health_counter.decrease_health(damage)

    def move(self):
        self.hitbox.x += self.direction.x * self.speed
        for group in self.collision_groups:
            self.collision("horizontal", group)

        self.hitbox.y += self.direction.y * self.speed
        for group in self.collision_groups:
            self.collision("vertical", group)

        self.rect.center = self.hitbox.center

    def collision(self, direction, group):
        if direction == 'horizontal':
            for sprite in group:
                if sprite == self:
                    pass
                elif sprite.rect.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.rect.left
                    else:
                        self.hitbox.left = sprite.rect.right

        if direction == "vertical":
            for sprite in group:
                if sprite == self:
                    pass
                elif sprite.rect.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.rect.top
                    else:
                        self.hitbox.top = sprite.rect.bottom
