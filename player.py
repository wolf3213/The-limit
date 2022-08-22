import pygame
from tiles import Tile
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        #self.image = pygame.image.load('graphics/cat_R.png').convert_alpha()
        #self.image.fill('red')

        self.direction = pygame.math.Vector2(0, 0)
        self.image = pygame.image.load('graphics/cat_R.png').convert_alpha()
        self.animate_player()
        self.rect = self.image.get_rect(center=pos)
        self.speed=3
        self.gravity=0.9
        self.jump_speed=-12

        # player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def animate_player(self):
        if self.direction.x<0:
            self.image = pygame.image.load('graphics/cat_L.png').convert_alpha()
            self.facing_right = True
        elif self.direction.x>0:
            self.image = pygame.image.load('graphics/cat_R.png').convert_alpha()
            self.facing_right = False
    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        if (keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]):
                self.direction.x = 0
        if (keys[pygame.K_SPACE] and self.on_ground):
            self.jump()

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y


    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.animate_player()

