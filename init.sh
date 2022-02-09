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
	
	cur_date=1970-01-01
	# the following will be replaced by root_setup.sh to reduce duplicate entry, bid -> boot id; sid -> system id
	dname=nvme0n1; bid=p1; sid=p2

	while true
	do
		temp_date=`date -I`

		if [[ $cur_date != $temp_date ]]
		then
			mkdir /efi
			mount /dev/$dname$bid /efi
			
			pacman -Syyu --noconfirm
			
			cp /boot/vmlinuz-linux /efi/
			# use kernel for console font, equivalent.
			sed -i '/^HOOKS=/ s/.*/HOOKS=(base udev autodetect keyboard modconf block encrypt filesystems fsck)/g' /etc/mkinitcpio.conf
			mkinitcpio -g /efi/initramfs-linux.img -c /etc/mkinitcpio.conf -k /efi/vmlinuz-linux
			
			umount /efi
			rmdir /efi
		fi
		cur_date=$temp_date
		sleep 43200
	done
	
	
}

if ! pgrep pacman
then 
	for pid in $(pidof -o $$ -x "init.sh")
	do
		kill $pid
	done
	initFunc &
fi
