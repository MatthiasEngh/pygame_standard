import pygame



class DefaultPainter:
	def __init__(self, colorarray):
		self.colorarray = colorarray
	def draw(self):
		self.drawnmap = pygame.surfarray.make_surface(self.maparray)
		return self.drawnmap
	def get_map(self):
		return self.drawnmap



class HeightPainter(DefaultPainter):
	def __init__(self,heightmap,colormap):
		self.heightmap = heightmap
		self.colormap = colormap
		self.draw()



class QualityPainter(DefaultPainter):
	def __init__(self,qualitymap,colormap):
		self.qualitymap = qualitymap
		self.colormap = colormap



