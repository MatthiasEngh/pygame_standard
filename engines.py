import time
import pygame
from pygame_standard.content import Screen


class DefaultEntityManager:
	def __init__(self,entities=pygame.sprite.Group()):
		self.entities = entities
	def iterate(self,fields):
		self.entities.update({"fields":fields})
	def add_entity(self,entity):
		self.entities.add(entity)


class Field:
	def __init__(self,id,init_data=None):
		self.data = init_data
		self.id = id
		self.version = 0
	def has_changed(self,version):
		return not self.version == version
	def get_id(self):
		return self.id
	def get_version(self):
		return self.version
	def update(self,data):
		self.data = data
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
	def respond(self,event):
		event_id = event['element_id']
		if event_id in self.responses:
			field_id = self.responses[event_id]['field']
			response = self.responses[event_id]['response']
			data = None
			if 'form_data' in event:
				data = event['form_data']
			result = response(self.fields[field_id],data)
			if result is not None:
				self.fields[field_id].update(result)
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
		return self.fields_m.return_formdata() # engines needs to compile form data since here different fields should be accessed ... this will throw an error now
	def events(self,cmevent):
		if cmevent:
			self.fields_m.respond(cmevent)
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
	def events(self,cmevent):
		if cmevent:
			self.fields_m.respond(cmevent)
		else:
			for event in pygame.event.get(pygame.KEYDOWN):
				self.fields_m.respond(event.key)







