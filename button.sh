#!/bin/bash

DATE=$(date +"%Y-%m-%d %H:%M:%S")

sensorid=Orozco
status=$(docker run --rm --cap-add SYS_RAWIO --device /dev/mem hypriot/rpi-gpio read 1)
message=""

if [ "$status" = 1 ]
then
     message="button-pressed"
else
     message="button-opened"
fi

echo $sensorid,$DATE,$message >> /home/pi/iot/button.log


curl -X PUT "http://172.104.90.53:6002/iot/$sensorid/$status/$message"
