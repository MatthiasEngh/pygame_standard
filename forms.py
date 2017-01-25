


class Form:
	def __init__(self,ID):
		self.ID = ID
		self.components = {}
		self.attachments = []
		self.trigger = None
	def add_component(self,component):
		self.components[component.get_id()] = component
	def add_trigger(self,trigger):
		self.add_component(trigger)
		self.trigger = trigger.get_id()
	def add_attachment(self,attachment):
		self.components.add(attachment)
		self.attachments.append(attachment.get_id())
	def add_event_data(self,event):
		event['components'].extend(self.attachments)
		for cid in self.attachments:
			event[cid] = self.components[cid].get_value()
		event['form'] = self.ID
		return event
	def triggered(self,event):
		return self.trigger == event['components'][0]
	def get_id(self):
		return self.ID


RECEIVERFORMID = "receiver_form"

class ReceiverForm(Form):
	def __init__(self):
		self.receivers = {}
		Form.__init__(self,RECEIVERFORMID)
	def receive(self,data):
		for receiver in data:
			self.receivers[receiver].set_value(data[receiver])
	def add_receiver(self,receiver):
		self.receivers[receiver.get_id()] = receiver
