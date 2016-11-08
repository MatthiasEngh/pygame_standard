import pygame


class Screen(pygame.sprite.Group):
	def __init__(self):
		pygame.sprite.Group.__init__(self)
	def add_component(self,component):
		self.add([component])


class Component(pygame.sprite.Sprite):
	def __init__(self,rect,image):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = rect
	def update(self,state):
		pass


class Button(Component):
	def __init__(self,rect,images):
		self.images = (images*4)[0:4]
		Component.__init__(self,rect,images[0])
	def update(self,state):
		self.image = self.images[state]



