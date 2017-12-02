##!/usr/bin/env python

import subprocess
import feedparser



d = feedparser.parse('http://open.live.bbc.co.uk/weather/feeds/en/SW1A%202AA/3dayforecast.rss')

introMessage = "Hi, here is the 3 day weather forecast" 

subprocess.call(["/home/pi/speech.sh", introMessage])

counter = 0 
degree_sign= u'\N{DEGREE SIGN}'

for post in d.entries:
        
	
	weatherMessage =  post.title.replace(degree_sign+"C"," degrees Celcius")
	weatherMessage =  weatherMessage.replace(degree_sign+"F"," degrees Fahrenheit")
	
	weatherMessage =  weatherMessage.replace("("," ")
	weatherMessage =  weatherMessage.replace(")"," ")
	weatherMessage =  weatherMessage.replace(":"," ")

	print weatherMessage 	

	subprocess.call(["/home/pi/speech.sh", weatherMessage])
	
	counter = counter + 1
	if counter == 3:
		break 

