#!/bin/bash

DATE=$(date +"%Y-%m-%d %H:%M:%S")

id=chair1
y=$(docker run --rm --cap-add SYS_RAWIO --device /dev/mem hypriot/rpi-gpio read 1)

if [ "$y" = 1 ]
then
     status="button pressed"
else
     status="button opened"
fi

echo $id,$DATE,$status >> /home/pi/button.log

