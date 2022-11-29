import pygame, sys
from player import *


class Game:
    def __init__(self):

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_DIM, SCREEN_DIM))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Redstone")

        self.player = Player(pos=(0, 0), size=10)

        self.moving_sprites = pygame.sprite.Group()
        self.moving_sprites.add(self.player)

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

            self.moving_sprites.update()

            self.screen.fill((59, 65, 82))
            self.moving_sprites.draw(self.screen)

            pygame.display.flip()

            self.clock.tick(FPS)


if __name__ == '__main__':
	game = Game()
	game.run()


