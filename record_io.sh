# list all sources name for loopback
sources=`pactl list sources | grep Name: | sed 's/^.*Name: //'`
if [[ $sources != *"dummy"* ]]
then	
	# to remove, use `pactl unload-module module-null-sink`
	pactl load-module module-null-sink sink_name=dummy sink_properties=device.description=Recording
	while IFS= read -r item
	do
		pactl load-module module-loopback source=$item sink=dummy
	done <<<"$sources"
fi
