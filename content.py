import pygame
from pygame_standard.cursor import CURSORRELEASED, CURSORPRESSED
from pygame_standard.colors import *
import numpy as np


class Form:
	def add(self,component,track_changes=False):
		pass


class PanelGroup(pygame.sprite.LayeredUpdates):
	def __init__(self):
		pygame.sprite.LayeredUpdates.__init__(self)
	def draw(self,surface):
		for panel in self.sprites():
			panel.draw(surface)


class Panel(pygame.sprite.Sprite):
	def __init__(self,pos,size):
		self.components = pygame.sprite.Group()
		self.panels = PanelGroup()
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect(pos,size)
	def add_component(self,component):
		if isinstance(component, Panel):
			self.panels.add(component)
		else:
			self.components.add(component)
	def add_components(self,components):
		for component in components:
			self.add_component(component)
	def interact(self,cursor):
		interacted = pygame.sprite.spritecollideany(cursor,self.panels)
		if not interacted:
			interacted = pygame.sprite.spritecollideany(cursor,self.components)
		return interacted
	def update(self,data):
		self.components.update(data)
		self.panels.update(data)
	def draw(self,surface):
		if hasattr(self,"background"):
			surface.blit(self.background,self.rect.topleft)
		self.components.draw(surface)
		self.panels.draw(surface)



class Screen:
	def __init__(self,**kwargs):
		displayinfo = pygame.display.Info()
		width = displayinfo.current_w
		height = displayinfo.current_h
		self.container =	 Panel((0,0),(width,height))
		if not "screen_id" in kwargs:
			screen_id = None
		else:
			screen_id = kwargs["screen_id"]
		if screen_id is None:
			self.screen_id = ""
		else:
			self.screen_id = screen_id
	def add_component(self,component,panel_id=0):
		self.container.add_component(component)
	def interact(self,cursor):
		interacted = self.container
		while (isinstance(interacted, Panel)):
			interacted = interacted.interact(cursor)
			if isinstance(interacted, Interactible):
				return interacted
	def update(self,data):
		self.container.update(data)
	def draw(self,surface):
		self.container.draw(surface)



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
		self.ID = None
	def update(self,update_data):
		pass
	def get_rect(self):
		return self.rect
	def get_size(self):
		return self.rect.size


class Interactible(Component):
	def __init__(self,rect,image=None):
		Component.__init__(self,rect,image)
	def interact_element(self,update_data):
		return None


def create_event(binding,element_id,cursorstate):
	return {'bind':binding,'element_id':element_id,"cursorstate":cursorstate}


class ClickBinder(Interactible):
	binding = False
	def update(self,update_data):
		self.update_visuals(update_data)
	def interact_element(self,update_data):
		cursorstate = update_data["cursorstate"]
		self.update_visuals(cursorstate)
		if cursorstate[0] == CURSORRELEASED:
			self.binding = False
			cm_event = create_event(self.binding, self.ID, cursorstate[0])
		elif cursorstate[0] == CURSORPRESSED:
			self.binding = True
			cm_event = create_event(self.binding, self.ID, cursorstate[0])
		else:
			cm_event = None
		return cm_event
	def update_visuals(self,cursorstate):
		pass



class Plot(Component):
	def __init__(self,plot_size,plot_pos=(0,0),**kwargs):
		print plot_size
		print plot_pos
		rect = pygame.Rect(plot_pos,plot_size)
		Component.__init__(self,rect)
		self.image.fill(GRAY)


DEFAULT_FONT = None
DEFAULT_FONTSIZE = 20
DEFAULT_FONT_AA = 1
DEFAULT_FONT_COLOR = GRAY
DEFAULT_FONT_BG = None

class Text(Component):
	def __init__(self,pos,font_size,text):
		self.font = pygame.font.Font(DEFAULT_FONT,font_size)
		image = self.font.render(text,DEFAULT_FONT_AA,DEFAULT_FONT_COLOR,DEFAULT_FONT_BG)
		image.set_colorkey(BLACK)
		rect = image.get_rect()
		rect.topleft = pos
		Component.__init__(self,rect,image)



DEFAULT_BUTTON_FONTSIZE = 20
DEFAULT_BUTTON_FONT = None
DEFAULT_BUTTON_AA = 1
DEFAULT_BUTTON_COLOR = BLACK
DEFAULT_BUTTON_BG = GRAY
DEFAULT_BUTTON_ACTIVATED = GRAY
DEFAULT_BUTTON_ACTIVATED_BG = BLACK
DEFAULT_BUTTON_BORDER = GRAY
DEFAULT_BUTTON_BORDER_WIDTH = 1


class Button(Interactible,Panel):
	def __init__(self,pos,text,buttonID,border_width=DEFAULT_BUTTON_BORDER_WIDTH):
		self.text = text
		textElement = Text(pos,DEFAULT_BUTTON_FONTSIZE,text)
		Panel.__init__(self,pos,textElement.get_size())
		self.add_component(textElement)
		self.background = pygame.Surface(self.rect.size)
		border_rect = self.background.get_rect()
		Interactible.__init__(self,self.rect)
		pygame.draw.rect(self.background,DEFAULT_BUTTON_BORDER,border_rect,border_width)
		self.ID = buttonID
	def update_visuals(self,cursorstate):
		pass
	def interact_element(self,data):
		if data['cursorstate'][0] == CURSORRELEASED:
			return return_event(False,self.ID)



DEFAULT_KNOB_RADIUS = 15
DEFAULT_KNOB_DIAMETER = 2* DEFAULT_KNOB_RADIUS
DEFAULT_SLIDER_KNOB_RECT = pygame.Rect((0,0),(DEFAULT_KNOB_DIAMETER,DEFAULT_KNOB_DIAMETER))
DEFAULT_SLIDER_KNOB_SURF = pygame.Surface(DEFAULT_SLIDER_KNOB_RECT.size)
pygame.draw.circle(DEFAULT_SLIDER_KNOB_SURF,BLACK,(DEFAULT_KNOB_RADIUS,DEFAULT_KNOB_RADIUS),DEFAULT_KNOB_RADIUS,DEFAULT_KNOB_RADIUS)
DEFAULT_KNOB_BORDERWIDTH = 4
pygame.draw.circle(DEFAULT_SLIDER_KNOB_SURF,GRAY,(DEFAULT_KNOB_RADIUS,DEFAULT_KNOB_RADIUS),DEFAULT_KNOB_RADIUS,DEFAULT_KNOB_BORDERWIDTH)
DEFAULT_SLIDER_BORDER = 2


class Slider(ClickBinder):
	def __init__(self,start,stop,slider_id,track_changes=False):
		self.value = 0
		self.start = start
		self.stop = stop
		self.v = np.subtract(stop,start)
		self.unit_v = np.divide(self.v,np.linalg.norm(self.v))
		self.size = [abs(stop[0]-start[0])+DEFAULT_KNOB_DIAMETER,abs(stop[1]-start[1])+DEFAULT_KNOB_DIAMETER]
		self.pos = [min(start[0],stop[0])-DEFAULT_KNOB_RADIUS,min(start[1],stop[1])-DEFAULT_KNOB_RADIUS]
		self.rect = pygame.Rect(self.pos,self.size)
		self.draw()
		Component.__init__(self,self.rect,self.image)
		self.ID = slider_id
	def knob_location(self,value):
		posx = self.start[0] + value*(self.stop[0] - self.start[0])
		posy = self.start[1] + value*(self.stop[1]-self.start[1])
		pos = [posx-self.rect.left,posy-self.rect.top]
		return pos
	def update_visuals(self,cursorstate):
		if self.binding:
			self.adjust_value(cursorstate[1])
			self.draw()
	def draw(self):
		self.image = pygame.Surface(self.size)
		pygame.draw.line(self.image,GRAY,self.knob_location(0),self.knob_location(1),DEFAULT_KNOB_RADIUS)
		pygame.draw.line(self.image,BLACK,np.subtract(self.knob_location(0),[0,DEFAULT_SLIDER_BORDER]),np.add(self.knob_location(1),[0,DEFAULT_SLIDER_BORDER]),DEFAULT_KNOB_RADIUS-DEFAULT_SLIDER_BORDER)
		knob_rect = DEFAULT_SLIDER_KNOB_RECT.copy()
		knob_rect.center = self.knob_location(self.value)
		self.image.blit(DEFAULT_SLIDER_KNOB_SURF,knob_rect.topleft)
	def adjust_value(self,cursor_pos):
		mouse_v = np.subtract(cursor_pos,self.start)
		projection = np.matmul(mouse_v,np.outer(self.unit_v,self.unit_v))
		n_proj = np.divide(np.sqrt(projection.dot(projection)),np.sqrt(self.v.dot(self.v)))
		dp = mouse_v.dot(self.v)
		s_proj = dp/abs(dp)*n_proj
		result = max(min(s_proj,1),0)
		self.value = result



class VerticalSlider(Slider):
	def __init__(self,pos,height,slider_id):
		start = list(pos)
		start[1] = start[1] + height
		stop = list(pos)
		Slider.__init__(self,start,stop,slider_id)



class HorizontalSlider(Slider):
	def __init__(self,pos,width):
		start = list(pos)
		stop = list(pos)
		stop[0] = start[0] + width
		Slider.__init__(self,start,stop,slider_id)



DEFAULT_SLIDER_ARRAY_SPACING = 10

class VerticalSliderArray(Panel):
	def __init__(self,pos,height,count,slider_array_id):
		new_sliders = []
		spos = list(pos)
		for i in range(count):
			new_slider = VerticalSlider(spos,height,slider_array_id+"_"+str(i))
			new_sliders.append(new_slider)
			spos[0] = new_slider.rect.right + DEFAULT_KNOB_RADIUS + DEFAULT_SLIDER_ARRAY_SPACING
		size = np.subtract(new_slider.rect.bottomright,pos)
		Panel.__init__(self,pos,size)
		self.add_components(new_sliders)




