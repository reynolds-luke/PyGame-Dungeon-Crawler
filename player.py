import pygame
from character import *


class Player(Character):
    def __init__(self, game, groups, pos, collision_groups):
        """
        The Player class inherits the Character class. It is the character that the user can control. It can move in
        four directions, as dictated by user input. Also, the player keeps track of when it runs into the activation
        tile at the center of each room, which triggers the next wave of enemies
        """
        super().__init__(game=game, type="player", groups=groups, animations_names=PLAYER_ANIMATION_NAMES,
                         animation_speed=PLAYER_ANIMATION_SPEED, graphics_path=PLAYER_GRAPHICS_PATH,
                         graphics_scaling=TILE_DIM, starting_graphic="./graphics/player/down/down_0.png",
                         status="down_idle", hitbox_scaling=(-4 * (TILE_DIM[0] / 16), -8 * (TILE_DIM[1] / 16)),
                         pos=pos, speed=PLAYER_WALK_SPEED, health=PLAYER_HEALTH, damage_cooldown=PLAYER_DAMAGE_COOLDOWN,
                         collision_groups=collision_groups, spawn_immunity_time=PLAYER_SPAWN_IMMUNITY_TIME)

    def get_status(self):
        """
        This method is called at every frame, and it just checks if the player is moving. If it is not, it adds the
        keyword "idle" onto the player's status so that the game knows not to animate it with a walking animation.
        """
        if self.direction.x == self.direction.y == 0:  # If not moving...
            if not "idle" in self.status:  # This ensures that the world "idle" doesn't get added on forever
                self.status += "_idle"

    def inputs(self):
        """
        This method is called at every frame, and it takes in the user's keyboard input (arrow keys or WASD) to control
        the player's movement.
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:  # If "up arrow" or "W" pressed
            self.direction.y = -1  # Start moving up
            self.status = "up"  # Set status for animations to "up"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:  # If "down arrow" or "S" pressed
            self.direction.y = 1  # Start moving down
            self.status = "down"  # Set status for animations to "down"
        else:
            self.direction.y = 0  # Stops unnecessary movement when neither going up nor down

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  # If "left arrow" or "A" pressed
            self.direction.x = -1  # Start moving left
            self.status = "left"  # Set status for animations to "left"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # If "right arrow" or "D" pressed
            self.direction.x = 1  # Start moving right
            self.status = "right"  # Set status for animations to "right"
        else:
            self.direction.x = 0  # Stops unnecessary movement when neither going left nor right

        if self.direction != (0, 0):  # Finally, we normalize the direction so that our movement speed is constant
            self.direction = self.direction.normalize()

    def check_for_activation(self):
        """
        This method is called at every frame, and it checks if the player has run into the activation sprite. If they
        did, then the method calls the begin_attack method in the game class
        """
        for sprite in self.game.activation_sprites:  # For each "activation tile" (will only be one, in current version)
            if sprite.rect.colliderect(self.rect):  # check collisions
                self.game.begin_attack()  # If there is a collision, tell the game to start an attack

    def check_if_dead(self):
        """
        This method simply checks at every frame if the character is dead. If is, it simply relays that information to
        the game class so that it can stop running the game
        """
        if self.is_dead:
            self.game.alive = False

    def update(self):
        """
        This method is called by the game class at every frame. It is the sequence of updates that the sprite does at
        each frame to continue playing
        """
        self.inputs()  # Check for user keyboard inputs
        self.move()  # Move, checking collisions along the way
        self.check_for_activation()  # Check if the player hit an activation tile
        self.check_if_dead()  # Check if the player is dead
        self.get_status()  # Update if the player is idle or not
        self.animate()  # Move to the next frame of the animation
