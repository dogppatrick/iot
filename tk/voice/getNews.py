##!/usr/bin/env python

import subprocess
import feedparser
import time 


d = feedparser.parse('http://feeds.bbci.co.uk/news/rss.xml?edition=uk')

introMessage = "BBC News Headlines at " + time.strftime("%H:%M") 

subprocess.call(["/home/pi/speech.sh", introMessage])

maxItems = 3
itemCounter = 0 

for post in d.entries:
        print post.title
	subprocess.call(["/home/pi/speech.sh", post.title])
	itemCounter = itemCounter + 1
	if itemCounter == maxItems:
		break

sportPage = feedparser.parse('http://feeds.bbci.co.uk/sport/rss.xml?edition=uk')

itemCounter = 0

for post in sportPage.entries:
        print post.title
        subprocess.call(["/home/pi/speech.sh", post.title])
        itemCounter = itemCounter + 1
        if itemCounter == maxItems:
                break

