# list all sources name for loopback
pactl list sources | grep Name: | sed 's/^.*Name: //'

# null-sink
pactl load-module module-null-sink sink_name=dummy sink_properties=device.description=Recording
pactl list sources
printf "use pauvcontrol, decide the sources"; read temp1 temp2
pactl load-module module-loopback source=$temp1 sink=dummy
pactl load-module module-loopback source=$temp2 sink=dummy

pactl load-module module-loopback source=VoIP.monitor sink=alsa_output.pci-0000_00_1b.0.analog-stereo latency_msec=200
pactl load-module module-loopback source=Games.monitor sink=alsa_output.pci-0000_00_1b.0.analog-stereo latency_msec=50


# pacmd load-module module-combine-sink sink_name=Combined slaves=dummy,alsa_output.usb-Sennheiser_Communications_Sennheiser_USB_headset-00.analog-stereo sink_properties=device.description=Combined

pacmd load-module module-loopback source=$temp2 sink=dummy latency_msec=1
