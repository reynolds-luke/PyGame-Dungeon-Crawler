import pygame, sys
from player import *
from slime import *
from world import *
from helpers import *

from health_bars import *
from score import *
from crosshair import *


class Game:
    def __init__(self):

        # Initialize Pygame
        pygame.init()
        #self.screen = pygame.display.set_mode(SCREEN_DIM, pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((700, 700))
        self.real_screen_dim = pygame.display.get_surface().get_size()
        self.clock = pygame.time.Clock()

        pygame.mouse.set_visible(False)
        pygame.display.set_caption("The Dungeon")

        # Creating the sprite groups
        self.foreground_sprites = CameraGroup() # Player, Enemies, Walls, etc.
        self.background_sprites = CameraGroup() # Floor Tiles
        self.activation_sprites = CameraGroup() # The activation tile in the center of each room

        self.obstacle_sprites = pygame.sprite.Group() # Walls, Gates

        self.enemy_sprites = pygame.sprite.Group() # Slimes, Dark Slimes, Eggs

        self.camera_static_UI_sprites = pygame.sprite.Group() # UI elements that don't move with the player
        self.camera_dynamic_UI_sprites = CameraGroup() # UI elements that move with the player

        # Creating the sprites present from the start of the game
        self.player = Player(game=self, groups=[self.foreground_sprites], animations_names=PLAYER_ANIMATION_NAMES,
                             animation_speed=PLAYER_ANIMATION_SPEED, graphics_path=PLAYER_GRAPHICS_PATH,
                             graphics_scaling=TILE_DIM, starting_graphic="./graphics/player/down/down_0.png",
                             hitbox_scaling=(-4 * (TILE_DIM[0] / 16), -8 * (TILE_DIM[1] / 16)), pos=(0, 0),
                             speed=PLAYER_WALK_SPEED, health=PLAYER_HEALTH, damage_cooldown=PLAYER_DAMAGE_COOLDOWN,
                             collision_groups=[self.obstacle_sprites])

        self.cross_hair = Crosshair(groups=[self.camera_static_UI_sprites], enemy_sprites=self.enemy_sprites,
                                    player=self.player, screen_dim=self.screen.get_size(), game=self)

        self.score_counter = ScoreCounter(game=self)

        # Creating the start of the level
        self.difficulty = 0
        self.enemies_remaining = 0
        self.world = World(game=self)

    def begin_attack(self):
        self.world.begin_attack()
        print("BEGIN ATTACK")
        self.enemies_remaining = 0
        for i in range(10):
            self.enemies_remaining += 1
            Slime(game=self, groups=[self.foreground_sprites, self.enemy_sprites],
                  animations_names=SLIME_ANIMATION_NAMES, animation_speed=SLIME_ANIMATION_SPEED,
                  graphics_path=SLIME_GRAPHICS_PATH, graphics_scaling=TILE_DIM,
                  starting_graphic="./graphics/slime/slime_animation/enemy0.png",
                  hitbox_scaling=(-4 * (TILE_DIM[0] / 16), -8 * (TILE_DIM[1] / 16)), pos=(0, 0),
                  speed=SLIME_WALK_SPEED, health=SLIME_HEALTH, damage_cooldown=SLIME_DAMAGE_COOLDOWN,
                  collision_groups=[self.obstacle_sprites, self.enemy_sprites])

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_p:
                        self.world.create_room()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.cross_hair.shoot()

            if self.enemies_remaining == 0:
                self.world.create_room()

            self.draw_screen()
            pygame.display.flip()
            self.clock.tick(FPS)

    def draw_screen(self):
        self.background_sprites.update()
        self.foreground_sprites.update()
        self.camera_dynamic_UI_sprites.update()
        self.camera_static_UI_sprites.update()

        self.screen.fill(BACKGROUND_COLOR)
        self.background_sprites.custom_draw(self.player)
        self.foreground_sprites.custom_draw(self.player)
        self.camera_dynamic_UI_sprites.custom_draw(self.player)

        pygame.draw.rect(self.screen, BACKGROUND_COLOR, pygame.Rect(0, 0, self.real_screen_dim[0], 60))
        self.camera_static_UI_sprites.draw(self.screen)

    def game_over(self):
        print("game over!!!")


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(100, 200)
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_rect = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_rect)

    def print_sprites(self):
        for sprite in self.sprites():
            print(sprite)


if __name__ == '__main__':
    game = Game()
    game.run()
