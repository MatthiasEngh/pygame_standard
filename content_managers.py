import pygame


CURSORIDLE = 1
CURSORCLICKED = 2
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
			self.state = CURSORCLICKED
		if pygame.event.get(pygame.MOUSEBUTTONUP):
			self.state = CURSORRELEASED
		return self.state
	def get_state(self):
		return self.state




class DefaultCM:
	def __init__(self,screens):
		self.screens = screens
		self.cursor = Cursor()
	def interact(self,events):
		if pygame.event.get(pygame.MOUSEMOTION):
			self.cursor.move()
		collided = None
		for screen in self.screens:
			if screen:
				collided = pygame.sprite.spritecollideany(self.cursor,screen)
			if collided:
				print collided
		if collided:
			collided.update(self.cursor.clickcheck())
		else:
			for screen in self.screens:
				screen.update(0)
		return None





