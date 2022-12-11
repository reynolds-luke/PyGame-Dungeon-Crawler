import pygame, random
from settings import *


class Potion(pygame.sprite.Sprite):
    """
    This class describes a potion object, that sometimes spawn in a room after the player defeats a level. The potion
    finds a valid location to spawn, then waits for the player to run into it. When it does, the potion applies its
    effect (which is random, of three possibilities) and then creates the new room for the player to explore
    """
    def __init__(self, groups, world, player, cross_hair):
        super().__init__(groups)  # We inherit from the python sprite class, with the given groups
        self.world = world  # This class needs access to the world (world map) object so it can create a new room
        self.player = player  # This class also needs to know what the player is, so it can detect collisions
        self.cross_hair = cross_hair  # Since some potion effects affect the crosshair, it is also included here

        # The following calculates possible spawn locations for the potion, given the world map
        spawn_locations = [] # We initialize to the empty list
        for pos in self.world.map:  # Then we iterate through all positions, and add them if they are valid spawn spots
            if self.world.map[pos] == "new_floor":
                spawn_locations.append(pos)
        self.pos = spawn_locations[random.randint(0, len(spawn_locations)-1)]  # We choose a location at random
        self.pos_scaled = (TILE_DIM[0] * self.pos[0], TILE_DIM[1] * self.pos[1])  # We scale to find the true spawn loc

        self.type = POTION_TYPES[random.randint(0, len(POTION_TYPES)-1)]  # We set the potion to be of a random type

        self.image = pygame.image.load(POTION_GRAPHICS_PATH+self.type+".png").convert_alpha()  # We load in the graphic
        self.image = pygame.transform.scale(self.image, TILE_DIM)  # We scale up the graphic to the right size
        self.rect = self.image.get_rect(center=self.pos_scaled)  # We create a rect so pygame knows where to draw it

        self.powerup_sound = pygame.mixer.Sound(POWERUP_SFX_PATH)  # The sound played when the player gets the potion
        self.powerup_sound.set_volume(POWERUP_SFX_VOLUME)  # Sets the appropriate volume

    def update(self):
        """
        This method is called by the game at every frame. It checks for collisions between the potion sprite and the
        player sprite. If there is a collision, it applies the effect, creates a new room, and then removes the potion
        sprite from the game.
        """
        if self.player.rect.colliderect(self.rect):  # If the potion has collides with the player...
            self.powerup_sound.play()  # Play the powerup sound
            if self.type == "double_damage":
                self.cross_hair.image = pygame.image.load(CROSSHAIR_DOUBLE_GRAPHICS_PATH)
                self.cross_hair.strength = 2  # Applies the "double damage" effect
            if self.type == "larger_crosshair":
                self.cross_hair.graphics_scale = CROSSHAIR_ENLARGED_DIM # Applies the "larger crosshair" effect
            if self.type == "speed":
                self.player.speed *= 1.5  # Applies the "speed" effect. Is cumulative

            self.world.create_room()  # Creates a new room
            self.kill()  # Removes the sprite from the game.
