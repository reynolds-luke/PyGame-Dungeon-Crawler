import pygame
from settings import *


class Crosshair(pygame.sprite.Sprite):
    """
    The Character class is a class describes the crosshair, which is the way in which the player is able to aim and
    fire at enemies. It follows the mouse pointer, and when the mouse is clicked it "shoots" and checks to see if the
    player was able to hit an enemy.
    """

    def __init__(self, groups, player, enemy_sprites, screen_dim, game):
        super().__init__(groups)  # We inherit the pygame Sprite class, with the given sprite groups
        self.game = game  # We keep the game itself as an attribute, for when we need to cause things to happen

        # Because we want to check for collisions with the enemy, and the enemy sprites have a different coordinate
        # location system that has to do with the location of the player, we are required to also store the location
        # of the crosshair in this adjusted coordinate system. To evaluate this, we require the following attributes:
        self.player = player  # Needed to get the location of the player
        self.half_width = screen_dim[0] // 2
        self.half_height = screen_dim[1] // 2

        self.attack_sound = pygame.mixer.Sound()  # The game played when the player attacks
        self.attack_sound.set_volume(0.2)  # Sets the appropriate volume

        self.image = pygame.image.load(CROSSHAIR_GRAPHICS_PATH)  # Loads in the crosshair image
        self.image = pygame.transform.scale(self.image, CROSSHAIR_DIM)  # Scales up the image
        self.rect = self.image.get_rect()  # Pygame requires a "rect" object to know where to draw the sprite
        self.adjusted_rect = self.rect  # As explained earlier, we also need to track the adjusted coordinates
        self.strength = 1  # The "strength of" (i.e. damage associated with) the player attack
        self.graphics_scale = CROSSHAIR_DIM # How big we draw the crosshair

        self.enemy_sprites = enemy_sprites  # The group containing all the enemy sprites

    def shoot(self):
        """
        Activated by the game when the mouse is clicked. Plays the shooting sound, and checks for collisions with any of
        the sprites in the enemy_sprites group.
        """
        self.attack_sound.play()  # Play the attack sound
        for sprite in self.enemy_sprites:  # Loops through all enemy sprites
            if sprite.rect.colliderect(self.adjusted_rect):  # If we hit an enemy sprite (using adjusted coordinate!)...
                sprite.take_damage(self.strength)  # ...We call the enemy's "take_damage" method

    def update(self):
        """
        This method is called every frame, and it updates the crosshair's location (based on the mouse location) as well
        as the size of the crosshair (which can change with powerups.)
        """
        self.image = pygame.transform.scale(self.image, self.graphics_scale)
        self.rect.center = pygame.mouse.get_pos()  # We recenter the crosshair on the mouse location

        # The following lines adjust the adjusted_rect so that it is in the correct location in the adjusted coordinate
        # system that allows the crosshair to know when it hits an enemy.
        self.adjusted_rect = self.rect.copy()
        self.adjusted_rect.centerx += self.player.rect.centerx - self.half_width
        self.adjusted_rect.centery += self.player.rect.centery - self.half_height
