# Game Screen
SCREEN_DIM = (1080, 1920)
FPS = 60

TEXT_FONT = 'Algerian'
TEXT_SIZE = 50

TILE_DIM = (64, 64)
STATS_BAR_RATIO = (4,1)
SPACING = 10
BACKGROUND_COLOR = (0, 48, 59)

PLAYER_STATS_BAR_SIZE = 50
PLAYER_STATS_BAR_DIM = (PLAYER_STATS_BAR_SIZE * STATS_BAR_RATIO[0], PLAYER_STATS_BAR_SIZE * STATS_BAR_RATIO[1])
ENEMY_STATS_BAR_SIZE = 20
ENEMY_STATS_BAR_DIM = (ENEMY_STATS_BAR_SIZE * STATS_BAR_RATIO[0], ENEMY_STATS_BAR_SIZE * STATS_BAR_RATIO[1])

CROSS_HAIR_DIM = (50, 50)
CROSS_HAIR_ENLARGED_DIM = (100, 100)

SCORE_DIGIT_RATIO = [24, 42]
SCORE_DIGITS_SIZE = 1
SCORE_DIGITS_DIM = [SCORE_DIGITS_SIZE*SCORE_DIGIT_RATIO[0], SCORE_DIGITS_SIZE*SCORE_DIGIT_RATIO[1]]

LEADERBOARD_FILE_NAME = "leaderboard.csv"

SHOOT_VOLUME = 0.2
CHARACTER_HURT_VOLUME = 1

# Graphics Settings
PLAYER_ANIMATION_NAMES = ["up", "down", "left", "right", "up_idle", "down_idle", "left_idle", "right_idle"]
PLAYER_GRAPHICS_PATH = "./graphics/player/"

SLIME_ANIMATION_NAMES = ["slime_animation"]
SLIME_GRAPHICS_PATH = "./graphics/slime/"

DARK_SLIME_ANIMATION_NAMES = ["dark_slime_animation"]
DARK_SLIME_GRAPHICS_PATH = "./graphics/dark_slime/"
DARK_SLIME_STARTING_GRAPHIC_PATH = "./graphics/dark_slime/dark_slime_animation/sprite_0.png"

CROSS_HAIR_GRAPHICS_PATH = "./graphics/aim/aim.png"

HEALTH_BAR_GRAPHICS_PATH = "./graphics/health_bar/"
HEALTH_BAR_STARTING_GRAPHIC_PATH = "./graphics/health_bar/sprite_0.png"

DIGITS_FILE_PATH = "./graphics/digits/"

TILES_GRAPHICS_PATH = "./graphics/tiles/"
TILES_STARTING_GRAPHIC_PATH = "./graphics/tiles/floor.png"

# Player Settings
PLAYER_ANIMATION_SPEED = 0.15
PLAYER_WALK_SPEED = TILE_DIM[0] / 7
PLAYER_HEALTH = 4
PLAYER_DAMAGE_COOLDOWN = 1
PLAYER_SPAWN_IMMUNITY_TIME = 0

# Slime Settings
SLIME_ANIMATION_SPEED = 0.15
SLIME_WALK_SPEED = 0.7 * PLAYER_WALK_SPEED
SLIME_HEALTH = 4
SLIME_DAMAGE_COOLDOWN = 1

# Dark Slime Settings
DARK_SLIME_ANIMATION_SPEED = 0.3 * SLIME_ANIMATION_SPEED
DARK_SLIME_WALK_SPEED = 0.3 * SLIME_WALK_SPEED
DARK_SLIME_HEALTH = 4
DARK_SLIME_DAMAGE_COOLDOWN = 1

# Enemy Settings
WAVES = [{"slime_count": 1, "dark_slime_count": 0},
         {"slime_count": 0, "dark_slime_count": 1},
         {"slime_count": 2, "dark_slime_count": 1},
         {"slime_count": 3, "dark_slime_count": 2},
         {"slime_count": 10, "dark_slime_count": 5},
         {"slime_count": 15, "dark_slime_count": 5},
         {"slime_count": 15, "dark_slime_count": 10}]


# Potion Settings
POTION_GRAPHICS_PATH = "./graphics/potions/"
POTION_TYPES = ["double_damage", "larger_crosshair", "speed"]


# Room Settings
OBSTACLE_TILES = ["wall", "gate"]


# Enemy Spawn info
MIN_DIST = 8
