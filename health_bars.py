import pygame, time
from helpers import *
from settings import *


class HealthCounter:
    """
    The HealthCounter class is a class that is used whenever a Character object is created that needs a health counter.
    It includes all the attributes/methods that are needed for an arbitrary type of health. Additionally, it creates a
    HealthBar object which deals with actually displaying the graphics.
    """

    def __init__(self, game, character, type, health):
        self.health = health # At the moment this is not used, but in the future could handle variable starting healths
        self.character = character  # We will refer to the character often, so include it as an attribute.
        self.type = type  # The type of Character (player, slime, etc)
        self.game = game  # We sometimes need to directly access the games methods/attributes, so we save it here

        # If this is a player health counter, we create a PlayerHealthBar
        if type == "player":
            self.health_bar = PlayerHealthBar(groups=self.game.camera_static_UI_sprites, counter=self,
                                              graphics_scaling=PLAYER_STATS_BAR_DIM)
        # If this is a slime health counter, we create an EnemyHealthBar with correct offset
        elif type == "slime":
            self.health_bar = EnemyHealthBar(groups=self.game.camera_dynamic_UI_sprites, counter=self,
                                             enemy=self.character, graphics_scaling=ENEMY_STATS_BAR_DIM,
                                             offset=pygame.math.Vector2(0, 40))
        # If this is a Dark Slime health counter, we create an EnemyHealthBar with correct offset
        elif type == "dark_slime":
            self.health_bar = EnemyHealthBar(groups=self.game.camera_dynamic_UI_sprites, counter=self,
                                             enemy=self.character, graphics_scaling=ENEMY_STATS_BAR_DIM,
                                             offset=pygame.math.Vector2(0, 80))

    def decrease_health(self, damage):
        """"
        This method is called whenever the character this health counter is related to takes damage. It simply relays
        that information to the health bar
        """
        self.health_bar.decrease(damage)  # We tell the health bar that the damage was decreased

    def kill_character(self):
        """"
        This method is called whenever the health bar reports that the character is dead. It simply relays that
        information to the character
        """
        self.character.is_dead = True


class HealthBar(pygame.sprite.Sprite):
    """
    The HealthBar class is a class that is used to create a health bar at a particular location. It contains all the
    code used by both the PlayerHealthBar and EnemyHealthBar classes.
    """

    def __init__(self, groups, counter, graphics_scaling):
        super().__init__(groups)  # We inherit the pygame Sprite class, with the given sprite groups
        self.frame_index = 0  # We initialize to hull health
        self.animation = import_folder(HEALTH_BAR_GRAPHICS_PATH)  # We load in the animation. See helpers.py
        self.graphics_scaling = graphics_scaling  # We set the graphics scaling appropriately
        self.counter = counter  # We remember which health counter we are related to

        self.image = pygame.image.load(HEALTH_BAR_STARTING_GRAPHIC_PATH).convert_alpha()  # We load in the graphic
        self.image = pygame.transform.scale(self.image, self.graphics_scaling)  # We scake appropriately
        self.rect = self.image.get_rect(topleft=(SPACING, SPACING))  # We set the location to the top left, by default.

    def decrease(self, damage):
        """
        This method is called whenever the character it is related to takes damage. It updates the graphic of
        health bar's animation. If it reached the end of the animation (i.e. no more health), then we report that
        the character has died.
        """
        self.frame_index += damage  # We update the frame of the health bar animation (i.e. total damage taken)

        if self.frame_index >= len(self.animation) - 1:  # If the health bar animation has finished...
            self.counter.kill_character()  # We call the character
        else:  # Otherwise...
            self.image = self.animation[self.frame_index]  # We draw the new graphic
            self.image = pygame.transform.scale(self.image, self.graphics_scaling)  # We rescale the image
            self.rect = self.image.get_rect(topleft=self.rect.topleft)  # We reset the rect object


class PlayerHealthBar(HealthBar):
    """
    The PlayerHealthBar class inherits the HealthBar class, and adds player-specific things such as the location and
    groups relating to the player health bar
    """

    def __init__(self, groups, counter, graphics_scaling):
        super().__init__(groups=groups, counter=counter, graphics_scaling=graphics_scaling)  # Inherit HealthBar class
        self.rect.topleft = (SPACING, SPACING)  # go to the correct location


class EnemyHealthBar(HealthBar):
    """
    The EnemyHealthBar class inherits the HealthBar class, and adds enemy-specific things such as following where the
    enemy sprite goes and having a brief spawn-in animation
    """

    def __init__(self, groups, counter, enemy, graphics_scaling, offset):
        super().__init__(groups=groups, counter=counter, graphics_scaling=graphics_scaling)  # Inherit HealthBar class
        self.offset = offset  # This saves how "offset" the center of the health bar is from the center of the character
        self.enemy = enemy  # Used so this object can reference its related character object

    def update(self):
        """
        This function is called at every frame, it tells the health bar where it should draw itself, given the location
        of the enemy and how long ago it was created
        """

        # This initial conditional checks to see if the spawn-in animation should be playing
        if time.time() - self.enemy.time_of_creation < self.enemy.time_before_attack:
            # The following three lines allow creates the spawn-in animation, where the health bar slowly fills up
            self.frame_index = int(
                4 - 4 * ((time.time() - self.enemy.time_of_creation) / self.enemy.time_before_attack))
            self.image = self.animation[self.frame_index]
            self.image = pygame.transform.scale(self.image, ENEMY_STATS_BAR_DIM)

        # Each frame, we move the health bar so that it follows its corresponding character, just below it.
        self.rect.center = self.enemy.rect.center + self.offset
