pacmd load-module module-null-sink sink_name=dummy sink_properties=device.description=recording
pactl load-module module-loopback sink=dummy
pactl load-module module-loopback sink=dummy

pactl load-module module-loopback source=VoIP.monitor sink=alsa_output.pci-0000_00_1b.0.analog-stereo latency_msec=200
pactl load-module module-loopback source=Games.monitor sink=alsa_output.pci-0000_00_1b.0.analog-stereo latency_msec=50


pacmd load-module module-combine-sink sink_name=Combined slaves=dummy,alsa_output.usb-Sennheiser_Communications_Sennheiser_USB_headset-00.analog-stereo sink_properties=device.description=Combined

pacmd load-module module-loopback source=$temp2 sink=dummy latency_msec=1
