#!/usr/bin/python
#-*-coding:utf-8 -*-

import os
from Tkinter import *

def getSystem():
    import subprocess
    subprocess.call('`sudo rm ip.txt`', shell=True)
    subprocess.call('`sudo ip addr show | grep inet | grep -v inet6 > ip.txt`', shell=True)
    subprocess.call('`sudo uname -a >> ip.txt`', shell=True)
    path = os.path.expanduser("/home/pi/tk/")                   
    #for f in os.readlines(path):
    f = open(path+"ip.txt","r")
    for line in f.readlines():
        line = line.strip()
        #tex.insert(END,f + "\n")
        tex.insert(END,line + "\n")        

def clrOutput():
    tex.delete('1.0',END)

def getTemp():
    import requests
    from bs4 import BeautifulSoup
    url = 'http://www.cwb.gov.tw/V7/observe/real/ObsN.htm'
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'lxml')

    tp = soup.select('table#63 > tr > td.temp1')[1].get_text()
    tex.insert(END,"Temperature:" + tp + "\n")

    return tp

def getHumidity():
    import requests
    from bs4 import BeautifulSoup
    url = 'http://www.cwb.gov.tw/V7/observe/real/ObsN.htm'
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'lxml')

    tp = soup.select('table#63 > tr > td:nth-of-type(13)')[1].get_text()
    tex.insert(END,"Humidity:" + tp + "%\n")

    return tp

def uploadData():
    import httplib, urllib, time

    thingSpeakApiKey = "7LAOABTV0FTEJKFU"

    params = urllib.urlencode({'field1': getTemp(), 'field2': getHumidity(), 'key': thingSpeakApiKey})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    try:
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        conn.connect()
        tex.insert(END,"Connecting to thingspeak..." + "\n")
    except (httplib.HTTPException, socket.error) as ex:
        tex.insert(END,"Error:" + ex + "\n")
        time.sleep(1)

    conn.request("POST", "/update", params, headers)
    response = conn.getresponse()
    tex.insert(END,"Status:" + str(response.status) + "\n")
    tex.insert(END,"Reason:" + response.reason + "\n")
    tex.insert(END,"Params:" + params + "\n")
    tex.insert(END,"Time:" + time.strftime("%c") + "\n")
    data = response.read()
    tex.insert(END,"Closing connection!" + "\n")
    conn.close()

def setLight():
    import RPi.GPIO as GPIO
    import time
  
    GPIO.setmode(GPIO.BCM)
    try:
        GPIO.setup(21, GPIO.IN)
        time.sleep(1)
        GPIO.setup(21, GPIO.OUT)
        time.sleep(1)
        GPIO.setup(21, GPIO.IN)
        time.sleep(1)
        GPIO.setup(21, GPIO.OUT)

        tex.insert(END,"Light is switching\n")
    except:
        tex.insert(END,"Error: Relay device\n")

def voiceCmd():
    import subprocess
    import sys
    import json
    import urllib
    import pycurl
    import StringIO
    import os.path
    import base64 
    import time
    import traceback
    import logging
    from subprocess import Popen, PIPE, STDOUT
    
    filename = 'test.flac'
    duration = 5
    key = 'AIzaSyDj53Y1lG6l8ek46OcCHtqMOf1KvXYW5Bw'
    stt_url = 'https://speech.googleapis.com/v1beta1/speech:syncrecognize?key=' + key

    try:
        #recording
        subprocess.call('`rm voice/test.flac > /dev/null 2>&1`', shell=True)
        os.system(
                    'arecord -D plughw:1,0 -f cd -c 1 -t wav -d ' + str(duration) + ' -q -r 16000 | flac - -s -f --best --sample-rate 16000 -o voice/' + filename
        )
        
        c = pycurl.Curl()
        c.setopt(pycurl.VERBOSE, 0)
        c.setopt(pycurl.URL, stt_url)
        fout = StringIO.StringIO()
        c.setopt(pycurl.WRITEFUNCTION, fout.write)
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json'])

        with open("voice/" + filename, 'rb') as speech:
        # Base64 encode the binary audio file for inclusion in the JSON
            speech_content = base64.b64encode(speech.read())


        jsonContentTemplate = """{
            'config': {
			'encoding':'FLAC',
      			'sampleRate': 16000,
      			'languageCode': 'zh-tw',
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
        
        #STT
        start = time.time()
        c.setopt(pycurl.POSTFIELDS, jsonContent)
        c.perform()

        response_data = fout.getvalue()
        end = time.time()
        tex.insert(END,"Processed time:" + str(end - start) + "\n")

        c.close()

        start_loc = response_data.find("transcript")
        temp_str = response_data[start_loc + 14:]
        end_loc = temp_str.find("\""+",")
        final_result = temp_str[:end_loc]
        tex.insert(END,"Response: " + final_result + "\n")    
        
        #Token and POS
        import jieba
        import jieba.posseg as pseg
        jieba.load_userdict("/usr/local/lib/python2.7/dist-packages/jieba/userdict.txt")
        words = pseg.cut(final_result)
        k=""
        kk=""
        stack=[]
        s=[]
        for w in words:
            s.append(w.word)
            k=w.flag
            kk=kk+k
            stack.append(kk)
        ss='=>'.join(s)
        tex.insert(END,"Tokens: " + ss + "\n")
        
        from fuzzywuzzy import fuzz
	from fuzzywuzzy import process
               
        lastPos="" 
        score=0 
        totalScore=0              
        #simple nlp process
        while len(stack) > 0:
            p0=len(stack)
            p1=stack.pop()
            p2=p1[-1:]
            
            #lastPos to see a pair  
            try:
                lastPos=p1[-2:]
            except:
                lastPos=""
            
            if p2=='n':
	        score1=fuzz.ratio(u"紅色LED電燈泡",s[p0-1])
                score2=fuzz.ratio(u"電燈泡",s[p0-1])
                slist=[score1,score2]
                score=max(slist)
                tex.insert(END,"n:" + str(score) + "\n")
                if score >=70:
                    totalScore=totalScore+1
            elif p2=='v':
		score1=fuzz.ratio(u"關閉",s[p0-1])
                score2=fuzz.ratio(u"關掉",s[p0-1])
                score3=fuzz.ratio(u"關起",s[p0-1])                
                score4=fuzz.ratio(u"不要開啟",s[p0-1])
                score5=fuzz.ratio(u"不要打開",s[p0-1])
                score6=fuzz.ratio(u"不要不關掉",s[p0-1])


                slist=[score1,score2,score3,score4,score5,score6]
                score=max(slist)

		tex.insert(END,"v:" + str(score) + "\n")
                if score >= 90:
		    totalScore=totalScore-10
                else:
                    score1=fuzz.ratio(u"打開",s[p0-1])
                    score2=fuzz.ratio(u"開啟",s[p0-1])
                    score3=fuzz.ratio(u"不要關閉",s[p0-1])
                    score4=fuzz.ratio(u"不要關起",s[p0-1])
                    score5=fuzz.ratio(u"不要關掉",s[p0-1])
                    score6=fuzz.ratio(u"不要不打開",s[p0-1])

                    slist=[score1,score2,score3,score4,score5,score6]
                    score=max(slist)
                    tex.insert(END,"v:" + str(score) + "\n")
                    if score >= 90:
                        totalScore=totalScore+10
	    else:
	        pass

	if totalScore>0:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(21, GPIO.OUT)
            tex.insert(END,u"LED電燈開啟!" + "\n")
            tex.insert(END,"Score:" + str(totalScore) + "\n")
	else:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(21, GPIO.IN)
            tex.insert(END,u"LED電燈關閉!" + "\n")
	    tex.insert(END,"Score:" + str(totalScore) + "\n")
 
    except Exception as e:
        print traceback.format_exc()
        #tex.insert(END,"Error: " + traceback.format_exc() + "\n")

if __name__ == '__main__':
    global process
    root = Tk()

    step= root.attributes('-fullscreen', True)
    step = LabelFrame(root,text="IoT LASS Box", font = "Arial 8 bold italic")
    step.grid(row=0, columnspan=7, sticky='W',padx=2, pady=2, ipadx=2, ipady=2)

    Button(step, text="System", font = "Arial 8 bold italic", activebackground="turquoise", width=10, height=3, command=getSystem, bg="yellow").grid(row=1, column =2)
    Button(step, text="Clean-Screen", font = "Arial 8 bold italic", activebackground="turquoise", width=10, height=3, command=clrOutput, bg="pink").grid(row=1, column =6)
    Button(step, text="Quit", font = "Arial 8 bold italic", activebackground="turquoise", width=10, height=3, command=root.quit, bg="gray").grid(row=2, column =6)

    Button(step, text="Temperature", font = "Arial 8 bold italic", activebackground="turquoise", width=10, height=3, command=getTemp, bg="blue").grid(row=2, column =2)
    Button(step, text="Humidity", font = "Arial 8 bold italic", activebackground="turquoise", width=10, height=3, command=getHumidity, bg="red").grid(row=2, column =3)
    Button(step, text="LED-Test", font = "Arial 8 bold italic", activebackground="turquoise", width=10, height=3, command=setLight, bg="green").grid(row=1, column =3)
    Button(step, text="Voice-CMD", font = "Arial 8 bold italic", activebackground="turquoise", width=10, height=3, command=voiceCmd, bg="purple").grid(row=1, column =5)
    Button(step, text="ThingSpeak", font = "Arial 8 bold italic", activebackground="turquoise", width=10, height=3, command=uploadData, bg="orange").grid(row=2, column =5)

    tex = Text(master=root)
    scr=Scrollbar(root,orient=VERTICAL,command=tex.yview)
    scr.grid(row=3, column=2, rowspan=6, columnspan=1, sticky=NS)
    tex.grid(row=3, column=1, sticky=W)
    tex.config(yscrollcommand=scr.set,font=('Arial', 8, 'bold', 'italic'))

    root.mainloop()
