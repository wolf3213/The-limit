import pygame

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,size,colour,groups):
		super().__init__(groups)
		self.image = pygame.Surface((size,size))
		self.image.fill(colour)
		self.rect = self.image.get_rect(topleft = pos)

	def update(self,x_shift):
		self.rect.x += x_shift
class Wind_(pygame.sprite.Sprite):
	def __init__(self,pos,direction_wind,groups):
		super().__init__(groups)
		self.direction_wind=direction_wind
		if self.direction_wind=='up':
			self.image = pygame.image.load('graphics/arrow_up.png').convert_alpha()
		elif self.direction_wind=='right':
			self.image = pygame.image.load('graphics/arrow.png').convert_alpha()
		self.rect = self.image.get_rect(topleft=pos)



class Platform_(pygame.sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		self.image = pygame.image.load('graphics/platform_3.png').convert_alpha()
		self.rect = self.image.get_rect(topleft=pos)
	def update(self, x_shift):
		self.rect.x += x_shift