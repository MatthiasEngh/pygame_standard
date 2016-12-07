from pygame_standard.window import Window
from pygame_standard.content import Screen, VerticalSlider


size = (100,200)
window = Window(size)

interface_screen = Screen(screen_id="interface")

pos = (50,50)
length = 100
slider = VerticalSlider(pos,length,"test_slider")
interface_screen.add_component(slider)
window.add_screen(interface_screen)

window.run()


