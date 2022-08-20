import pygame

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,size,colour):
		super().__init__()
		self.image = pygame.Surface((size,size))
		self.image.fill(colour)
		self.rect = self.image.get_rect(topleft = pos)

	def update(self,x_shift):
		self.rect.x += x_shift
class Wind_(pygame.sprite.Sprite):
	def __init__(self,pos):
		super().__init__()
		self.image = pygame.image.load('graphics/wind.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)

	def update(self,x_shift):
		self.rect.x += x_shift
class Windleft_(pygame.sprite.Sprite):
	def __init__(self,pos):
		super().__init__()
		self.image = pygame.image.load('graphics/wind_left.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)

	def update(self,x_shift):
		self.rect.x += x_shift
class Platform_(pygame.sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		self.image = pygame.image.load('graphics/platform_3.png').convert_alpha()
		self.rect = self.image.get_rect(topleft=pos)
	def update(self, x_shift):
		self.rect.x += x_shift