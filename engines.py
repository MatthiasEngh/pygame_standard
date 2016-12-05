import time
import pygame
from pygame_standard.content import Screen
import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab



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


class DefaultEntityManager:
	def __init__(self,entities=pygame.sprite.Group()):
		self.entities = entities
	def iterate(self,fields):
		self.entities.update({"fields":fields})
	def add_entity(self,entity):
		self.entities.add(entity)


class Field:
	def __init__(self,id):
		self.id = id
		self.version = 0
	def has_changed(self,version):
		return not self.version == version
	def get_id(self):
		return self.id
	def get_version(self):
		return self.version
	def update(self):
		self.version += 1



class ArrayField(Field):
	def __init__(self,id,array):
		Field.__init__(self,id)
		self.array = array
	def get_plotdata(self):
		return self.array
	def update(self,array):
		self.array = array
		Field.update(self)


class DefaultFieldManager:
	def __init__(self,fields={},responses = {}):
		self.fields = fields
		self.responses = responses
	def get_fields(self):
		return self.fields
	def respond(self,event,data):
		if event in self.responses:
			self.fields[self.responses[event]['field']].update(self.responses[event]['response'](self.fields[self.responses[event]['field']]))
		else:
			print "event type %s has no response" % event
	def add_response(self,event_id,response_fn,field_id):
		self.responses[event_id] = {'response':response_fn,'field':field_id}
	def add_field(self,field):
		self.fields[field.get_id()] = field
	def add_fields(self,fields):
		for field in fields:
			self.add_field(field)






class DefaultEngine:
	def __init__(self,fields = {},responses = {},entities = pygame.sprite.Group(),screen_id=None,**kwargs):
		self.screen = Screen(screen_id=screen_id,**kwargs)
		self.entity_m = DefaultEntityManager(entities)
		self.fields_m = DefaultFieldManager(fields,responses)
	def iterate(self):
		self.entity_m.iterate(self.fields_m.get_fields())
	def events(self,cmevent,data=None):
		if cmevent:
			self.fields_m.respond(cmevent,data)
	def get_screen(self):
		return self.screen
	def add_entity(self,entity):
		self.screen.add_component(entity)
		self.entity_m.add_entity(entity)
	def add_field(self,field):
		self.fields_m.add_field(field)
	def add_response(self,event_id,response_fn,field_id):
		self.fields_m.add_response(event_id,response_fn,field_id)
	def add_fields(self,fields):
		self.fields_m.add_fields(fields)
	def get_screen(self):
		return self.screen


class ExampleEngine(DefaultEngine):
	def __init__(self,**kwargs):
		DefaultEngine.__init__(self,**kwargs)
	def iterate(self):
		# check events and walk program state
		self.entity_m.iterate(self.fields_m.get_fields())
		return []
	def events(self,cmevent,data = None):
		if cmevent:
			self.fields_m.respond(cmevent,data)
		else:
			for event in pygame.event.get(pygame.KEYDOWN):
				self.fields_m.respond(event.key)




class MatplotlibEngine(DefaultEngine):
	def __init__(self,screen_id,plot_size,data_field,**kwargs):
		DefaultEngine.__init__(self,screen_id=screen_id)
		plot = Plot(plot_size,data_field,**kwargs)
		self.add_entity(plot)
		self.add_field(data_field)
		self.iterate()



