import imp
import pygame
import sys
from settings import *
from level import *
from game_data import *
from ui import *

# python - m PyInstaller main.py --onefile -w (command for pyinstaller)

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
bg_surf = pygame.Surface((screen_width, screen_height))
bg_surf = pygame.image.load(
    './resources/decorations/background.png').convert_alpha()
pygame.display.set_caption("Bash Island")
pygame.display.set_icon(pygame.image.load("./resources/game_logo.png"))
clock = pygame.time.Clock()

# Animated Screens
intro_UI = Animated_Screen(screen, './resources/UI/intro')
new_season_notification = Animated_Screen(
    screen, './resources/UI/New Season Notification')
replay_UI = Animated_Screen(screen, './resources/UI/replay')
next_level_toggle_UI = Animated_Screen(
    screen, './resources/UI/next level toggle')

# music
bg_music = pygame.mixer.Sound(
    './resources/sound/autism_island_iii_-_back_to_the_island.mp3')
bg_music.play(-1)


class Game:
    def __init__(self, level_data, surface):
        self.level_data = level_data
        self.display_surface = surface
        self.current_health = 2
        self.sole_coins_amount = 0
        self.IF_WON = False
        self.won_sound = pygame.mixer.Sound('./resources/sound/round_end.wav')
        self.won_sound.set_volume(0.3)

        # initializatioin of level
        self.level = Level(self.level_data, self.display_surface,
                           self.change_sole_coin_amount, self.change_health, self.check_IF_WON)

        # User Interface
        self.ui = UI(self.display_surface)

        # Sound
        self.lose_sound = pygame.mixer.Sound('./resources/sound/death.wav')

    def change_sole_coin_amount(self):
        self.sole_coins_amount += 1

    def change_health(self, amount):
        self.current_health -= amount

    def check_IF_WON(self):
        self.IF_WON = True

    def level_update(self, level_data):
        self.level_data = level_data
        self.level = Level(self.level_data, self.display_surface,
                           self.change_sole_coin_amount, self.change_health, self.check_IF_WON)

    def run(self, level_no):
        if self.IF_WON:
            self.won_sound.play()
            self.IF_WON = False
            return ('won', self.sole_coins_amount)

        elif self.current_health >= 0:
            self.level.run()  # level run here
            self.ui.show_health(self.current_health)
            self.ui.show_sole_coin(self.sole_coins_amount)
            self.ui.show_level(level_no)
            return ('play', self.sole_coins_amount)

        elif self.current_health < 0:
            self.lose_sound.play()
            return ('lose', self.sole_coins_amount)

    def replay(self, level_data):
        self.current_health = 2
        self.sole_coins_amount = 0
        self.level_data = level_data
        self.level = Level(self.level_data, self.display_surface,
                           self.change_sole_coin_amount, self.change_health, self.check_IF_WON)


level_list = [level_0, level_1, level_2]
level_index = 2
game = Game(level_list[level_index], screen)
game_status = 'intro'
coin_amount = 0
click_time = 0
while True:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        keys = pygame.key.get_pressed()

    if game_status == 'intro':
        intro_UI.update()
        start_button = Button(762, 525, 213, 39)
        if start_button.check_collision() or keys[pygame.K_RETURN]:
            level_index = 0
            game.level_update(level_list[level_index])
            game.replay(level_list[level_index])
            game_status = 'play'

    if game_status == 'play':
        screen.blit(bg_surf, (0, 0))
        (game_status, coin_amount) = game.run(level_index+1)

    if game_status == 'lose':
        replay_UI.update()
        replay_UI.show_score('YOU LOSE', coin_amount)
        replay_button = Button(492, 554, 213, 39)
        if replay_button.check_collision() or keys[pygame.K_RETURN]:
            game.replay(level_list[level_index])
            game_status = 'play'

    if game_status == 'won':
        next_level_toggle_UI.update()
        next_level_toggle_UI.show_score('YOU WON', coin_amount)
        next_button = Button(492, 554, 213, 39)
        if next_button.check_collision() or keys[pygame.K_RETURN]:
            level_index += 1
            if level_index >= len(level_list):
                game_status = 'new_season_notification'
                click_time = pygame.time.get_ticks()
            else:
                game.level_update(level_list[level_index])
                game.replay(level_list[level_index])
                game_status = 'play'

    if game_status == 'new_season_notification':
        new_season_notification.update()
        current_time = pygame.time.get_ticks()
        if current_time-click_time > 500:
            if next_button.check_collision() or keys[pygame.K_RETURN]:
                game_status = 'intro'

    pygame.display.update()
    clock.tick(60)
