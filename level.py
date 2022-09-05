import pygame
from tiles import Tile
from tiles import Platform_
from tiles import Wind_
from tiles import Windleft_
from settings import *
from player import Player
from support import import_csv_layout, import_cut_graphics


class Level:
    def __init__(self,level_data,surface):
        self.display_surface=surface

        self.world_shift=0
        self.collison_tollorence=3

        tiles_layout = import_csv_layout(level_data['terrain'])
        self.tiles = self.create_tile_group(tiles_layout,'terrain')
        self.winds_up= pygame.sprite.Group()
        self.winds_left = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        # player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)
        #for row_index, row in enumerate(layout):
            #for col_index, cell in enumerate(row):
                #x = col_index * tile_size
                #y = row_index * tile_size

                #if cell == 'X':
                    #tile = Tile((x, y), tile_size,'grey')
                    #self.tiles.add(tile)
                #if cell == 'P':
                    #player_sprite = Player((x, y))
                    #self.player.add(player_sprite)
               # if cell == 'W':
                    #wind_up = Wind_((x, y))
                    #self.winds_up.add(wind_up)
                #if cell == 'A':
                    #wind_left = Windleft_((x, y))
                    #self.winds_left.add(wind_left)
                #if cell == 'G':
                    #platform = Platform_((x, y+88))
                    #self.platforms.add(platform)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        #terrain_tile_list = import_cut_graphics('graphics/stone.png')
                        #tile_surface = terrain_tile_list[int(val)]
                        sprite = Tile( (x,y),tile_size, 'grey')

                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x, y))
                    self.player.add(sprite)


    def winds_collisions(self):
        player = self.player.sprite
        for sprite in self.winds_up.sprites():
            if sprite.rect.colliderect(player.rect):
                    player.direction.y = -1.3 #ponieważ potrzebujesz zapasu 4 pixeli na doskoczenie do platformy
                    #player.gravity=0
                    #print(player.direction.y)
            #else:
                #player.gravity=0.9
        for sprite in self.winds_left.sprites():
            if sprite.rect.colliderect(player.rect):
                    player.direction.x = -1
                    player.direction.y = -0.3

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                # if abs(player.rect.left - sprite.rect.right)<self.collison_tollorence:
                #     player.rect.left = sprite.rect.right
                # elif abs(player.rect.right - sprite.rect.left)<self.collison_tollorence:
                #     player.rect.right = sprite.rect.left
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                    #print("collision with ground")
                elif abs(player.rect.bottom - sprite.rect.top)<self.collison_tollorence:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
                elif abs(player.rect.top - sprite.rect.bottom)<self.collison_tollorence:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
                    #print("collision with celling")
                #elif player.direction.y == 0:
                    #break
    def platforms_collisions(self):
        player = self.player.sprite
        for sprite in self.platforms.sprites():
            if (sprite.rect.colliderect(player.rect)):
                if  player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True




    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False



    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0

    def death(self,kill_player):
        player = self.player.sprite
        player_y = player.rect.centery
        #print(player.rect.y)
        if player_y>1100:
            kill_player +=1
            #print(kill_player)
            return kill_player


    def run(self,joystick):

        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()
        #self.winds_up.update(self.world_shift)
        #self.winds_left.update(self.world_shift)
        #self.winds_left.draw(self.display_surface)
        #self.platforms.update(self.world_shift)
        #self.platforms.draw(self.display_surface)



        #player = self.player.sprite
        #if (player.direction.y>9 or player.direction.y<-9 or player.direction.x>9 or player.direction.x<-9):
            #print(player.direction.x)
            #print(player.direction.y)
        self.player.update(joystick)
        self.get_player_on_ground()
        ##self.winds_collisions()


        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        #self.platforms_collisions()
        self.player.draw(self.display_surface)

