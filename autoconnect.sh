#!/bin/bash

rfkill unblock wifi

dev_arr=(`ls /sys/class/net/`)
if ! pgrep wpa_supplicant
then 
	mkdir -p /var/run/wpa_supplicant
	wpa_supplicant -B -i ${dev_arr[2]} -c /etc/wpa_supplicant/wpa_supplicant.conf >/dev/null
fi


wpa_cli -i ${dev_arr[2]} remove_network 0
wpa_cli -i ${dev_arr[2]} add_network 0
wpa_cli -i ${dev_arr[2]} scan
sleep 5
wpa_cli -i ${dev_arr[2]} scan_results

printf "ssid "; read ssid

wpa_cli -i ${dev_arr[2]} set_network 0 ssid "\"$ssid\""
while true
do
	printf "protocol (NONE/WPA/WEP) "; read proto
	if [[ $proto == "NONE" ]]
	then
		wpa_cli -i ${dev_arr[2]} set_network 0 key_mgmt NONE
		break
	elif [[ $proto == "WPA" ]]
	then
		printf "psk "; read -s pass
		wpa_cli -i ${dev_arr[2]} set_network 0 psk "\"$pass\""
		break
	elif [[ $proto == "WEP" ]]
	then
		printf "identity "; read id
		printf "password "; read -s pass
		
		wpa_cli -i ${dev_arr[2]} set_network 0 identity "\"$id\""
		wpa_cli -i ${dev_arr[2]} set_network 0 password "\"$pass\""	
		break	
	else
		echo "Not a valid proto, redo"
	fi
done

wpa_cli -i ${dev_arr[2]} enable_network 0

# wpa_cli -i ${dev_arr[2]} disable_network 0
# rfkill block wifi



# things to take
# pc, pc charger, phone, phone charger, keyboard, whiteboard
# white board_pen, headphone
