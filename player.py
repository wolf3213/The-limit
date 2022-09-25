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
        self.rect = self.image.get_rect(topleft=pos)
        #defualts values
        self.default_speed=6
        self.default_gravity=0.9
        self.default_jump_speed=-12
        #asigning those values
        self.speed = self.default_speed
        self.gravity=self.default_gravity
        self.jump_speed=self.default_jump_speed

        # player status
        self.status = 'idle'

        self.facing_right = True
        self.facing_left = False
        self.on_ground = False
        self.on_ceiling = False

        #dash
        self.can_dash = True
        self.dash_start_time = 0
        self.dash_duration_time= 230
        self.dash_state=False
        self.dash_cooldown = 50
        self.dash_speed=10
        self.dash_can_choose_direction=True


    def animate_player(self):
        if self.direction.x<0:
            self.image = pygame.image.load('graphics/cat_L.png').convert_alpha()
            self.facing_left = True
            self.facing_right = False
        elif self.direction.x>0:
            self.image = pygame.image.load('graphics/cat_R.png').convert_alpha()
            self.facing_right = True
            self.facing_left= True
    def dash(self,keys): #function which makes dashes NOT FINISHED
        current_time = pygame.time.get_ticks()

        if keys[pygame.K_LSHIFT] and self.can_dash:
            self.dash_start_time = pygame.time.get_ticks()
            self.dash_state = True
            self.can_dash = False
        if self.dash_state:
            if self.dash_can_choose_direction==True:
                if keys[pygame.K_RIGHT] and not keys[pygame.K_UP]:
                    self.direction.x = 1
                elif keys[pygame.K_LEFT] and not keys[pygame.K_UP]:
                    self.direction.x = -1
                elif keys[pygame.K_UP]:
                    self.direction.y = -1
                elif keys[pygame.K_DOWN]:
                    self.direction.y = 1
                elif self.facing_right == True:
                    self.direction.x = 1
                elif self.facing_left== True:
                    self.direction.x = -1
                self.speed = self.dash_speed
                self.gravity = 0
        self.dash_can_choose_direction = False
        if current_time - self.dash_start_time >= self.dash_duration_time:  # if time of dash ends, end dash
            self.gravity=self.default_gravity
            if self.on_ground:
                self.speed = self.default_speed
                self.can_dash=True
                self.dash_can_choose_direction = True
                self.dash_state = False




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
            elif self.dash_state==False:
                self.direction.x = 0

            if (keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]):
                self.direction.x = 0
            if (keys[pygame.K_SPACE] and self.on_ground):
                self.jump()
            self.dash(keys)

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
            elif axis_x < -0.4:
                self.direction.x = -1
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
            elif self.dash_state == False:
                self.direction.x = 0

            if (keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]):
                self.direction.x = 0
            if (keys[pygame.K_SPACE] and self.on_ground):
                self.jump()
            self.dash(keys)



    def dash_cooldown(self):
        current_time = pygame.time.get_ticks()
        if self.dash_state==False:
            if current_time - self.dash_start_time >= self.dash_cooldown:
                self.can_dash = True
                #print("cooldown_rested")


    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        if self.dash_state==True:
            self.rect.y += self.direction.y*self.speed


    def jump(self):
        self.direction.y = self.jump_speed

    def movement (self):
        self.rect.x += self.direction.x * self.speed
    def update(self,joystick):
        self.get_input(joystick)
        self.movement()
        self.animate_player()

