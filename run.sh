#!/bin/bash

DATE=$(date +"%Y-%m%-d_%H%M")
raspistill  -hf -o /home/pi/$DATE.jpg

wolfram -script /home/pi/test.m
