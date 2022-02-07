#!/bin/bash
initFunc() {
	# dns setting
	echo "nameserver 1.1.1.1" >/etc/resolv.conf.head


	rfkill block bluetooth
	# rfkill block wifi
	rfkill block wifi

	# write to an existing file does not change right, hence this line does not need su ken. Furthermore, due to existence of another startup service, we only need this once unlike redshift

	for value in {1..15}
	do
		printf 1 >/sys/class/backlight/intel_backlight/brightness
		sleep 1
	done
}


for pid in $(pidof -o $$ -x "init.sh")
do
	kill $pid
done
initFunc &
