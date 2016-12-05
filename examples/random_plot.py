import pygame
from pygame_standard.window import Window
from pygame_standard.content import Screen, Button
from pygame_standard.engines import MatplotlibEngine, ArrayField
from pygame_standard.colors import GRAY, WHITE
import numpy as np


size = (600,600)
window = Window(size)

plot_data = np.random.random(100)
data_field_id = "plot_data"
data_field = ArrayField(data_field_id,plot_data)

plot_response_id = "plot"
def data_field_response(*args,**kwargs):
	return np.random.random(100)

plotting_engine = MatplotlibEngine(screen_id="plot",plot_size=(400,400),data_field=data_field,plot_pos=(100,100))
plotting_engine.add_response(plot_response_id,data_field_response,data_field_id)
window.add_engine(plotting_engine)

interface_screen = Screen(screen_id="interface")
cb_rect = pygame.Rect((50,50),(100,20))
cb_image0 = pygame.Surface(cb_rect.size)
cb_image0.fill(GRAY)
cb_image1 = cb_image0.copy()
cb_image1.fill(WHITE)
cb_images = [cb_image0,cb_image1]
cb = Button(cb_rect,cb_images,plot_response_id)
interface_screen.add_component(cb)
window.add_screen(interface_screen)

window.run()


