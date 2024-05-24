from tiles import *
from random import randint


class Enemy(Animated_Tile):
    def __init__(self, size, x, y,path):
        super().__init__(size, x, y, path)
        self.rect.y += 20
        self.speed = randint(1, 3)

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse_motion(self):
        self.speed *= -1

    def update(self, shift):
        self.move()
        self.animate()
        self.reverse_image()
        self.rect.x += shift

class Static_Enemy(Animated_Tile):
    def __init__(self,size,x,y,path):
        super().__init__(size,x,y,path)

    def update(self,shift):
        self.animate()
        self.rect.x += shift
