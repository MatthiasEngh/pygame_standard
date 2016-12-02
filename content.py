import pygame
from pygame_standard.cursor import CURSORRELEASED


class Screen(pygame.sprite.Group):
	def __init__(self,screen_id=""):
		self.screen_id = screen_id
		pygame.sprite.Group.__init__(self)
	def add_component(self,component):
		self.add([component])



class BackgroundSprite(pygame.sprite.Sprite):
	def __init__(self,background_image):
		pygame.sprite.Sprite.__init__(self)
		self.image = background_image
		self.rect = background_image.get_rect()


class BackgroundScreen(Screen):
	def __init__(self,background,screen_id=""):
		Screen.__init__(self,screen_id)
		background_sprite = BackgroundSprite(background)
		self.add_component(background_sprite)



class Component(pygame.sprite.Sprite):
	def __init__(self,rect,image):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = rect
	def update(self,update_data):
		pass


class Button(Component):
	def __init__(self,rect,images,buttonID):
		self.images = (images*4)[0:4]
		Component.__init__(self,rect,images[0])
		self.ID = buttonID
	def update(self,update_data):
		cursorstate = update_data["cursorstate"]
		self.image = self.images[cursorstate]
		if cursorstate == CURSORRELEASED:
			return self.ID



