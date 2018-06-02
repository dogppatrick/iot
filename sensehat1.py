
from sense_emu import SenseHat

sense = SenseHat()

red = (255,0,0)
sense.show_message("Sample Text",text_colour=red)
