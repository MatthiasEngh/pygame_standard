
from pygame_standard.forms import RECEIVERFORMID




class DefaultFM:
	forms = {}
	def add(self,form):
		self.forms[form.get_id()] = form
	def check_event(self,event):
		for form_id in self.forms:
			form = self.forms[form_id]
			if form.triggered(event):
				return form.add_event_data(event)
		return event
	def receive(self,data):
		if RECEIVERFORMID in self.forms:
			self.forms[RECEIVERFORMID].receive(data)




