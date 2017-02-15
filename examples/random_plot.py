import pygame
from pygame_standard.window import Window
from pygame_standard.content import Screen, Button
from pygame_standard.engines import ArrayField
from pygame_standard.matplotliblib import MatplotlibEngine
import numpy as np


# Create a window
size = (600,600)
window = Window(size)


# Create the active Screen engine
plot_data = np.random.random(100)
data_field_id = "plot_data"
data_field = ArrayField(data_field_id,plot_data)

plot_response_id = "plot"
def data_field_response(*args,**kwargs):
	return np.random.random(100)

plotting_engine = MatplotlibEngine(screen_id="plot",plot_size=(400,400),data_field=data_field,plot_pos=[100,100])
plotting_engine.add_response(plot_response_id,data_field_response,data_field_id)
window.add_engine(plotting_engine)

# Create the interface Screen
interface_screen = Screen(screen_id="interface")
cb_pos =(50,50)
cb_text = "button"
cb = Button(cb_pos,cb_text,plot_response_id)
interface_screen.add_component(cb)
window.add_screen(interface_screen)


window.run()


