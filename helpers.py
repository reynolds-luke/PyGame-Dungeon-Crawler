import pygame
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
    for row in range(-floor(dim[0] / 2), ceil(dim[0] / 2)):
        for col in range(-floor(dim[1] / 2), ceil(dim[1] / 2)):
            if row == -floor(dim[0] / 2) or row == ceil(dim[0] / 2) - 1 or col == -floor(dim[1] / 2) or col == ceil(
                    dim[1] / 2) - 1:
                world[(row, col)] = "wall"
            else:
                world[(row, col)] = "floor"
    print(world.keys())
    return world
