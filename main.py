import pygame, sys
from player import *
from room import *
from helpers import *

class Game:
    def __init__(self):

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_DIM, pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Redstone")

        self.foreground_sprites = CameraGroup()
        self.moving_sprites = pygame.sprite.Group()
        self.background_tiles = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.player = Player(pos=(0, 0), groups=[self.moving_sprites, self.foreground_sprites], obstacle_sprites=self.obstacle_sprites)

        self.world = create_starting_room(dim=[5,5])
        for pos in self.world.keys():
            pos_scaled = (TILE_DIM[0]*pos[0], TILE_DIM[1]*pos[1])
            groups = [self.background_tiles]
            if self.world[pos] == "wall":
                groups.append(self.obstacle_sprites)
                groups.append(self.foreground_sprites)

            StaticTile(pos=pos_scaled, type=self.world[pos], groups=groups)

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

            self.background_tiles.update()
            self.moving_sprites.update()

            self.screen.fill((59, 65, 82))
            self.background_tiles.custom_draw(self.player)
            self.foreground_sprites.custom_draw(self.player)

            pygame.display.flip()

            self.clock.tick(FPS)


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
            offset_rect = sprite.rect.topleft-self.offset
            self.display_surface.blit(sprite.image, offset_rect)

if __name__ == '__main__':
    game = Game()
    game.run()


