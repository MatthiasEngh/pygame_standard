



class DefaultEngine:
	def __init__(self,layers=[]):
		# initialize with optional layers
		self.layers = layers
	def iterate(self,events):
		# check events and walk program state
		return []
	def add_layer(self,layer):
		# add an interactible and graphical layer
		self.layers.append(layer)




