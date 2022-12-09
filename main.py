import pygame, sys
from player import *
from slime import *
from room import *
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

        self.world = create_starting_room(dim=STARTING_ROOM_DIM) # Of format (tile_x, tile_y): tile_type
        self.generated_tiles = dict() # Of format (tile_x, tile-y): is_already_created

        for pos in self.world.keys(): #
            pos_scaled = (TILE_DIM[0] * pos[0], TILE_DIM[1] * pos[1])
            groups = [self.background_sprites]
            if self.world[pos] == "wall":
                groups.append(self.obstacle_sprites)
                groups.append(self.foreground_sprites)

            StaticTile(pos=pos, pos_scaled=pos_scaled, type=self.world[pos], groups=groups, world=self.world)

    def regenerate_tiles(self):
        for sprite in iter(self.background_sprites):
            sprite.kill()

        for pos in self.world.keys():
            pos_scaled = (TILE_DIM[0] * pos[0], TILE_DIM[1] * pos[1])

            groups = [self.background_sprites]
            if self.world[pos] in OBSTACLE_TILES:
                groups.append(self.obstacle_sprites)
                groups.append(self.foreground_sprites)
            if self.world[pos] == "activation":
                groups.append(self.activation_sprites)

            StaticTile(pos=pos, pos_scaled=pos_scaled, type=self.world[pos], groups=groups, world=self.world)

    def create_room(self):
        self.enemies_remaining = -1
        self.difficulty += 1

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
            {pos: "gate_deactive" for pos in new_room if
             new_room[pos] == "wall" and new_hallway.get(pos) == "new_path"})
        self.world.update(world_update)

        self.regenerate_tiles()

    def begin_attack(self):
        self.enemies_remaining = 0
        world_update = {pos: "gate" for pos in self.world if self.world[pos] == "gate_deactive"}
        world_update.update({pos: "floor" for pos in self.world if self.world[pos] == "new_path"})
        world_update.update({pos: "new_floor" for pos in self.world if self.world[pos] == "activation"})

        for i in range(self.difficulty):
            self.enemies_remaining += 1
            Slime(game=self, groups=[self.foreground_sprites, self.enemy_sprites],
                  animations_names=SLIME_ANIMATION_NAMES, animation_speed=SLIME_ANIMATION_SPEED,
                  graphics_path=SLIME_GRAPHICS_PATH, graphics_scaling=TILE_DIM,
                  starting_graphic="./graphics/slime/slime_animation/enemy0.png",
                  hitbox_scaling=(-4 * (TILE_DIM[0] / 16), -8 * (TILE_DIM[1] / 16)), pos=(0, 0),
                  speed=SLIME_WALK_SPEED, health=SLIME_HEALTH, damage_cooldown=SLIME_DAMAGE_COOLDOWN,
                  collision_groups=[self.obstacle_sprites, self.enemy_sprites])
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

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.cross_hair.shoot()

            if self.enemies_remaining == 0:
                self.create_room()

            self.background_sprites.update()
            self.foreground_sprites.update()
            self.camera_dynamic_UI_sprites.update()
            self.camera_static_UI_sprites.update()

            # 00303B
            self.screen.fill((0, 48, 59))
            self.background_sprites.custom_draw(self.player)
            self.foreground_sprites.custom_draw(self.player)
            self.camera_dynamic_UI_sprites.custom_draw(self.player)

            pygame.draw.rect(self.screen, (0, 48, 59), pygame.Rect(0, 0, self.real_screen_dim[0], 60))
            self.camera_static_UI_sprites.draw(self.screen)

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
