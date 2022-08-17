import pygame

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,size,colour):
		super().__init__()
		self.image = pygame.Surface((size,size))
		self.image.fill(colour)
		self.rect = self.image.get_rect(topleft = pos)

	def update(self,x_shift):
		self.rect.x += x_shift

