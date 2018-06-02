#!/bin/bash

DATE=`date '+%Y-%m-%d-%H%M%S'`
raspistill  -hf -o /home/pi/iot/$DATE.jpg

wolfram -script /home/pi/iot/test.m
