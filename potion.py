import pygame, random
from settings import *


class Potion(pygame.sprite.Sprite):
    def __init__(self, groups, world, player, cross_hair):
        super().__init__(groups)
        self.world = world
        self.player = player
        self.cross_hair = cross_hair

        spawn_locations = []
        for pos in self.world.map:
            if self.world.map[pos] == "new_floor":
                spawn_locations.append(pos)

        self.pos = spawn_locations[random.randint(0, len(spawn_locations)-1)]
        self.pos_scaled = (TILE_DIM[0] * self.pos[0], TILE_DIM[1] * self.pos[1])

        self.type = POTION_TYPES[random.randint(0, len(POTION_TYPES)-1)]

        self.image = pygame.image.load(POTION_GRAPHICS_PATH+self.type+".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, TILE_DIM)
        self.rect = self.image.get_rect(center=self.pos_scaled)

    def update(self):
        if self.player.rect.colliderect(self.rect):
            if self.type == "double_damage":
                self.cross_hair.strength = 2
            if self.type == "larger_crosshair":
                print("here")
                self.cross_hair.graphics_dim = CROSS_HAIR_ENLARGED_DIM
            if self.type == "speed":
                self.player.speed *= 1.5
            self.world.create_room()
            self.kill()
