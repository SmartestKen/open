#!/bin/bash

loop() {
	
	folder="/home/ken/clips/"


	review_lists=`find $folder -type f -name '*.mp4' | shuf -n 3`

	# one echo to produce a new line
	printf "\r\033[K"
	
	
	
	rm -f /tmp/current.mp4
	while IFS= read -r line <&9
	do
		
		ln -sfT "$line" /tmp/current.mp4
		# no new line because ffplay will print one
		echo -n "$line"
		ffplay "$line" -autoexit 2>/dev/null
		
		review_count=$((review_count+1))
		echo $review_count >$folder".reviewed"
	done 9<<< "$review_lists"	

	


	# aplay /usr/share/sounds/freedesktop/index.theme -q 2>/dev/null
}

for pid in $(pidof -o $$ -x "mem.sh")
do
    kill -9 $pid
done
pkill ffplay

loop &
