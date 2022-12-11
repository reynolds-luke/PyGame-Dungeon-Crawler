import pygame, random
from math import floor, ceil
from os import walk


# The import_folder helper function was originally written by ClearCode (see README.md). Comments by me.
def import_folder(path):
    """
    Given a file path to a folder, this function returns a list of images found within that folder.
    """
    surface_list = []  # We initialize the list of images (surfaces) to 0

    for _, _, img_files in walk(path):  # We get a list(s) of image files
        for image in img_files:  # For each of the image files...
            full_path = path + '/' + image  # We get the full path of the image
            image_surf = pygame.image.load(full_path).convert_alpha()  # We load in the image (i.e. the surface)
            surface_list.append(image_surf)  # We add the image to our list of surfaces
    return surface_list  # We return the list of surfaces
