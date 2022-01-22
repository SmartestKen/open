#!/bin/bash



if xrandr | grep 'HDMI1 connected' >/dev/null
then
	screen_size="2560x1440"
else
	screen_size="1920x1080"
fi

ext="mp4"
folder="/home/ken/clips"

if [[ $1 == "" ]]
then

	# ffmpeg -y -v error -f x11grab -video_size $screen_size -framerate 10 -i $DISPLAY -f pulse -i default -c:v mjpeg -preset ultrafast -c:a aac /tmp/temp.$ext
	
	
	# ask two input two audio sources if not already there.
	# pacmd list-sources | grep -e 'index:' -e device.description -e 'name:'
	# set default on pavucontrol and check the name with * in pacmd output (or look at the device.description
	# note source only (there are .monitor ones for sys sound, do not use sink
	if [[ ! -f /home/ken/.audio1 || ! -f /home/ken/.audio2 ]]
	then
		echo "require /home/ken/.audio1 and /home/ken/.audio2 from pacmd"
		exit 1
	fi
		

	
	ffmpeg -y -v error -f x11grab -video_size $screen_size -framerate 10 -i $DISPLAY -f pulse -i $(</home/ken/.audio2) -f pulse -i $(</home/ken/.audio1) -c:v libx264 -preset ultrafast -c:a aac /tmp/temp.$ext

	
	ffplay /tmp/temp.$ext -nodisp -autoexit 2>/dev/null &
	
	# ffmpeg -v error -f x11grab -video_size $screen_size -i $DISPLAY -vframes 1 /tmp/temp.$ext
	
	
	last_topic=$(<${folder}/.last_topic)
	read -p "Topic? ($last_topic)" topic

	if [[ $topic == "" ]]
	then
		topic=$last_topic
	else
		echo "$topic" >${folder}/.last_topic
	fi
		
	# deal with no topic (just assume previous topic (or folder basde so that no need to input

	time=`date +"%Y-%m-%d_%a_%H:%M:%S"`
	mv /tmp/temp.$ext ${folder}/${topic}_$time.$ext


else
	cur_file=`readlink /tmp/current.mp4`
	if [[ $1 == "rm" ]]
	then
		echo "removed $cur_file"
		mv $cur_file /tmp/temp.$ext
	elif [[ $1 == "mv" ]]
	then
		time=`date +"%Y-%m-%d_%a_%H:%M:%S"`
		echo "$cur_file -> ${folder}/${2}_${cur_file#*_}"
		mv $cur_file ${folder}/${2}_${cur_file#*_}
	fi
fi
