import pygame
import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab
from pygame_standard.engines import DefaultEngine
from pygame_standard.entities import Entity


class Plot(Entity):
	def __init__(self,size,plot_data,**kwargs):
		image = pygame.Surface(size)
		image.fill((255,100,0))
		if "plot_pos" in kwargs:
			Entity.__init__(self,image,pos=kwargs["plot_pos"])
		else:
			Entity.__init__(self,image)
		figwidth = 4
		figheight = 4
		self.fig = pylab.figure(figsize=[figwidth, figheight],
		                   dpi=100,
		                   )
		self.update_pldv(plot_data)
		self.plot(plot_data)
	def update(self,update_data):
		if "fields" in update_data:
			plot_data = update_data["fields"]["plot_data"]
			if plot_data.has_changed(self.pldv):
				self.update_pldv(plot_data)
				self.plot(plot_data)
	def plot(self,plot_data):
		ax = self.fig.gca()
		ax.clear()
		ax.plot(plot_data.get_plotdata())
		canvas = agg.FigureCanvasAgg(self.fig)
		canvas.draw()
		renderer = canvas.get_renderer()
		raw_data = renderer.tostring_rgb()
		size = canvas.get_width_height()	 
		plotsurf = pygame.image.fromstring(raw_data, size, "RGB")
		self.image.blit(plotsurf, (0,0))
	def update_pldv(self,plot_data):
		self.pldv = plot_data.get_version()


class MatplotlibEngine(DefaultEngine):
	def __init__(self,screen_id,plot_size,data_field,**kwargs):
		DefaultEngine.__init__(self,screen_id=screen_id)
		plot = Plot(plot_size,data_field,**kwargs)
		self.add_entity(plot)
		self.add_field(data_field)
		self.iterate()
