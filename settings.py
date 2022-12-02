# Game Screen
TILE_DIM = (128, 128)
SCREEN_DIM = (1080, 1920)
FPS = 60

# Rooms
def get_wall(len):
    return ["w" for i in range(len)]
def get_open(len):
    return ["w"] + ["f" for i in range(len-2)] + ["w"]

ROOMS = []

ROOMSIZE = (10,15)
ROOM1 = [get_wall(ROOMSIZE[1]+2)] + ROOMSIZE[0]*[get_open(ROOMSIZE[1]+2)] + [get_wall(ROOMSIZE[1]+2)]
ROOMS.append(ROOM1)



