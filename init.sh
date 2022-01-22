#!/bin/bash
initFunc() {
	# dns setting
	printf "nameserver 1.1.1.1" >/etc/resolv.conf.head


	rfkill block bluetooth
	# rfkill block wifi
	rfkill block wifi

	# write to an existing file does not change right, hence this line does not need su ken. Furthermore, due to existence of another startup service, we only need this once unlike redshift

	for value in {1..15}
	do
		printf 10 >/sys/class/backlight/intel_backlight/brightness
		sleep 1
	done
	
	cur_date=1970-01-01
	while true
	do
		temp_date=`date -I`
		if [[ $cur_date != $temp_date ]]
		then
			pacman -Syyu --noconfirm
		fi
		cur_date=$temp_date
		sleep 43200
	done

}

# if pacman currently running, do not start a new script
if ! pgrep pacman
then 

	for pid in $(pidof -o $$ -x "init.sh")
	do
		kill $pid
	done


	initFunc &
fi
