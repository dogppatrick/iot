#!/bin/bash

sensorid=Orozco
limit=99700
sleeptime=3

while true
do
  DATE=$(date +"%Y-%m-%d %H:%M:%S")
  source_temp=$(/opt/vc/bin/vcgencmd measure_temp)
  temp=$(awk -F"=" '{print $2}' <<< $source_temp | awk -F"'" '{print $1}')
  echo $temp > /home/pi/iot/sensor.log
  output=$(wolfram -script edge.m)

  echo $DATE Sensorid: $sensorid, The temperature: $temp

  if(($(echo "$output > $limit" | bc -l))); then
    curl -X PUT "http://172.104.90.53:6002/iot1/$sensorid/$temp/overheating"
  fi

  sleep $sleeptime
done 

