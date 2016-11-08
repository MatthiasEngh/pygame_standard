import pygame
import sys
from pygame_standard.engines import DefaultEngine
from pygame_standard.content_managers import DefaultCM
import time

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)




class Window:
	events = []
	def __init__(self,size,engine = DefaultEngine(),screens=[]):
		self.surface = pygame.display.set_mode(size)
		self.engine = engine
		self.screens = screens
		self.content_manager = DefaultCM(screens)
	def run(self):
		# main loop
		while True:
			self.iterate()
	def iterate(self):
		# unit cycle
		self.check_events()
		self.updates = self.engine.iterate(self.events)
		self.refresh()
	def check_events(self):
		# get events
		if pygame.event.get(pygame.QUIT):
			pygame.quit()
			sys.exit()
		self.content_manager.interact(self.events)
	def refresh(self):
		# refreshes screen
		self.update()
		self.draw()
	def update(self):
		for update in self.updates:
			self.surface.blit(update.surface,po.rect)
	def draw(self):
		for screen in self.screens:
			screen.draw(self.surface)
		pygame.display.update()
	def add_screen(self,screen):
		# adds an interface layer to draw and check mouseclick events against
		self.screens.append(screen)














