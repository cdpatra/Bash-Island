import pygame
from support import *


class UI:
    def __init__(self, surface):
        # setup
        self.display_surface = surface

        # health bar
        self.life_list = import_folder('./resources/UI/life heart')

        # sole coins
        self.sole_coin = pygame.image.load('./resources/UI/sole_coin.png')
        self.sole_coin_rect = self.sole_coin.get_rect(topleft=(6, 35))
        self.font = pygame.font.Font('./resources/UI/Minercraftory.ttf', 23)

    def show_health(self, current_health):
        life_surface = self.life_list[current_health]
        self.display_surface.blit(life_surface, (20, 10))

    def show_sole_coin(self, amount):
        self.display_surface.blit(self.sole_coin, self.sole_coin_rect)
        sole_coin_amount_surface = self.font.render(
            str(amount), False, '#505050')
        sole_coin_amount_rect = sole_coin_amount_surface.get_rect(
            midleft=(self.sole_coin_rect.right, self.sole_coin_rect.centery+5))
        self.display_surface.blit(
            sole_coin_amount_surface, sole_coin_amount_rect)

    def show_level(self, level_no):
        level_surf = self.font.render(
            "Level"+" "+str(level_no), False, '#505050')
        level_rect = level_surf.get_rect(topleft=(1080, 17))
        self.display_surface.blit(level_surf, level_rect)


class Animated_Screen:
    def __init__(self, surface, path):
        self.display_surface = surface
        self.frame_list = import_folder(path)
        self.frame_index = 0
        self.image = self.frame_list[self.frame_index]
        self.frame_speed = 0.1
        self.primary_font = pygame.font.Font(
            './resources/UI/ALBAM___.TTF', 80)
        self.secondary_font = pygame.font.Font(
            './resources/UI/Minercraftory.ttf', 40)
        self.sole_coin_image = pygame.image.load(
            './resources/UI/sole_coin_display.png')

    def animate(self):
        self.frame_index += self.frame_speed
        if self.frame_index > len(self.frame_list):
            self.frame_index = 0

        self.image = self.frame_list[int(self.frame_index)]

    def show_score(self, message, coin_amount):
        message_surface = self.primary_font.render(message, False, 'white')
        message_rect = message_surface.get_rect(topleft=(425, 213))
        sole_coin_surface = self.secondary_font.render(
            str(coin_amount), False, '#505050')
        sole_coin_rect = sole_coin_surface.get_rect(topleft=(627, 350))

        self.display_surface.blit(self.sole_coin_image, (475, 330))
        self.display_surface.blit(sole_coin_surface, sole_coin_rect)
        self.display_surface.blit(message_surface, message_rect)

    def update(self):
        self.animate()
        self.display_surface.blit(self.image, (0, 0))


class Button:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect((x, y), (width, height))

    def check_collision(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                return True
            else:
                return False
        else:
            return False
