from pygame_standard.window import Window
from pygame_standard.content import Screen, Button, Text
from pygame_standard.engines import DefaultEngine, Field, ButtonField
from pygame_standard.forms import ReceiverForm


size = (150,120)
window = Window(size)

interface_screen = Screen(screen_id="interface")

button_pos = (50,50)
button_text = "Button"
button_id = "buttonID"
button = Button(button_pos,button_text,button_id)



textElement = Text((100,50),20,"1",'text_element')


engine = DefaultEngine()
field0ID = 'field0'
field0 = ButtonField(field0ID)
field0.subject(button)

field1ID = 'currentF'
field1 = Field(field1ID,0)
field1.master(textElement)

field2ID = 'lastF'
field2 = Field(field2ID,1)

engine.add_field(field0)
engine.add_field(field1)
engine.add_field(field2)

receiver_form = ReceiverForm()
receiver_form.add_receiver(textElement)

window.add_form(receiver_form)

interface_screen.add_component(button)
interface_screen.add_component(textElement)
window.add_screen(interface_screen)
window.add_engine(engine)



window.run()


