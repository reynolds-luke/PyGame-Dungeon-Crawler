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


def generate_room():
    """
    This function creates a room dictionary, centered at (0,0)
    """
    room_type = random.randint(0, 1)  # We create a random room type: either rectangular or circular
    if room_type == 0:  # Case of creating a rectangular room
        dim = [random.randint(15, 25), random.randint(15, 25)]  # We initialize the random dimensions of the room
        room = create_rect_room(dim=dim, wall_name="wall", floor_name="new_floor")  # We create the room
        room[(0, 0)] = "activation"  # We add an activation tile at the center of the room
        return room
    elif room_type == 1:  # Case of creating a circular room
        radius = random.randint(10, 15)  # Chooses a random radius
        room = generate_circular_room(radius=radius, wall_name="wall", floor_name="new_floor")  # We create the room
        room[(0, 0)] = "activation"  # We add an activation tile at the center of the room
        return room


def create_rect_room(dim, wall_name, floor_name):
    """
    This function creates a rectangular room dictionary, given a dimension of the form (weight, height)
    """
    world = dict()  # initialize the world dictionary

    # We add 2 to the dimensions to account for the walls
    dim[0] += 2
    dim[1] += 2

    for row in range(-floor(dim[0] / 2), ceil(dim[0] / 2)):  # This iterates over the height, centering at zero
        for col in range(-floor(dim[1] / 2), ceil(dim[1] / 2)):  # This iterates over the width, centering at zero
            if row == -floor(dim[0] / 2) or row == ceil(dim[0] / 2) - 1 or col == -floor(dim[1] / 2) or col == ceil(
                    dim[1] / 2) - 1:  # This conditional checks to see if we are on the edge of the room and adds a wall
                world[(row, col)] = wall_name
            else:  # If we are not at the edge, we add a floor to the dictionary
                world[(row, col)] = floor_name

    return world  # We return the dictionary


def generate_circular_room(radius, wall_name, floor_name):
    """
    This function creates a circular room dictionary, given a radius
    """
    room = dict()

    dim = [2 * radius, 2 * radius]
    dim[0] += 2
    dim[1] += 2
    for row in range(-floor(dim[0] / 2), ceil(dim[0] / 2)):  # This iterates over the height, centering at zero
        for col in range(-floor(dim[1] / 2), ceil(dim[1] / 2)):  # This iterates over the width, centering at zero
            if row ** 2 + col ** 2 < radius ** 2:  # If fully within the radius, we add a floor
                room[(row, col)] = floor_name
            # If on the edge of being within the circle, we add a wall
            elif (abs(row) - 1) ** 2 + col ** 2 < radius ** 2 or row ** 2 + (abs(col) - 1) ** 2 < radius ** 2:
                room[(row, col)] = wall_name
    return room
