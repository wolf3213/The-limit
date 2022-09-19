import pygame
from tiles import Tile
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos,groups):
        super().__init__(groups)
        #self.image = pygame.image.load('graphics/cat_R.png').convert_alpha()
        #self.image.fill('red')

        self.direction = pygame.math.Vector2(0, 0)
        self.image = pygame.image.load('graphics/cat_R.png').convert_alpha()
        self.animate_player()
        self.rect = self.image.get_rect(center=pos)
        self.speed=8
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
            self.facing_left = True
            self.facing_right = False
        elif self.direction.x>0:
            self.image = pygame.image.load('graphics/cat_R.png').convert_alpha()
            self.facing_right = True
            self.facing_left= True
    def get_input(self,joystick):
        if pygame.joystick.get_count() == 0:#pad not found
            #keybaord only
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
        else:
            #xbox and keyboard
            #axis
            axis_x = joystick.get_axis(0)
            #axis_y = joystick.get_axis(1)
            #print(axis_x)
            #'A" button on xbox controller
            button_jump = joystick.get_button(0)
            keys = pygame.key.get_pressed()
            if (button_jump>0 and self.on_ground):
                self.jump()
            if axis_x > 0.4:
                self.direction.x = 1
                print("right")
            elif axis_x < -0.4:
                self.direction.x = -1
                print("left")
            ##############
            # keyboard
            elif keys[pygame.K_RIGHT]:
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

    def update(self,joystick):
        self.get_input(joystick)
        self.rect.x += self.direction.x * self.speed
        self.animate_player()

