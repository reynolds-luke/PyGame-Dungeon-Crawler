import pygame, sys, csv
from helpers import *

from world import *

from player import *
from slime import *
from dark_slime import *
from potion import *

from health_bars import *
from score import *
from crosshair import *


class Game:
    def __init__(self):

        # Initialize Pygame
        pygame.init()
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Algerian', 50)
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
        self.player = Player(game=self, groups=[self.foreground_sprites], pos = (0,0),
                             collision_groups=[self.obstacle_sprites])

        self.cross_hair = Crosshair(groups=[self.camera_static_UI_sprites], enemy_sprites=self.enemy_sprites,
                                    player=self.player, screen_dim=self.screen.get_size(), game=self)

        self.score_counter = ScoreCounter(game=self)

        # Creating the start of the level
        self.alive = True
        self.world = World(game=self)
        self.difficulty = 0
        self.enemies_remaining = -1
        self.world.create_room()

    def begin_attack(self):
        self.world.begin_attack()
        print("BEGIN ATTACK", self.difficulty)
        self.enemies_remaining = 0
        for i in range(WAVES[self.difficulty]["slime_count"]):
            self.enemies_remaining += 1
            Slime(game=self, groups=[self.foreground_sprites, self.enemy_sprites], pos=self.player.rect.center,
                  collision_groups=[self.obstacle_sprites, self.enemy_sprites], time_before_attack=3)
        for i in range(WAVES[self.difficulty]["dark_slime_count"]):
            self.enemies_remaining += 1
            DarkSlime(game=self, groups=[self.foreground_sprites, self.enemy_sprites], pos=self.player.rect.center,
                      collision_groups=[self.obstacle_sprites, self.enemy_sprites], time_before_attack=3)
        self.difficulty += 1

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
                        Potion(groups=[self.foreground_sprites], map=self.world.map, player=self.player, cross_hair=self.cross_hair)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.cross_hair.shoot()

            if self.enemies_remaining == 0:
                self.enemies_remaining = -1
                create_potion = random.randint(1,3)
                if create_potion == 1:
                    Potion(groups=[self.foreground_sprites], world=self.world, player=self.player,
                           cross_hair=self.cross_hair)
                else:
                    self.world.create_room()

            if False:
                self.draw_game_screen()
            else:
                self.get_name()
                self.draw_leaderboard_screen()

            pygame.display.flip()
            self.clock.tick(FPS)

    def draw_game_screen(self):
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

    def draw_leaderboard_screen(self):
        leaderboard_file_name = "leaderboard.csv"
        self.screen.fill(BACKGROUND_COLOR)
        entries = []
        with open(leaderboard_file_name, 'r') as csvfile:
            csvreader = csv.reader(csvfile)

            for row in csvreader:
                entries.append(row)
        entries = entries[1:]
        entries.sort(key=(lambda row: int(row[1])), reverse=True)
        displayed_entries = entries[: 10]

        print(entries)

        text_surface = self.my_font.render('LEADERBOARD', True, (255, 255, 255))
        self.screen.blit(text_surface, (SPACING,SPACING))
        height = 50
        for idx in range(len(displayed_entries)):
            height += 50
            row = displayed_entries[idx]
            text_surface = self.my_font.render(f'{idx+1}. {row[0]}:-----------{row[1]}', True, (255, 255, 255))
            self.screen.blit(text_surface, (SPACING, height))



    def get_name(self):
        self.screen.fill(BACKGROUND_COLOR)
        pygame.display.flip()
        name = ""
        font = pygame.font.Font(None, 50)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isalnum() or event.unicode.isspace():
                        if len(name) <= 10:
                            name += event.unicode
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_RETURN:
                        return
                self.screen.fill(BACKGROUND_COLOR)
                block = font.render(name, True, (255, 255, 255))
                rect = block.get_rect()
                rect.center = self.screen.get_rect().center
                self.screen.blit(block, rect)
                pygame.display.flip()



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
