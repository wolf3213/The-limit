import pygame
from tiles import Tile
from settings import *
from player import Player
class Level:
	def __init__(self,level_data,surface):
		self.display_surface=surface
		self.setup_level(level_data)

		self.world_shift=0


	def setup_level(self,layout):
		self.tiles = CameraGroup()
		self.winds_up= CameraGroup()
		self.winds_left = CameraGroup()
		self.player = pygame.sprite.GroupSingle()
		for row_index, row in enumerate(layout):
			for col_index, cell in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size

				if cell == 'X':
					tile = Tile((x, y), tile_size,'grey')
					self.tiles.add(tile)
				if cell == 'P':
					player_sprite = Player((x, y))
					self.player.add(player_sprite)
				if cell == 'W':
					wind_up = Tile((x, y), tile_size,'white')
					self.winds_up.add(wind_up)
				if cell == 'A':
					wind_left = Tile((x, y), tile_size,'white')
					self.winds_left.add(wind_left)

	def horizontal_movement_collision(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0:
					player.rect.left = sprite.rect.right
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
	def vertical_movement_collision(self):
		player = self.player.sprite
		player.apply_gravity()

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0:
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0.1:
			player.on_ceiling = False
		for sprite in self.winds_up.sprites():
			if sprite.rect.colliderect(player.rect):
					player.direction.y = -3
		for sprite in self.winds_left.sprites():
			if sprite.rect.colliderect(player.rect):
					player.direction.x = -8
					player.direction.y = -0.9

	def get_player_on_ground(self):
		if self.player.sprite.on_ground:
			self.player_on_ground = True
		else:
			self.player_on_ground = False




	def death(self,kill_player):
		player = self.player.sprite
		player_y = player.rect.centery
		#print(player.rect.y)
		if player_y>1100:
			kill_player +=1
			print(kill_player)
			return kill_player


	def run(self):
		player = self.player.sprite
		self.tiles.custom_draw(player)
		self.winds_up.custom_draw(player)
		self.winds_left.custom_draw(player)

		#self.scroll_x()
		self.player.update()
		self.get_player_on_ground()
		self.horizontal_movement_collision()
		self.vertical_movement_collision()
		self.player.draw(self.display_surface)


class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2(0,0)

		#center camera setup
		self.half_w = self.display_surface.get_size()[0] // 2
		self.half_h = self.display_surface.get_size()[1] // 2

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
