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

        #self.world_shift=0
        self.collison_tollorence=3

        self.visible_sprites = CameraGroup()
        self.active_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        tiles_layout = import_csv_layout(level_data['terrain'])
        self.tiles = self.create_tile_group(tiles_layout,'terrain',[self.visible_sprites,self.collision_sprites])
        winds_laylout = import_csv_layout(level_data['winds'])
        self.winds = self.create_tile_group(winds_laylout, 'winds', [self.visible_sprites, self.collision_sprites])

        # TO FIX
        # self.winds_up= pygame.sprite.Group()
        # self.winds_left = pygame.sprite.Group()
        # self.platforms = pygame.sprite.Group()
        # player
        player_layout = import_csv_layout(level_data['player'])
       #self.player = pygame.sprite.GroupSingle()
        self.player_setup(player_layout,self.visible_sprites)


    def create_tile_group(self, layout, type, groups):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        #terrain_tile_list = import_cut_graphics('graphics/stone.png')
                        #tile_surface = terrain_tile_list[int(val)]
                        sprite = Tile((x,y),tile_size, 'grey',groups)
                    if type == 'winds':
                        sprite = Tile((x, y), tile_size, 'white', groups)
                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout,groups):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    self.player = Player((x, y),groups)
                    #self.player.add(sprite)


    # def winds_collisions(self):
    #     player = self.player.sprite
    #     for sprite in self.winds_up.sprites():
    #         if sprite.rect.colliderect(player.rect):
    #                 player.direction.y = -1.3 #ponieważ potrzebujesz zapasu 4 pixeli na doskoczenie do platformy
    #                 #player.gravity=0
    #                 #print(player.direction.y)
    #         #else:
    #             #player.gravity=0.9
    #     for sprite in self.winds_left.sprites():
    #         if sprite.rect.colliderect(player.rect):
    #                 player.direction.x = -1
    #                 player.direction.y = -0.3

    def horizontal_movement_collision(self):
        player = self.player

        for sprite in self.collision_sprites.sprites():
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
        player = self.player
        player.apply_gravity()
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

        for sprite in self.collision_sprites.sprites():
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

    #TO FIX
    # def platforms_collisions(self):
    #     player = self.player.sprite
    #     for sprite in self.platforms.sprites():
    #         if (sprite.rect.colliderect(player.rect)):
    #             if  player.direction.y > 0:
    #                 player.rect.bottom = sprite.rect.top
    #                 player.direction.y = 0
    #                 player.on_ground = True




    def get_player_on_ground(self):
        if self.player.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False





    def death(self,kill_player):
        player = self.player
        player_y = player.rect.centery
        #print(player.rect.y)
        if player_y>1081:
            kill_player +=1
            #print(kill_player)
            return kill_player


    def run(self,joystick):

        #self.scroll_x()
        #self.tiles.update(self.world_shift)
        self.visible_sprites.custom_draw(self.player)
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
        #self.player.draw(self.display_surface)

class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2(0,0)

		# center camera setup
		# self.half_w = self.display_surface.get_size()[0] // 2
		# self.half_h = self.display_surface.get_size()[1] // 2

		# camera
		cam_left = CAMERA_BORDERS['left']
		cam_top = CAMERA_BORDERS['top']
		cam_width = self.display_surface.get_size()[0] - (cam_left + CAMERA_BORDERS['right'])
		cam_height = self.display_surface.get_size()[1] - (cam_top + CAMERA_BORDERS['bottom'])

		self.camera_rect = pygame.Rect(cam_left,cam_top,cam_width,cam_height)

	def custom_draw(self,player):

		# get the player offset
		# self.offset.x = player.rect.centerx - self.half_w
		# self.offset.y = player.rect.centery - self.half_h

		# getting the camera position
		if player.rect.left < self.camera_rect.left:
			self.camera_rect.left = player.rect.left
		if player.rect.right > self.camera_rect.right:
			self.camera_rect.right = player.rect.right
		if player.rect.top < self.camera_rect.top:
			self.camera_rect.top = player.rect.top
		if player.rect.bottom > self.camera_rect.bottom:
			self.camera_rect.bottom = player.rect.bottom

		# camera offset
		self.offset = pygame.math.Vector2(
			self.camera_rect.left - CAMERA_BORDERS['left'],
			self.camera_rect.top - CAMERA_BORDERS['top'])

		for sprite in self.sprites():
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)