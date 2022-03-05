pacmd load-module module-null-sink sink_name=dummy sink_properties=device.description=Virtual-Sound-Card
pactl load-module module-loopback sink=dummy
pactl load-module module-loopback sink=dummy


pacmd load-module module-null-sink sink_name=Recording sink_properties=device.description=Recording
pacmd load-module module-combine-sink sink_name=Combined slaves=Recording,alsa_output.usb-Sennheiser_Communications_Sennheiser_USB_headset-00.analog-stereo sink_properties=device.description=Combined
pacmd load-module module-loopback source=$temp2 sink=Recording latency_msec=1
