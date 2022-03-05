pacmd load-module module-null-sink sink_name=dummy sink_properties=device.description=Virtual-Sound-Card
pactl load-module module-loopback sink=dummy
pactl load-module module-loopback sink=dummy
