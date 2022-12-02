import pygame, random
from math import floor, ceil
from os import walk


def import_folder(path):
    surface_list = []

    for _, _, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list


def create_starting_room(dim):
    world = dict()
    dim[0] += 2
    dim[1] +=2
    for row in range(-floor(dim[0] / 2), ceil(dim[0] / 2)):
        for col in range(-floor(dim[1] / 2), ceil(dim[1] / 2)):
            if row == -floor(dim[0] / 2) or row == ceil(dim[0] / 2) - 1 or col == -floor(dim[1] / 2) or col == ceil(
                    dim[1] / 2) - 1:
                world[(row, col)] = "wall"
            else:
                world[(row, col)] = "floor"

    return world


def generate_room():
    room_type = random.randint(0,1)
    if room_type == 0:
        return generate_rectangular_room()
    elif room_type == 1:
        return generate_circular_room()

def generate_rectangular_room():
    dim = [random.randint(5, 15), random.randint(5, 15)]
    room = dict()
    dim[0] += 2
    dim[1] +=2
    for row in range(-floor(dim[0] / 2), ceil(dim[0] / 2)):
        for col in range(-floor(dim[1] / 2), ceil(dim[1] / 2)):
            if row == -floor(dim[0] / 2) or row == ceil(dim[0] / 2) - 1 or col == -floor(dim[1] / 2) or col == ceil(
                    dim[1] / 2) - 1:
                room[(row, col)] = "wall"
            else:
                room[(row, col)] = "new_floor"

    room[(0,0)] = "activation"
    return room

def generate_circular_room():
    radius = random.randint(5,10)
    dim = [2*radius, 2*radius]
    room = dict()
    dim[0] += 2
    dim[1] +=2
    for row in range(-floor(dim[0] / 2), ceil(dim[0] / 2)):
        for col in range(-floor(dim[1] / 2), ceil(dim[1] / 2)):
            if row**2+col**2 < radius ** 2:
                room[(row, col)] = "new_floor"
            elif (abs(row)-1)**2+col**2 < radius**2 or row**2+(abs(col)-1)**2 < radius**2:
                room[(row, col)] = "wall"

    room[(0, 0)] = "activation"
    return room
