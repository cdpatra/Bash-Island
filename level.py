import pygame
from support import *
from settings import *
from tiles import *
from enemies import *
from player import *


class Level:
    def __init__(self, level_data, surface, change_sole_coins, change_health, check_IF_WON):

        # general setup
        self.display_surface = surface
        self.world_shift = 0

        # user interface
        self.change_sole_coins = change_sole_coins
        self.change_health = change_health
        self.developer_name = pygame.image.load(
            './resources/UI/name.png').convert_alpha()

        # player setup
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)
        self.IF_WON = check_IF_WON

        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(
            terrain_layout, 'terrain')

        # grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # crates
        crates_layout = import_csv_layout(level_data['crates'])
        self.crates_sprites = self.create_tile_group(crates_layout, 'crates')

        # sole coins
        sole_coins_layout = import_csv_layout(level_data['sole coins'])
        self.sole_coins_sprites = self.create_tile_group(
            sole_coins_layout, 'sole coins')

        # foreground palms
        fg_palms_layout = import_csv_layout(level_data['fg palms'])
        self.fg_plams_sprites = self.create_tile_group(
            fg_palms_layout, 'fg palms')

        # background palms
        bg_palms_layout = import_csv_layout(level_data['bg palms'])
        self.bg_palms_sprites = self.create_tile_group(
            bg_palms_layout, 'bg palms')

        # house
        house_layout = import_csv_layout(level_data['house'])
        self.house_sprite = self.create_tile_group(house_layout, 'house')

        
        #enemy
        self.enemies_flag=False
        self.enemies2_flag=False
        self.enemies3_flag=False
        for check_key in level_data:
            if check_key=='enemies':
                enemies_layout = import_csv_layout(level_data['enemies'])
                self.enemies_sprites = self.create_tile_group(
                    enemies_layout, 'enemies')
                self.enemies_flag=True

            if check_key=='enemies2':
                enemies2_layout=import_csv_layout(level_data['enemies2'])
                self.enemies2_sprites=self.create_tile_group(enemies2_layout,'enemies2')
                self.enemies2_flag=True

            if check_key=='enemies3':
                enemies3_layout=import_csv_layout(level_data['enemies3'])
                self.enemies3_sprites=self.create_tile_group(enemies3_layout,'enemies3')
                self.enemies3_flag=True

        # constraints
        constraints_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(
            constraints_layout, 'constraints')

        # water
        level_width = (len(level_data['terrain'][0]))*tile_size
        self.water = Water(screen_height-60, level_width)

        # player enemy collision timer
        self.player_enemy_collision_initial_time = 0
        self.current_time = 0

        # Sounds
        self.enemy_collision_sound = pygame.mixer.Sound(
            './resources/sound/stomp.wav')
        self.sole_coin_collect_sound = pygame.mixer.Sound(
            './resources/sound/Picked Coin Echo 2.wav')
        self.won_sound = pygame.mixer.Sound('./resources/sound/round_end.wav')

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index*tile_size
                    y = row_index*tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics(
                            './resources/terrain/terrain_tiles.png')
                        terrain_tile_surface = terrain_tile_list[int(val)]
                        sprite = Static_Tile(
                            tile_size, x, y, terrain_tile_surface)

                    if type == 'grass':
                        grass_tile_list = import_cut_graphics(
                            './resources/decorations/grass/grass.png')
                        grass_tile_surface = grass_tile_list[int(val)]
                        sprite = Static_Tile(
                            tile_size, x, y, grass_tile_surface)

                    if type == 'house':
                        house_tile_list = import_cut_graphics(
                            './resources/decorations/house/house.png')
                        house_tile_surface = house_tile_list[int(val)]
                        sprite = Static_Tile(
                            tile_size, x, y, house_tile_surface)

                    if type == 'crates':
                        sprite = Crates(tile_size, x, y)

                    if type == 'sole coins':
                        sprite = Sole_Coins(
                            tile_size, x, y, './resources/sole coins')

                    if type == 'fg palms':
                        if val == '0':
                            sprite = Palms(
                                tile_size, x, y, './resources/palm trees/palm_small', 38)
                        if val == '1':
                            sprite = Palms(
                                tile_size, x, y, './resources/palm trees/palm_large', 68)

                    if type == 'bg palms':
                        sprite = Palms(tile_size, x, y,
                                       './resources/palm trees/palm_bg', 64)

                    if type == 'enemies':
                        sprite = Enemy(tile_size, x, y,'./resources/enemy')
                    
                    if type=='enemies2':
                        sprite=Enemy(tile_size,x,y,'./resources/enemy2')
                    
                    if type=='enemies3':
                        sprite=Static_Enemy(tile_size,x,y,'./resources/enemy3')

                    if type == 'constraints':
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)
        return sprite_group

    def enemy_reverse_detection(self):
        if self.enemies_flag:
            for enemy in self.enemies_sprites.sprites():
                if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                    enemy.reverse_motion()

        if self.enemies2_flag:
            for enemy2 in self.enemies2_sprites.sprites():
                if pygame.sprite.spritecollide(enemy2, self.constraint_sprites, False):
                    enemy2.reverse_motion()

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index*tile_size
                y = row_index*tile_size
                if val == '0':
                    sprite = Player((x, y), self.display_surface)
                    self.player.add(sprite)
                if val == '1':
                    sprite = Static_Tile(tile_size, x, y, pygame.image.load(
                        './resources/decorations/hat.png').convert_alpha())
                    self.goal.add(sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width/7 and direction_x < 0:
            player.speed = 0
            self.world_shift = 6
        elif player_x > screen_width - (screen_width/7) and direction_x > 0:
            player.speed = 0
            self.world_shift = -6
        else:
            player.speed = 6
            self.world_shift = 0

    def horizontal_movement_collisions(self):
        player = self.player.sprite
        player.rect.x += player.direction.x*player.speed
        collidable_sprites = self.terrain_sprites.sprites(
        ) + self.fg_plams_sprites.sprites()
        for sprite in collidable_sprites:
            if player.rect.colliderect(sprite.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right + 3
                    player.collide_on_left = True
                    self.collision_position_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left - 3
                    player.collide_on_right = True
                    self.collision_position_x = player.rect.right

        if player.collide_on_left and (player.rect.left < self.collision_position_x or player.direction.x >= 0):
            player.collide_on_left = False
        if player.collide_on_right and (player.rect.right > self.collision_position_x or player.direction.x <= 0):
            player.collide_on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites(
        ) + self.fg_plams_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0.5:
                    player.rect.bottom = sprite.rect.top
                    player.collide_on_floor = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.collide_on_ceiling = True
                player.direction.y = 0

        if player.collide_on_floor and player.direction.y < 0 or player.direction.y > 1:
            player.collide_on_floor = False
        elif player.collide_on_ceiling and player.direction.y > 0:
            player.collide_on_ceiling = False

    def detect_sole_coin_collision(self):
        collide_coin_list = pygame.sprite.spritecollide(
            self.player.sprite, self.sole_coins_sprites, True)
        for sole_coin in collide_coin_list:
            self.change_sole_coins()
            self.sole_coin_collect_sound.play()

    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
            self.change_health(3)

    def check_player_collision_with_enemy(self):
        if self.enemies_flag:
            player_enemy_collision_list = pygame.sprite.spritecollide(
                self.player.sprite, self.enemies_sprites, False)

        if self.enemies2_flag:
            player_enemy2_collision_list=pygame.sprite.spritecollide(self.player.sprite,self.enemies2_sprites,False)
            for sprites in player_enemy2_collision_list:
                player_enemy_collision_list.append(sprites)

        if self.enemies3_flag:
            player_enemy3_collision_list=pygame.sprite.spritecollide(self.player.sprite,self.enemies3_sprites,False)
            for sprites in player_enemy3_collision_list:
                player_enemy_collision_list.append(sprites)

        if player_enemy_collision_list:
            self.current_time = pygame.time.get_ticks()
            if self.current_time-self.player_enemy_collision_initial_time > 1000:
                for collision in player_enemy_collision_list:
                    self.change_health(1)
                    self.enemy_collision_sound.play()
                    self.player_enemy_collision_initial_time = pygame.time.get_ticks()

    def check_player_collision_with_goal(self):
        player_goal_collision_list = pygame.sprite.spritecollide(
            self.player.sprite, self.goal, False)
        for collision in player_goal_collision_list:
            self.IF_WON()

    # This method is used to run the level data which is imported

    def run(self):

        # Draw Background Palms
        self.bg_palms_sprites.draw(self.display_surface)
        self.bg_palms_sprites.update(self.world_shift)

        # Draw house
        self.house_sprite.draw(self.display_surface)
        self.house_sprite.update(self.world_shift)

        # Draw Terrain
        # This line is used to draw the rectangle on the display surface
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        # Draw Crates
        self.crates_sprites.draw(self.display_surface)
        self.crates_sprites.update(self.world_shift)

        # Draw Enemies and updating constraints
        self.enemies_sprites.draw(self.display_surface)
        if self.enemies2_flag:
            self.enemies2_sprites.draw(self.display_surface)
        if self.enemies3_flag:
            self.enemies3_sprites.draw(self.display_surface)

        # constraints
        self.enemy_reverse_detection()
        self.constraint_sprites.update(self.world_shift)
        self.enemies_sprites.update(self.world_shift)
        if self.enemies2_flag: 
            self.enemies2_sprites.update(self.world_shift)
        if self.enemies3_flag: 
            self.enemies3_sprites.update(self.world_shift)

        # Draw Player and goal
        self.player.update()
        self.player.draw(self.display_surface)
        self.scroll_x()

        # Collisiton detection
        self.horizontal_movement_collisions()
        self.vertical_movement_collision()
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # Draw Grass
        self.grass_sprites.draw(self.display_surface)
        self.grass_sprites.update(self.world_shift)

        # Draw Sole Coins
        self.sole_coins_sprites.draw(self.display_surface)
        self.sole_coins_sprites.update(self.world_shift)

        # Draw Foreground Palms
        self.fg_plams_sprites.draw(self.display_surface)
        self.fg_plams_sprites.update(self.world_shift)

        # Draw water
        self.water.draw(self.display_surface, self.world_shift)

        # show developer name
        self.display_surface.blit(self.developer_name, (18, 670))

        # Sole coin collide detection
        self.detect_sole_coin_collision()

        # check death
        self.check_death()

        # check player collision with enemy
        self.check_player_collision_with_enemy()

        # check player collision with goal
        self.check_player_collision_with_goal()
