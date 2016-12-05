import pygame
import sys
from pygame_standard.engines import DefaultEngine
from pygame_standard.content_managers import DefaultCM
import time




class Window:
	engines = []
	def __init__(self,size,screens={},screenorder=None):
		if not screenorder:
			screenorder = screens.keys()
		self.surface = pygame.display.set_mode(size)
		self.screens = screens
		self.screenorder = screenorder
		self.reversescreenorder = screenorder[::-1]
		self.content_manager = DefaultCM(screens,self.reversescreenorder)
	def run(self):
		# main loop
		while True:
			self.iterate()
			pygame.time.wait(5)
	def iterate(self):
		# unit cycle
		self.check_events()
		for engine in self.engines:
			engine.iterate()
		self.draw()
	def check_events(self):
		# get events
		if pygame.event.get(pygame.QUIT):
			pygame.quit()
			sys.exit()
		cmevent = self.content_manager.interact()
		for engine in self.engines:
			engine.events(cmevent)
	def draw(self):
		for screen in self.screenorder:
			self.screens[screen].draw(self.surface)
		pygame.display.update()
	def add_screen(self,screen,level=0):
		# adds an interface layer to draw and check mouseclick events against
		self.screens[screen.screen_id]= screen
		screensn = len(self.screens)
		self.screenorder.insert(screensn-level,screen.screen_id)
		self.reversescreenorder.insert(level,screen.screen_id)
	def add_engine(self,engine):
		self.add_screen(engine.get_screen())
		self.engines.append(engine)













