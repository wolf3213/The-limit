import pygame
from settings import *
from tiles import Tile
from level import Level
from sys import exit
from player import Player
from game_data import level_0
#init

def main(death_count,kill_player):
    pygame.init()
    #pad initalization
    joystick = None
    if joystick:
        print("joystick package is here")
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print("joystick initialized")
    else:
        joystick=False #look at get_input in player class
        print('joystick not initaliazed')
    #screen
    screen=pygame.display.set_mode((1920,1080),pygame.FULLSCREEN)
    clock=pygame.time.Clock()
    #level
    level=Level(level_0,screen)
    #backround
    pygame.display.set_caption('test game')
    sky_surface = pygame.image.load('graphics/sky.jpg').convert_alpha()
    #fonts
    def_font=pygame.font.Font(None,50)#default font
    text_name=def_font.render("Deathcount "+str(death_count),True,"red")
    running=True
    while running:

        for event in pygame.event.get(): #q
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("escape pressed")
                        pygame.quit()
                        running = False
                        exit()
                    if event.key == pygame.K_r:
                            death_count+=1
                            main(death_count,0)
                if pygame.joystick.get_count() > 0:  # if theres a pad
                    button_exit = joystick.get_button(7)
                    if button_exit > 0:
                        print("escape pressed on pad")
                        pygame.quit()
                        running = False
                        exit()

        screen.blit(sky_surface,(0,0))
        level.run(joystick)
        screen.blit(text_name,(940,50))


        kill_player=level.death(kill_player=0)
        if kill_player==1:
            death_count +=1
            main(death_count,kill_player=0)
        pygame.display.update()

        clock.tick(60)

if __name__ == "__main__":
    main(death_count=0,kill_player=0)