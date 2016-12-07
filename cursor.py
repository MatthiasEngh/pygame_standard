import pygame

CURSORIDLE = 1
CURSORPRESSED = 2
CURSORRELEASED = 3


class Cursor(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect((0,0),(1,1))
		self.rect.topleft = pygame.mouse.get_pos()
		self.state = CURSORIDLE
	def move(self):
		self.rect.topleft = pygame.mouse.get_pos()
	def clickcheck(self):
		if self.state == CURSORRELEASED:
			self.state = CURSORIDLE
		if pygame.event.get(pygame.MOUSEBUTTONDOWN):
			self.state = CURSORPRESSED
		if pygame.event.get(pygame.MOUSEBUTTONUP):
			self.state = CURSORRELEASED
		return self.state
	def get_state(self):
		return self.state
	def get_pos(self):
		return self.rect.topleft

