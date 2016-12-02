import time
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

class DefaultEntityManager:
	def __init__(self,entities=pygame.sprite.Group()):
		self.entities = entities
	def iterate(self,fields):
		self.entities.update({"fields":fields})
	def add_entity(self,entity):
		self.entities.add(entity)


class DefaultFieldManager:
	def __init__(self,fields={},responses = {}):
		self.fields = fields
		self.responses = responses
	def get_fields(self):
		return self.fields
	def respond(self,event):
		if event in self.responses:
			self.fields[self.responses[event]['field']] = self.responses[event]['response'](self.fields[self.responses[event]['field']])
		else:
			print "event type %s has no response" % event
	def add_response(self,event_id,response_fn,field_id):
		self.responses[event_id] = {'response':response_fn,'field':field_id}
	def add_field(self,field):
		self.fields[field['fid']] = field['val']
	def add_fields(self,fields):
		for field in fields:
			self.add_field(field)


class DefaultEngine:
	def __init__(self,fields = {},responses = {},entities = pygame.sprite.Group(),screens = {}):
		self.fields_m = DefaultFieldManager(fields,responses)
		self.entity_m = DefaultEntityManager(entities)
		self.screens = screens
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

	def add_response(self,event_id,response_fn,field_id):
		self.fields_m.add_response(event_id,response_fn,field_id)
	def add_fields(self,fields):
		self.fields_m.add_fields(fields)
	def add_field(self,field):
		self.fields_m.add_field()
	def add_entity(self,entity):
		self.entity_m.add_entity(entity)
	def add_screen(self,screen):
		self.screens[screen.screen_id] = screen







