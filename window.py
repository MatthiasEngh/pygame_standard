import pygame
import sys


BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)




class Window:
	events = []
	def __init__(self,size,core_program):
		self.surface = pygame.display.set_mode(size)
		self.core_program = core_program
	def run(self):
		while True:
			self.iterate()
	def iterate(self):
		self.check_events()
		self.paintobjects = self.core_program.iterate(self.events)
		self.refresh()
	def check_events(self):
		self.events = pygame.event.get()
		for event in self.events:
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
	def refresh(self):
		self.surface.fill(BLACK)
		for po in self.paintobjects:
			self.surface.blit(po.surface,po.rect)
		pygame.display.update()













