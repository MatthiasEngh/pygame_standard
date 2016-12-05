import pygame
from pygame_standard.cursor import CURSORRELEASED
from pygame_standard.colors import GRAY


class Screen(pygame.sprite.Group):
	def __init__(self,**kwargs):
		if not "screen_id" in kwargs:
			screen_id = None
		else:
			screen_id = kwargs["screen_id"]
		if screen_id is None:
			self.screen_id = ""
		else:
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
	def __init__(self,rect,image=None):
		pygame.sprite.Sprite.__init__(self)
		self.rect = rect
		if image is None:
			self.image = pygame.Surface(self.rect.size)
		else:
			self.image = image
	def update(self,update_data):
		pass


class Plot(Component):
	def __init__(self,plot_size,plot_pos=(0,0),**kwargs):
		rect = pygame.Rect(plot_pos,plot_size)
		Component.__init__(self,rect)
		self.image.fill(GRAY)


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



