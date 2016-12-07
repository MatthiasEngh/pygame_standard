import pygame




class Entity(pygame.sprite.Sprite):
	def __init__(self,image=None,pos=None):
		pygame.sprite.Sprite.__init__(self)
		if not image:
			self.image = pygame.Surface((1,1))
		else:
			self.image = image
		self.rect = self.image.get_rect()
		if pos:
			self.rect.topleft = pos
	def update(self,update_data):
		if "fields" in update_data:
			fields = update_data["fields"]
			self.rect.top += fields["yfield"]
			self.rect.left += fields["xfield"]
