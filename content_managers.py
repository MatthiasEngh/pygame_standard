import pygame
import time
from pygame_standard.cursor import Cursor




class DefaultCM:
	def __init__(self,screens,screenorder):
		self.screens = screens
		self.screenorder = screenorder
		self.cursor = Cursor()
		self.bound = None
	def interact(self):
		if pygame.event.get(pygame.MOUSEMOTION):
			self.cursor.move()
		collided = None
		if self.bound:
			result = self.bound.update({"cursorstate":[self.cursor.clickcheck(),self.cursor.get_pos()]})
			if result:
				if not result['bind']:
					print "releasing element", result['cm_event'][0]
					self.bound = None
				return result['cm_event']
		else:
			for screen in self.screens:
				self.screens[screen].update({"cursorstate":[0,self.cursor.get_pos()]})
			for screenID in self.screenorder:
				collided = self.screens[screenID].interact(self.cursor)
				if collided:
					break
			if collided:
				result = collided.update({"cursorstate":[self.cursor.clickcheck(),self.cursor.get_pos()]})
				if result:
					if result['bind']:
						print "binding element", result['cm_event'][0]
						self.bound = collided
					return result['cm_event']





