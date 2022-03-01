#!/bin/bash

for pid in $(pidof -o $$ -x "beep.sh")
do
    kill -9 $pid
done
  
while true
do
    aplay /usr/share/sounds/freedesktop/index.theme -q 2>/dev/null
    sleep 0.5
done