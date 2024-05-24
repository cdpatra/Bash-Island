import pygame
from support import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface):
        super().__init__()
        self.import_character_assets()
        self.display_surface = surface
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = pygame.Surface((64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2((0, 0))

        # player movement
        self.speed = 6
        self.gravity = 0.8
        self.jump_speed = -16

        # dust particles
        self.import_dust_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15

        # player status
        self.status = 'idle'
        self.facing_right = True
        self.collide_on_floor = False
        self.collide_on_ceiling = False
        self.collide_on_right = False
        self.collide_on_left = False

        # sounds
        self.jump_sound=pygame.mixer.Sound('./resources/sound/jump.wav')
        self.jump_sound.set_volume(0.15)

    def animate(self):
        self.get_status()
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        # set the rect
        if self.collide_on_floor and self.collide_on_right:
            self.rect = self.image.get_rect(bottomright=(self.rect.bottomright))
        elif self.collide_on_floor and self.collide_on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.collide_on_floor:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.collide_on_ceiling and self.collide_on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.collide_on_ceiling and self.collide_on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.collide_on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)
        else:
            self.rect = self.image.get_rect(center=self.rect.center)

    def animate_dust_particles(self):
        self.dust_frame_index += self.dust_animation_speed
        if self.status == 'run':
            if self.dust_frame_index >= len(self.run_dust_particles):
                self.dust_frame_index = 0

            dust_particle_surface = self.run_dust_particles[int(
                self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(20, 26)  # offset
                self.display_surface.blit(dust_particle_surface, pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(50, 26)  # offset
                flipped_dust_particles = pygame.transform.flip(
                    dust_particle_surface, True, False)
                self.display_surface.blit(flipped_dust_particles, pos)

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        elif self.direction.x != 0:
            self.status = 'run'
        else:
            self.status = 'idle'

    def import_character_assets(self):
        path = './resources/player/'
        self.animations = {'idle': [], 'jump': [], 'fall': [], 'run': []}
        for file in self.animations.keys():
            full_path = path + file
            self.animations[file] = import_folder(full_path)

    def import_dust_particles(self):
        self.run_dust_particles = import_folder(
            './resources/player/dust particles/run')

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        elif (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.direction.y == 0:
            self.jump()
        else:
            self.direction.x = 0

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.jump_sound.play()

    def update(self):
        self.get_input()
        self.animate()
        self.animate_dust_particles()
