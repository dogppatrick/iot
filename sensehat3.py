from sense_emu import SenseHat
from time import time
from time import sleep

sense = SenseHat()

temp = round(sense.get_temperature()*1.8 +32)

humidity = round(sense.get_humidity())

pressure = round(sense.get_pressure())

message = 'Temperature is %d F Humidity is %d percent Pressure is %d mbars' %(temp,humidity,pressure)

sense.show_message(message, scroll_speed=(0.08),text_colour=[200,0,200], back_colour= [0,0,200])

sense.clear()
