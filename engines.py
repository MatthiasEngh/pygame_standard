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
		self.value = init_data
		self.id = id
		self.version = 0
		self.masters = []
		self.subjects = []
	def has_changed(self,version):
		return not self.version == version
	def get_id(self):
		return self.id
	def get_version(self):
		return self.version
	def set_value(self,value):
		self.value = value
		self.update_version()
	def update_version(self):
		self.version += 1
	def get_value(self):
		return self.value
	def update_value(self,value):
		if value != self.value:
			self.set_value(value)
	def master(self,component):
		self.subjects.append(component.get_id())
	def subject(self,component):
		self.masters.append(component.get_id())
	def has_masters(self):
		return len(self.masters) > 0
	def get_masters(self):
		return self.masters
	def has_subjects(self):
		return len(self.subjects) > 0
	def get_subjects(self):
		return self.subjects


class SimpleFieldMixin:
	def update_value(self,value):
		self.set_value(value)

class SimpleUpdateCheckMixin:
	is_new = True
	def update_version(self):
		self.is_new = True
	def has_changed(self,version=None):
		is_new = self.is_new
		self.is_new = False
		return  is_new


class ButtonField(Field,SimpleFieldMixin,SimpleUpdateCheckMixin):
	pass



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
	def __init__(self,fields={}):
		self.fields = fields
		self.masters = {}
		self.master_fields = []
	def get_fields(self):
		return self.fields
	def add_field(self,field):
		self.fields[field.get_id()] = field
		if field.has_masters():
			for master in field.get_masters():
				self.assign_master(master,field)
		if field.has_subjects():
			self.master_fields.append(field)
	def assign_master(self,master,field):
		if master in self.masters:
			self.masters[master].append(field)
		else:
			self.masters[master] = [field]
	def add_fields(self,fields):
		for field in fields:
			self.add_field(field)
	def return_formdata(self):
		update_data = {}
		for mf in self.master_fields:
			for s in mf.get_subjects():
				update_data[s] = mf.get_value()
		return update_data
	def update_fields(self,data):
		for cid in data['components']:
			if cid in self.masters:
				for subject in self.masters[cid]:
					subject.update_value(data[cid])
	def apply_mechanic(self,mechanic):
		pass







class DefaultEngine:
	def __init__(self,fields = {},entities = pygame.sprite.Group(),screen_id=None,mechanics=[],**kwargs):
		self.screen = Screen(screen_id=screen_id,**kwargs)
		self.entity_m = DefaultEntityManager(entities)
		self.fields_m = DefaultFieldManager(fields)
		self.mechanics = mechanics
	def iterate(self):
		self.entity_m.iterate(self.fields_m.get_fields())
		self.calculate()
		return self.fields_m.return_formdata()
	def get_screen(self):
		return self.screen
	def add_entity(self,entity):
		self.screen.add_component(entity)
		self.entity_m.add_entity(entity)
	def add_field(self,field):
		self.fields_m.add_field(field)
	def add_fields(self,fields):
		self.fields_m.add_fields(fields)
	def add_mechanic(self,mechanic,index=None):
		if index is None:
			self.mechanics.append(mechanic)
		else:
			self.mechanics.insert(index,mechanic)
	def add_mechanics(self,mechanics):
		for mechanic in mechanics:
			self.add_mechanic(mechanic)
	def get_screen(self):
		return self.screen
	def calculate(self):
		for mechanic in self.mechanics:
			self.fields_m.apply_mechanic(mechanic)
	def update_fields(self,data):
		self.fields_m.update_fields(data)


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







