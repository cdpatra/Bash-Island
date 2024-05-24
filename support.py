from csv import reader
from settings import *
from os import walk
import pygame

def import_csv_layout(path):
    tile_layout = []
    with open(path) as map:
        # here level is <_csv.reader object> and we can iterate through it
        level = reader(map, delimiter=',')
        for row in level:
            tile_layout.append(list(row))
    return tile_layout


def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    # it gives the number of tiles require in x direction
    tile_num_x = int(surface.get_size()[0]/tile_size)
    # it gives the number of tiles require in y direction
    tile_num_y = int(surface.get_size()[1]/tile_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col*tile_size
            y = row*tile_size
            new_surf = pygame.Surface(
                (tile_size, tile_size), flags=pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), pygame.Rect(
                x, y, tile_size, tile_size))
            cut_tiles.append(new_surf)

    return cut_tiles


def import_folder(path):

    img_surface_list = []
    for file_path, file_directory, files in walk(path):
        for images in files:
            full_path = path + '/' + images
            img_surface = pygame.image.load(full_path).convert_alpha()
            img_surface_list.append(img_surface)

    return img_surface_list
