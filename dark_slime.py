import pygame
from settings import *
from character import *
from slime import *


class DarkSlime(Character):
    """
    The Dark Slime inherits the Character class. It is the larger of the two enemies, moves slowly, and deals high
    damage to the player on contact. When it dies, three regular slimes spawn where it died. Worth 300 points if killed.
    """

    def __init__(self, game, groups, pos, collision_groups, time_before_attack):
        # First, we initialize using the character class
        super().__init__(game=game, type="dark_slime", groups=groups, animations_names=DARK_SLIME_ANIMATION_NAMES,
                         animation_speed=DARK_SLIME_ANIMATION_SPEED, graphics_path=DARK_SLIME_GRAPHICS_PATH,
                         graphics_scaling=(2 * TILE_DIM[0], 2 * TILE_DIM[1]),
                         starting_graphic=DARK_SLIME_STARTING_GRAPHIC_PATH, status="dark_slime_animation",
                         hitbox_scaling=(-4 * (TILE_DIM[0] / 16), -8 * (TILE_DIM[1] / 16)), pos=pos,
                         speed=DARK_SLIME_WALK_SPEED, health=DARK_SLIME_HEALTH,
                         damage_cooldown=DARK_SLIME_DAMAGE_COOLDOWN, collision_groups=collision_groups,
                         spawn_immunity_time=time_before_attack)

        self.groups = groups  # We store this info so that when the Dark Slime dies, the new slimes have the same groups
        self.collision_groups = collision_groups  # The groups which the Dark Slime collides with
        self.player = self.game.player  # As an enemy, the Dark Slime needs to have access the player
        self.time_before_attack = time_before_attack  # Used for the spawning animation

        self.move() # This is just so that when the slimes spawn, collisions push them apart during the loading period

    def calculate_motion(self):
        """
        This method calculates which direction the Dark Slime is going to move, given the location of the enemy. At
        present, it basically just goes towards the player, though in future developments of the game this could
        change to be more interesting
        """
        if abs(self.rect.centerx - self.player.rect.centerx) < self.speed:  # This prevents 'jittering' of movement
            self.direction.x = 0
        elif self.rect.centerx < self.player.rect.centerx:  # If player is to right, move right
            self.direction.x = 1
        else:  # If player is to left, move left
            self.direction.x = -1

        if abs(self.rect.centery - self.player.rect.centery) < self.speed:  # This prevents 'jittering' of movement
            self.direction.y = 0
        elif self.rect.centery < self.player.rect.centery:  # If player is below, move down
            self.direction.y = 1
        else:  # If player is above, move up
            self.direction.y = -1

        if self.direction != (0, 0):  # We normalize the direction vector for constant movement speed
            self.direction = self.direction.normalize()

    def check_player_collision(self):
        """
        This method checks if the Dark Slime is touching the player. If it is, it deals 2 damage points to the player.
        """
        if self.player.rect.colliderect(self.hitbox):  # If there is a collision...
            self.player.take_damage(2)  # Deal to damage to the player

    def check_if_dead(self):
        """
        This method checks to see if the Dark Slime is dead. If it is, it kills off all its related objects and then
        removes itself from the game as well, adding 300 points. It also creates three smaller slimes where it died.
        """
        if self.is_dead:  # If the Dark Slime died...
            self.game.score_counter.add_to_score(300)  # Add 300 to the score
            self.game.enemies_remaining -= 1  # Update the game to know it died

            # The following loop creates three regular Slimes where the Dark Slime died
            for i in range(3):
                self.game.enemies_remaining += 1  # We make sure to tell the game we added enemies
                Slime(game=self.game, groups=self.groups, pos=self.rect.center,
                      collision_groups=self.collision_groups, time_before_attack=1)

            # We end by killing off the Dark Slime object and all its related objects
            self.health_counter.health_bar.kill()
            self.kill()

    def update(self):
        """
        This method is called every frame of the game, and controls how the Dark Slime is updated with each frame
        """
        if time.time() - self.time_of_creation >= self.time_before_attack:  # If not in the spawning state...
            self.calculate_motion()  # Figure out which direction to go
            self.move()  # Move in that direction
            self.check_player_collision()  # Check to see if we hit the player
            self.check_if_dead()  # Check to see if we died

        self.animate()  # Animate to the next frame. Note that this is outside the above conditional.
