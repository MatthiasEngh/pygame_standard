

TRACK_CHANGES = 0

MODES = [
	TRACK_CHANGES,
]

class Form:
	def __init__(self):
		self.components = {}
	def add(self,component,mode=None):
		self.components[component.get_id()] = component
		if mode in MODES:
			self.event = component.get_id()
	def add_event_data(self,event):
		event['form_data'] = self.get_values()
		return event
	def get_values(self):
		form_data = []
		for component in self.components:
			form_data.append(self.components[component].get_value())
		return form_data
	def set_values(self,vaue_dict):
		for element_id in value_dict:
			self.components[element_id].set_value(value_dict[element_id])
