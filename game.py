import pygame
from settings import *
from tiles import Tile
from level import Level
from sys import exit
from player import Player
from game_data import level_0
clock = pygame.time.Clock()
#init
#kill player==0 if player alive kill player==1 if player is dying

class Game():
    def __init__(self,joystick):
#         super().__init__()
        self.joystick=joystick
        #screen
        self.screen=pygame.display.set_mode((1920,1080),pygame.FULLSCREEN)
        self.clock=pygame.time.Clock()
        #level
        self.level=Level(level_0,self.screen)
        #backround
        pygame.display.set_caption('test game')
        self.sky_surface = pygame.image.load('graphics/sky.jpg').convert_alpha()
        #fonts
        self.def_font=pygame.font.Font(None,50)#default font

        self.running=True

    def run(self,death_count):
        self.text_name = self.def_font.render("Deathcount " + str(death_count), True, "red")
        while self.running:

            for event in pygame.event.get(): #q
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            print("escape pressed")
                            pygame.quit()
                            self.running = False
                            exit()
                        if event.key == pygame.K_r:
                                death_count+=1
                                game = Game(self.joystick)
                                self.running = False # i am not sure if that's needed
                                game.run(death_count)
                    if pygame.joystick.get_count() > 0:  # if theres a pad
                        button_exit = self.joystick.get_button(7)
                        if button_exit > 0:
                            print("escape pressed on pad")
                            pygame.quit()
                            self.running = False
                            exit()

            self.screen.blit(self.sky_surface,(0,0))
            self.level.run(self.joystick)
            self.screen.blit(self.text_name,(940,50))


            kill_player=self.level.death(0)
            #print(kill_player)
            if kill_player==1:
                death_count +=1
                self.running = False # i am not sure if that's needed
                game = Game(self.joystick)
                game.run(death_count)
            pygame.display.update()
            #print(death_count)


            self.clock.tick(60)
            #print(self.clock.get_fps())


if __name__ == "__main__":
    pygame.init()
    # pad initalization
    joystick = None
    if joystick:
        print("joystick package is here")
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print("joystick initialized")
    else:
        joystick = False  # look at get_input in player class
        print('joystick not initaliazed')
    game = Game(joystick)
    game.run(death_count=0)
    # main(death_count=0,kill_player=0)