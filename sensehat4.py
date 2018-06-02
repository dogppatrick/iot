from sense_hat import SenseHat
sense = SenseHat()
Import Rpi.GPIO as GPIO
GPIO.setwarnings (False)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(33,GPIO.OUT)

while True:
	t = sense.get_temperature()
	t = round(t,1)
	if t > 26 and t < 29.0:
		GPIO.output(33,False)
		bg = [45, 76, 164] 
	else:
		GPIO.output(33,True)
		bg = [100, 0, 0] 
	msg = “Temperature = %s” % (t)
	sense.show_message(msg, scroll_speed=0.05, back_colour=bg)
