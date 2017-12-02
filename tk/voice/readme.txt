Plug in a USB audio card

Increase mic volume for USB device to full using 

alsamixer

(F6 to change to USB device and arrow keys move across to Mic and up arrow increases volume to full, Esc to quit)

Make a test recording:

arecord -D plughw:1,0 -f S16_LE test.wav

CTRL-C to quit

aplay test.wav


Sign up to Google cloud platform for free

https://console.cloud.google.com/start

Google Cloud Speech API

go to Credenitials tab -> Create Credentials -> API Key -> cut and paste your API key for use in speechAnalyser.py later

sudo apt-get install mplayer

sudo apt-get install sox

sudo apt-get install flac

sudo apt-get install python-pycurl

sudo apt-get install python-pip

sudo pip install feedparser


sudo pip install yahoo-finance

search for stock/share symbols at https://uk.finance.yahoo.com/lookup/ and edit getShares.py to suit.


while in folder /home/pi pull ZIP file from our server with

wget www.securipi.co.uk/vr.zip

unzip vr.zip

chmod a+x speech.sh

edit speechAnalyser.py so it contains your Google Cloud Speech API key

nano speechAnalyser.py

save it and exit

run it while connected to the internet

python speechAnalyser.py

say the trigger word "oscar", wait for a beep, and then say either "news, weather, shares, time, light on, light off, flatter me"
