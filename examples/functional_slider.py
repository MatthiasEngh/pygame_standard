import pygame
from pygame_standard.window import Window
from pygame_standard.content import Screen, VerticalSlider, Text, Button
from pygame_standard.forms import ReceiverForm
from pygame_standard.engines import DefaultEngine, Field


size = (600,600)
window = Window(size)



interface_screen = Screen(screen_id="interface")

pos = (50,50) 
height = 100
sliderID = "verticalSlider"
verticalSlider = VerticalSlider(pos,height,sliderID)

textElement = Text((100,50),20,"text",'text_element')

interface_screen.add_component(verticalSlider)
interface_screen.add_component(textElement)

engine = DefaultEngine()
field0ID = 'field0'
field0 = Field(field0ID)
field0.subject(verticalSlider)
field0.master(textElement)


engine.add_field(field0)

receiver_form = ReceiverForm()
receiver_form.add_receiver(textElement)

window.add_form(receiver_form)
window.add_screen(interface_screen)
window.add_engine(engine)



window.run()


