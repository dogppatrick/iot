import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(26,GPIO.OUT)

GPIO.output(26,GPIO.HIGH)
time.sleep(1)
GPIO.output(26,GPIO.LOW)
time.sleep(1)
GPIO.output(26,GPIO.HIGH)
time.sleep(1)
GPIO.output(26,GPIO.LOW)

