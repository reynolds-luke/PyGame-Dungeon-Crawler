import pygame, random
from settings import *
from character import *


class Slime(Character):
    """
    The Slime inherits the Character class. It is the smaller of the two enemies, moves quickly, and deals a small
    amount of damage to the player on contact. Worth 100 points if killed
    """

    def __init__(self, game, groups, pos, collision_groups, time_before_attack):
        # First, we initialize using the character class
        super().__init__(game=game, type="slime", groups=groups, animations_names=SLIME_ANIMATION_NAMES,
                         animation_speed=SLIME_ANIMATION_SPEED, graphics_path=SLIME_GRAPHICS_PATH,
                         graphics_scaling=TILE_DIM, starting_graphic="./graphics/slime/slime_animation/enemy0.png",
                         status="slime_animation", hitbox_scaling=(-4 * (TILE_DIM[0] / 16), -8 * (TILE_DIM[1] / 16)),
                         pos=pos, speed=SLIME_WALK_SPEED, health=SLIME_HEALTH, damage_cooldown=SLIME_DAMAGE_COOLDOWN,
                         collision_groups=collision_groups, spawn_immunity_time=time_before_attack)

        self.player = self.game.player  # As an enemy, the Dark Slime needs to have access the player
        self.time_before_attack = time_before_attack  # Used for the spawning animation

        # We randomize the position a bit, to make things more interesting
        pos = (pos[0] + random.randint(-3 * TILE_DIM[0], -3 * TILE_DIM[0]),
               pos[1] + random.randint(-3 * TILE_DIM[1], 3 * TILE_DIM[1]))
        self.hitbox.center = pos  # We must update the hitbox and rect to have this new position
        self.rect.center = self.hitbox.center

        # To disperse overlapping sprites during the spawn animation, we call the move function to do collisions
        self.move()

    def calculate_motion(self):
        """
        This method calculates which direction the Slime is going to move, given the location of the enemy. At present,
        it basically just goes towards the player, though in future developments of the game this could change to be
        more interesting.
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
        This method checks if the Slime is touching the player. If it is, it deals 1 damage points to the player.
        """
        if self.player.rect.colliderect(self.hitbox):  # If there is a collision...
            self.player.take_damage(1)  # Deal to damage to the player

    def check_if_dead(self):
        """
        This method checks to see if the Slime is dead. If it is, it kills off all its related objects and then removes
        itself from the game as well. It also increases the score by 100 points.
        """
        if self.is_dead:  # If the Slime died...
            self.game.score_counter.add_to_score(100)  # Add 100 to the score
            self.game.enemies_remaining -= 1  # Update the game to know it died

            # We end by killing off the Slime object and all its related objects
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
