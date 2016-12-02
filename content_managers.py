import pygame
import time
from pygame_standard.cursor import Cursor




class DefaultCM:
	def __init__(self,screens,screenorder):
		self.screens = screens
		self.screenorder = screenorder
		self.cursor = Cursor()
	def interact(self):
		if pygame.event.get(pygame.MOUSEMOTION):
			self.cursor.move()
		collided = None
		for screen in self.screens:
			self.screens[screen].update({"cursorstate":0})
		for screenID in self.screenorder:
			collided = pygame.sprite.spritecollideany(self.cursor,self.screens[screenID])
			if collided:
				break
		if collided:
			return collided.update({"cursorstate":self.cursor.clickcheck()})





