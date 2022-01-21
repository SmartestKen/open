#!/bin/bash

while true
do
	
	if xrandr | grep 'HDMI1 connected' >/dev/null
	then
		width=2560
		height=1440
	else
		width=1920
		height=1080
	fi
	
	noteid=$(xdotool search --name "index.py.*Geany")
	if [[ $noteid == "" ]]
	then
		geany -i /home/ken/open/index.py &
	fi
	
	active_id=$(xdotool getactivewindow)
	echo $active_id
	# what if they do not listen?
	if [[ $active_id == $note_id ]] 
	then
		xdotool windowmove $active_id 1920 0
		xdotool windowsize $active_id 640 1335
	else
		xdotool windowmove $active_id 0 0
		xdotool windowsize $active_id 1920 1335
	fi

	sleep 1
done

# per-application, hence does not apply
