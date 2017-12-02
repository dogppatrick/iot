
##!/usr/bin/env python
# see readme.txt for full instructions
# originally from https://randomconsultant.blogspot.co.uk/2017/01/building-amazon-echo-like-device-with.html
# our trigger word is oscar
# get your Google Cloud Speech API key from https://console.cloud.google.com/start
# our version can turn an LED on or off if connected to GPIO4 and GND with a 220 ohm resistor.
# our version can read our share/stock prices too.

import sys
import json
import urllib
import subprocess
import pycurl
import StringIO
import os.path
import base64 
import time
import RPi.GPIO as GPIO
import subprocess
from subprocess import Popen, PIPE, STDOUT

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.OUT)

def transcribe(duration):

	key = 'AIzaSyDj53Y1lG6l8ek46OcCHtqMOf1KvXYW5Bw'
	stt_url = 'https://speech.googleapis.com/v1beta1/speech:syncrecognize?key=' + key
	filename = 'test.flac'

	#Do nothing if audio is playing
	#------------------------------------
	if isAudioPlaying():
		#print time.strftime("%Y-%m-%d %H:%M:%S ")  + "Audio is playing"
		return ""

	

	#Record sound
	#----------------

 	#print "listening .."
    	os.system(
        'arecord -D plughw:1,0 -f cd -c 1 -t wav -d ' + str(duration) + '  -q -r 16000 | flac - -s -f --best --sample-rate 16000 -o ' + filename)
    	

	#Check if the amplitude is high enough
	#---------------------------------------
	cmd = 'sox ' + filename + ' -n stat'
	p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
	soxOutput = p.stdout.read()
	#print "Popen output" + soxOutput

	
	maxAmpStart = soxOutput.find("Maximum amplitude")+24
	maxAmpEnd = maxAmpStart + 7
	
	#print "Max Amp Start: " + str(maxAmpStart)
	#print "Max Amop Endp: " + str(maxAmpEnd)

	maxAmpValueText = soxOutput[maxAmpStart:maxAmpEnd]
	
	
	#print "Max Amp: " + maxAmpValueText

	maxAmpValue = float(maxAmpValueText)

	if maxAmpValue < 0.1 :
		#print "No sound"
		#Exit if sound below minimum amplitude
		return ""	
	

	#Send sound  to Google Cloud Speech Api to interpret
	#----------------------------------------------------
	
	print time.strftime("%Y-%m-%d %H:%M:%S ")  + "Sending to google api"


  	# send the file to google speech api
	c = pycurl.Curl()
	c.setopt(pycurl.VERBOSE, 0)
	c.setopt(pycurl.URL, stt_url)
	fout = StringIO.StringIO()
	c.setopt(pycurl.WRITEFUNCTION, fout.write)
 
	c.setopt(pycurl.POST, 1)
	c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json'])

	with open(filename, 'rb') as speech:
		# Base64 encode the binary audio file for inclusion in the JSON
        	# request.
        	speech_content = base64.b64encode(speech.read())

	jsonContentTemplate = """{
  		'config': {
      			'encoding':'FLAC',
      			'sampleRate': 16000,
      			'languageCode': 'en-GB',
			'speechContext': {
    				'phrases': [
    					'jarvis'
  				],
  			},
  		},
  		'audio': {
      		'content':'XXX'
  		}
	}"""


	jsonContent = jsonContentTemplate.replace("XXX",speech_content)

	#print jsonContent

	start = time.time()

	c.setopt(pycurl.POSTFIELDS, jsonContent)
	c.perform()


	#Extract text from returned message from Google
	#----------------------------------------------
	response_data = fout.getvalue()


	end = time.time()
	#print "Time to run:" 
	#print(end - start)


	#print response_data

	c.close()
	
	start_loc = response_data.find("transcript")
    	temp_str = response_data[start_loc + 14:]
	#print "temp_str: " + temp_str
    	end_loc = temp_str.find("\""+",")
    	final_result = temp_str[:end_loc]
	#print "final_result: " + final_result
    	return final_result


def isAudioPlaying():
	
	audioPlaying = False 

	#Check processes using ps
        #---------------------------------------
        cmd = 'ps -C omxplayer,mplayer'
	lineCounter = 0
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

        for ln in p.stdout:
		lineCounter = lineCounter + 1
		if lineCounter > 1:
			audioPlaying = True
			break

	return audioPlaying ; 



def listenForCommand(): 
	
	command  = transcribe(3)
	
	print time.strftime("%Y-%m-%d %H:%M:%S ")  + "Command: " + command 

	success=True 

	if command.lower().find("news")>-1 :
                os.system('python getNews.py')

 	elif command.lower().find("weather")>-1 :
               	os.system('python getWeather.py')
	
 	elif command.lower().find("shares")>-1 :
               	os.system('python getShares.py')


        elif command.lower().find("time")>-1 :
                subprocess.call(["/home/pi/speech.sh", time.strftime("%H:%M") ])
                print time.strftime("%H:%M")	
	
	elif command.lower().find("flatter")>-1  and  command.lower().find("me")>-1   :
                subprocess.call(["/home/pi/speech.sh", "you are gorgeous"])

	elif command.lower().find("light")>-1  and  command.lower().find("on")>-1   :
                GPIO.output(4,GPIO.HIGH)

	elif command.lower().find("light")>-1  and  command.lower().find("off")>-1   :
                GPIO.output(4,GPIO.LOW) 

	else:
		subprocess.call(["aplay", "i-dont-understand.wav"])
		success=False

	return success 



print time.strftime("%Y-%m-%d %H:%M:%S ")  + "Launched speechAnalyser.py"


while True:
		
	sys.stdout.flush() 
	
	#Listen for trigger word
        spokenText = transcribe(2) ;
	
	if len(spokenText) > 0: 
        	print time.strftime("%Y-%m-%d %H:%M:%S ")  + "Trigger word: " + spokenText

        triggerWordIndex  = spokenText.lower().find("oscar")

        if triggerWordIndex >-1:
		#If trigger word found, listen for command 
                subprocess.call(["aplay", "beep-3.wav"])
		success = listenForCommand()	
		
		if not success:
			subprocess.call(["aplay", "beep-3.wav"])
			listenForCommand()
	
