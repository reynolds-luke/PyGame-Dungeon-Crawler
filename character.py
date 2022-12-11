import pygame, time
from helpers import *
from settings import *
from health_bars import *


class Character(pygame.sprite.Sprite):
    """
    The Character class is a class describes "characters" like the player and the slime. This separates methods that
    all character classes have in common, like collisions, movements, and health so that there is no need to rewrite
    these functions in the future.
    """

    def __init__(self, game, type, groups, animations_names, animation_speed, graphics_path, graphics_scaling,
                 starting_graphic, status, hitbox_scaling, pos, speed, health, damage_cooldown, collision_groups,
                 spawn_immunity_time):
        super().__init__(groups)  # We inherit the pygame Sprite class, with the given sprite groups
        self.game = game  # We keep the game itself as an attribute, for when we need to cause things to happen
        self.type = type  # 'type' is the type of character (player, slime, etc)
        self.time_of_creation = time.time()  # This is used when the character has a "loading" animation when created

        self.animations_names = animations_names  # For characters with multiple animations (e.g. "up", "left", etc)
        self.animations = dict()  # Eventually, we wil load in animations into a dictionary
        self.animation_speed = animation_speed  # The rate at which the animation is played
        self.frame_index = self.frame_index = random.randint(1, len(animations_names))  # Current frame of the animation
        self.graphics_path = graphics_path  # The file path to find the animation images
        self.graphics_scaling = graphics_scaling  # We scale up the images, because originally they are small.
        self.hitbox_scaling = hitbox_scaling  # The sprites' hit boxes are all smaller than the actual image
        self.status = status  # This stores when the player is idle, but in the future it may have other roles as well
        self.hurt_sound = pygame.mixer.Sound(CHARACTER_HURT_SFX_PATH)  # plays when the character is hurt
        self.hurt_sound.set_volume(CHARACTER_HURT_VOLUME) # Sets the appropriate volume
        self.import_graphics()  # Calls the method to import all the animations int other dictionary self.animations

        self.image = pygame.image.load(starting_graphic).convert_alpha()  # We initialize the image
        self.image = pygame.transform.scale(self.image, self.graphics_scaling)  # We scale up the image to desired size
        self.rect = self.image.get_rect(center=pos)  # pygame requires a "rect" object to know where to draw the sprite
        self.hitbox = self.rect.inflate(self.hitbox_scaling)  # The hit box follows the rect, but we scale it

        self.speed = speed  # The walking speed
        self.direction = pygame.math.Vector2()  # Which direction the character is walking

        self.collision_groups = collision_groups  # Stores which sprites should be treated as collision sprites.

        self.health_counter = HealthCounter(game=self.game, character=self, type=type, health=health)  # health_bars.py
        self.last_hit_time = time.time()  # Used for damage cool downs
        self.damage_cooldown = damage_cooldown  # How much time passes before the character can be attacked again
        self.spawn_immunity_time = spawn_immunity_time  # How much time the character is immune for after spawning
        self.has_been_attacked = False  # Used so the game doesn't show the "attacked" animation upon initialization
        self.is_dead = False  # Used so the character knows when to die

    def import_graphics(self):
        """
        This method imports all the animations needed for the sprite, adding them two a dictionary. The
        "self.animations" dictionary is such that the keys are the names of the animations, and the values are the list
        of animations. For example, an entry could be "right_walk": [frame1_image, frame2_image].
        """
        for animation in self.animations_names:  # Iterates through each animation
            full_path = self.graphics_path + animation
            self.animations[animation] = import_folder(full_path)  # See helpers.py for import_folder function

    def animate(self):
        """
        This function updates the image of the sprite so that it is on the correct frame of the animation
        """

        current_animation = self.animations[self.status]  # Loading in the correct animation list
        self.frame_index += self.animation_speed  # Every 1/animation_speed frames, self.frame_index increases by one

        if self.frame_index >= len(current_animation):  # Checks to see if we reached the end of the animation cycle
            self.frame_index = 0  # Reset animation

        self.image = current_animation[int(self.frame_index)]  # Set the image to the current frame of the animation
        self.image = pygame.transform.scale(self.image, self.graphics_scaling)  # Scale up the image accordingly

        # The following adds a blinking effect when the player is attacked
        if time.time() - self.last_hit_time <= 0.5 and self.has_been_attacked:
            if 20 * (time.time() - self.last_hit_time) % 2 <= 1:  # Creates the "blinking" effect.
                self.image.fill((255, 100, 100), special_flags=pygame.BLEND_RGB_ADD)

    def take_damage(self, damage):
        """
        This method makes the sprite take a certain amount of damage. It updates the healthbar and last_hit_time
        accordingly, and plays a sound
        """
        self.has_been_attacked = True
        if time.time() - self.last_hit_time >= self.damage_cooldown:  # Checks if cooldown grace period is over
            if time.time() - self.time_of_creation >= self.spawn_immunity_time:  # Checks if spawn grace period is over
                self.hurt_sound.play()  # Play the hurt sound
                self.last_hit_time = time.time()  # Reset the cooldown grace period timer
                self.health_counter.decrease_health(damage)  # See health_bars.py for the health_counter object

    def move(self):
        """
        This method uses the direction attribute to update the character's position, checking for collisions. Inspired
        from ClearCode's tutorials (see README.md)
        """

        # First we check for horizontal collisions
        self.hitbox.x += self.direction.x * self.speed
        for group in self.collision_groups:
            self.collision("horizontal", group)

        # Then we check for vertical collisions
        self.hitbox.y += self.direction.y * self.speed
        for group in self.collision_groups:
            self.collision("vertical", group)

        # We update self.rect to also be in the new position
        self.rect.center = self.hitbox.center

    def collision(self, direction, group):
        """
        This method checks for collisions between hitboxes, and adjusts the locations accordingly
        """
        if direction == 'horizontal':
            for sprite in group:  # For each collision sprite
                if sprite == self:  # We ignore the special case of colliding with ourselves
                    pass
                elif sprite.rect.colliderect(self.hitbox):  # We check for a collision
                    if self.direction.x > 0:  # If moving right, we hit their left side. Adjust accordingly.
                        self.hitbox.right = sprite.rect.left
                    else:  # If moving left, we hit their right side. Adjust accordingly.
                        self.hitbox.left = sprite.rect.right

        if direction == "vertical":
            for sprite in group:  # For each collision sprite
                if sprite == self:  # We ignore the special case of colliding with ourselves
                    pass
                elif sprite.rect.colliderect(self.hitbox):  # We check for a collision
                    if self.direction.y > 0:  # If moving down, we hit their top side. Adjust accordingly
                        self.hitbox.bottom = sprite.rect.top
                    else:  # If moving up, we hit their bottom side. Adjust accordingly.
                        self.hitbox.top = sprite.rect.bottom
