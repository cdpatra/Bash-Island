import pygame
from support import *
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift):
        self.rect.x += shift


class Static_Tile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface


class Crates(Static_Tile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y,  pygame.image.load(
            './resources/decorations/crates/crate.png').convert_alpha())
        y_offset = y+size
        self.rect = self.image.get_rect(bottomleft=(x, y_offset))


class Animated_Tile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames_surfaces = import_folder(path)
        self.frame_index = 0
        self.image = self.frames_surfaces[self.frame_index]

    def animate(self):
        self.frame_index += 0.10

        if self.frame_index >= len(self.frames_surfaces):
            self.frame_index = 0

        self.image = self.frames_surfaces[int(self.frame_index)]

    def update(self, shift):
        self.animate()
        self.rect.x += shift


class Sole_Coins(Animated_Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)


class Palms(Animated_Tile):
    def __init__(self, size, x, y, path, offset_y):
        super().__init__(size, x, y, path)
        self.rect=self.image.get_rect(topleft=(x,y))
        pygame.Rect.inflate_ip(self.rect,-10,60)
        y = y-offset_y
        self.rect.topleft= (x, y)


class Water():
    def __init__(self, top, level_width):
        start_water = -screen_width
        water_tile_size = 192  # in pixel
        tile_x_amount = 35
        self.water_sprite = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x = tile*water_tile_size + start_water
            y = top
            sprite = Animated_Tile(water_tile_size, x, y,
                                   './resources/decorations/water')
            self.water_sprite.add(sprite)

    def draw(self, surface, shift):
        self.water_sprite.update(shift)
        self.water_sprite.draw(surface)
