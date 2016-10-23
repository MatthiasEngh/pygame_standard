


class DefaultEntity:
	def __init__(self,pos):
		self.pos = pos
	def move_to(self,pos):
		self.pos = pos
	def move_to_x(self,x):
		self.pos[0] = x
	def move_to_y(self,y):
		self.pos[1] = y
	def move(self,movement):
		self.pos += movement


