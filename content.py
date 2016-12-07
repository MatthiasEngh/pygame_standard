import pygame
from pygame_standard.cursor import CURSORRELEASED
from pygame_standard.colors import GRAY, BLACK


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




DEFAULT_BUTTON_FONTSIZE = 20
DEFAULT_BUTTON_FONT = None
DEFAULT_BUTTON_AA = 1
DEFAULT_BUTTON_COLOR = BLACK
DEFAULT_BUTTON_BG = GRAY
DEFAULT_BUTTON_ACTIVATED = GRAY
DEFAULT_BUTTON_ACTIVATED_BG = BLACK


class Button(Component):
	def __init__(self,pos,text,buttonID):
		self.font = pygame.font.Font(DEFAULT_BUTTON_FONT,DEFAULT_BUTTON_FONTSIZE)
		self.text = text
		text_surf = self.font.render(self.text,DEFAULT_BUTTON_AA,DEFAULT_BUTTON_COLOR,DEFAULT_BUTTON_BG)
		text_second = self.font.render(self.text,DEFAULT_BUTTON_AA,DEFAULT_BUTTON_ACTIVATED,DEFAULT_BUTTON_ACTIVATED_BG)
		self.rect = text_surf.get_rect()
		self.rect.topleft = pos
		self.images = [text_surf,text_second]*2

		Component.__init__(self,self.rect,self.images[0])
		self.ID = buttonID
	def update(self,update_data):
		cursorstate = update_data["cursorstate"]
		self.image = self.images[cursorstate]
		if cursorstate == CURSORRELEASED:
			return self.ID





