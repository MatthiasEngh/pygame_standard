import pygame
import time
from pygame_standard.cursor import Cursor




class DefaultCM:
	def __init__(self,screens,screenorder):
		self.screens = screens
		self.cursor = Cursor()
		self.bound = None
	def interact(self):
		if pygame.event.get(pygame.MOUSEMOTION):
			self.cursor.move()
		self.cursor.clickcheck()
		interactible = None
		if self.bound:
			return self.interact_element(self.bound)
		else:
			interactible = self.hover_and_release()
			if interactible:
				return self.interact_element(interactible)

	def hover_and_release(self):
		interactible = None
		for screen in self.screens:
			self.screens[screen].update({"cursorstate":[0,self.cursor.get_pos()]})
			if not interactible:
				interactible = self.screens[screen].interact(self.cursor)
		return interactible
	def interact_element(self,interactible):
		result = interactible.interact_element({"cursorstate":[self.cursor.get_state(),self.cursor.get_pos()]})
		if result:
			if result['bind']:
				self.bound = interactible
			else:
				self.bound = None
			return {'components':[result['element_id']],result['element_id']:result['value']}





