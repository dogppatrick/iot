##!/usr/bin/env python

import subprocess
import time 
from yahoo_finance import Share

tw = Share('TW.L')
shareMessage = "Taylor Wimpey " + tw.get_price() 
print shareMessage
subprocess.call(["/home/pi/speech.sh", shareMessage])

tw = Share('TALK.L')
shareMessage = "Talk Talk " + tw.get_price()
print shareMessage
subprocess.call(["/home/pi/speech.sh", shareMessage])

tw = Share('AAL.L')
shareMessage = "Anglo American " + tw.get_price()
print shareMessage
subprocess.call(["/home/pi/speech.sh", shareMessage])


