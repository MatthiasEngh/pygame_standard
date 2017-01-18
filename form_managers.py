





class DefaultFM:
	forms = []
	def add(self,form):
		self.forms.append(form)
	def check_event(self,event):
		for form in self.forms:
			if hasattr(form, 'event'):
				if form.has_event(event):
					return form.add_event_data(event)
		return event



