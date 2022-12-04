import pygame, sys
from player import *
from room import *
from helpers import *
from enemy import *
from stats import *
from aimer import *


class Game:
    def __init__(self):

        # Initialize Pygame
        pygame.init()
        #self.screen = pygame.display.set_mode(SCREEN_DIM, pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((700, 700))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Redstone")

        self.moving_sprites = pygame.sprite.Group()
        self.foreground_sprites = CameraGroup()
        self.tiles = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.activation_sprites = pygame.sprite.Group()
        self.stats_sprites = pygame.sprite.Group()

        self.difficulty = 1

        self.health_bar = Health_Bar(groups=[self.stats_sprites], game=self)
        self.stamina_bar = Stamina_Bar(groups=[self.stats_sprites], game=self)

        self.player = Player(pos=(0, 0), groups=[self.moving_sprites, self.foreground_sprites], game=self)
        self.cross_hair = Crosshair(groups=[self.stats_sprites])

        self.world = create_starting_room(dim=STARTING_ROOM_DIM)
        for pos in self.world.keys():
            pos_scaled = (TILE_DIM[0] * pos[0], TILE_DIM[1] * pos[1])
            groups = [self.tiles]
            if self.world[pos] == "wall":
                groups.append(self.obstacle_sprites)
                groups.append(self.foreground_sprites)

            StaticTile(pos=pos, pos_scaled=pos_scaled, type=self.world[pos], groups=groups, world=self.world)

    def regenerate_tiles(self):
        for sprite in iter(self.tiles):
            sprite.kill()

        for pos in self.world.keys():
            pos_scaled = (TILE_DIM[0] * pos[0], TILE_DIM[1] * pos[1])

            groups = [self.tiles]
            if self.world[pos] in OBSTACLE_TILES:
                groups.append(self.obstacle_sprites)
                groups.append(self.foreground_sprites)
            if self.world[pos] == "activation":
                groups.append(self.activation_sprites)

            StaticTile(pos=pos, pos_scaled=pos_scaled, type=self.world[pos], groups=groups, world=self.world)

    def create_room(self):
        playerx = self.player.rect.centerx // TILE_DIM[0]
        playery = self.player.rect.centery // TILE_DIM[1]
        distance = 0
        while True:
            distance += 1
            if self.world.get((playerx + distance, playery)) is None:
                direction = pygame.math.Vector2(1, 0)
                break
            if self.world.get((playerx - distance, playery)) is None:
                direction = pygame.math.Vector2(-1, 0)
                break
            if self.world.get((playerx, playery + distance)) is None:
                direction = pygame.math.Vector2(0, 1)
                break
            if self.world.get((playerx, playery - distance)) is None:
                direction = pygame.math.Vector2(0, -1)
                break

        new_room = generate_room()
        new_room = {(posx + playerx, posy + playery): new_room[(posx, posy)] for posx, posy in new_room}
        new_hallway = dict()
        d = 0

        while 0 != len([coordinate for coordinate in self.world.keys() if coordinate in new_room.keys()]):
            d += 1
            new_hallway[(playerx + d * direction.x, playery + d * direction.y)] = "new_path"
            new_hallway[(playerx + d * direction.x + direction.y, playery + direction.x + d * direction.y)] = "wall"
            new_hallway[(playerx + d * direction.x - direction.y, playery + d * direction.y - direction.x)] = "wall"

            new_room = {(posx + direction.x, posy + direction.y): new_room[(posx, posy)] for posx, posy in new_room}

        extra_hallway_length = 3 * random.randint(2, 5)
        for i in range(extra_hallway_length):
            d += 1
            new_hallway[(playerx + d * direction.x, playery + d * direction.y)] = "new_path"
            new_hallway[(playerx + d * direction.x + direction.y, playery + direction.x + d * direction.y)] = "wall"
            new_hallway[(playerx + d * direction.x - direction.y, playery + d * direction.y - direction.x)] = "wall"

            new_room = {(posx + direction.x, posy + direction.y): new_room[(posx, posy)] for posx, posy in new_room}

        world_update = dict()
        world_update.update({pos: "wall" for pos in new_hallway if new_hallway[pos] == "wall"})
        world_update.update({pos: "wall" for pos in self.world if self.world[pos] == "wall"})
        world_update.update({pos: "floor" for pos in self.world if self.world[pos] == "floor"})
        world_update.update({pos: "wall" for pos in new_room if new_room[pos] == "wall"})

        world_update.update({pos: "floor" for pos in self.world if self.world[pos] == "new_floor"})
        world_update.update({pos: "floor" for pos in self.world if self.world[pos] == "activation"})
        world_update.update({pos: "floor" for pos in self.world if self.world[pos] == "gate"})
        world_update.update({pos: "new_path" for pos in new_hallway if new_hallway[pos] == "new_path"})
        world_update.update({pos: "new_floor" for pos in new_room if new_room[pos] == "new_floor"})
        world_update.update({pos: "activation" for pos in new_room if new_room[pos] == "activation"})

        world_update.update(
            {pos: "gate_deactive" for pos in new_room if new_room[pos] == "wall" and new_hallway.get(pos) == "new_path"})
        self.world.update(world_update)

        self.regenerate_tiles()

    def begin_attack(self):
        world_update = {pos: "gate" for pos in self.world if self.world[pos] == "gate_deactive"}
        world_update.update({pos: "floor" for pos in self.world if self.world[pos] == "new_path"})
        world_update.update({pos: "new_floor" for pos in self.world if self.world[pos] == "activation"})
        for i in range(self.difficulty):
            Slime(groups=[self.moving_sprites, self.foreground_sprites, self.enemy_sprites], game=self)
        self.world.update(world_update)
        self.regenerate_tiles()

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
                        self.create_room()

            self.tiles.update()
            self.moving_sprites.update()
            self.stats_sprites.update()
            # 00303B
            self.screen.fill((0, 48, 59))
            self.tiles.custom_draw(self.player)
            self.foreground_sprites.custom_draw(self.player)
            self.stats_sprites.draw(self.screen)

            pygame.display.flip()

            self.clock.tick(FPS)

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
