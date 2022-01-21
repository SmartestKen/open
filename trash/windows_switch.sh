#!/bin/bash
# if possible, handled at boot up, then shortcut to adjust whenever needed.

noteid=$(xdotool search --name "index.py.*Geany")
if [[ $noteid == "" ]]
then
	# if not exist, store current window, open geany (auto front and focused)
	printf $(xdotool getactivewindow) >/home/ken/.window_memory
	geany -i /home/ken/open/index.py &
else
	activeid=$(xdotool getactivewindow)
	
	# note currently active
	if [[ $noteid == $activeid ]]
	then
		if [[ -f "/home/ken/.window_memory" ]]
		then
			xdotool windowactivate $(</home/ken/.window_memory)
			rm -f /home/ken/.window_memory
		fi
	# note not currently active
	else 
		printf $(xdotool getactivewindow) >/home/ken/.window_memory
		xdotool windowactivate $noteid
	fi
fi	
