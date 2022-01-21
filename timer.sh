#!/bin/bash


loop() {
    clear;clear
    chmod +x /home/ken/open/mem.sh


    while true
    do	
        end=`date -d "+20minute" +%s`
        end_readable=`date -d "@$end" +%H:%M`

        while true
        do
            now=`date +%s`
            battery_left=$(</sys/class/power_supply/BAT1/capacity)
            if [[ $now > $end ]]
            then
            
				for i in {1..15}
				do
					xset dpms force off
					sleep 1
					xset dpms force on
				done

				if ! pgrep record.sh
				then
					/home/ken/open/mem.sh &
				fi
                break
            else
                printf "\r\033[K$(((end-now)/60)) min left, end at $end_readable, $battery_left"
                sleep 10
            fi
        done
        

        # separate script so that timer can continue to next session
        # /home/ken/open/beep.sh &
    done
}

for pid in $(pidof -o $$ -x "timer.sh")
do
    kill -9 $pid
done

loop $1 &
