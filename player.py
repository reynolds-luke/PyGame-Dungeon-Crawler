import pygame
from settings import *
from helpers import *


# Define Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, game):
        super().__init__(groups)
        self.game = game
        self.activation_sprites = self.game.activation_sprites
        self.obstacle_sprites = self.game.obstacle_sprites

        self.pos = pos
        self.image = pygame.image.load("./graphics/player/down/down_0.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.hitbox_scaling = (-4*(TILE_DIM[0]/16), -8*(TILE_DIM[1]/16))
        self.hitbox = self.rect.inflate(self.hitbox_scaling)

        self.direction = pygame.math.Vector2()
        self.speed = TILE_DIM[0] / 7

        self.import_graphics()
        self.status = "down_idle"
        self.frame_index = 0
        self.animation_speed = 0.15

    def import_graphics(self):
        player_path = "./graphics/player/"
        self.animations = {"up": [], "down":[], "left":[], "right":[],
                           "up_idle": [], "down_idle":[], "left_idle":[], "right_idle":[]}

        for animation in self.animations.keys():
            full_path = player_path + animation
            self.animations[animation] = import_folder(full_path)

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

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, TILE_DIM)
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
        self.hitbox = self.rect.inflate(self.hitbox_scaling)

    def move(self):
        self.hitbox.x += self.direction.x*self.speed
        self.collision("horizontal")

        self.hitbox.y += self.direction.y*self.speed
        self.collision("vertical")

        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.rect.left
                    else:
                        self.hitbox.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.rect.top
                    else:
                        self.hitbox.top = sprite.rect.bottom

        for sprite in self.activation_sprites:
            if sprite.rect.colliderect(self.rect):
                self.game.create_room()

    def update(self):
        self.inputs()
        self.move()
        self.get_status()
        self.animate()
