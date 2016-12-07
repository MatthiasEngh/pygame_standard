from pygame_standard.window import Window
from pygame_standard.content import Screen, Button


size = (150,120)
window = Window(size)

interface_screen = Screen(screen_id="interface")

button_pos = (50,50)
button_text = "Button"
button_id = "buttonID"
button = Button(button_pos,button_text,button_id)

interface_screen.add_component(button)
window.add_screen(interface_screen)



window.run()


