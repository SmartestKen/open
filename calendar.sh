#!/bin/bash

target_file="/home/ken/open/calendar.txt"

# remove calendar part (including border)
extra=`sed -n '/-=-=-=-=-=-=-=-=/,$p' $target_file | tail -n +2`
# separate the on_stage tasks with second border
on_stage=`sed '/################/q' <<< $extra`
# sort the remaning off_stage ones
extra=`sed -n '/################/,$p' <<<$extra | tail -n +2  | sort -b`



cal -n 2 >$target_file
echo "-=-=-=-=-=-=-=-=`date`-=-=-=-=-=-=-=-=" >>$target_file
echo "$on_stage" >>$target_file
echo "$extra" >>$target_file

existing=`ps aux | grep "geany -i /home/ken/open/calendar.txt"`
# 1 because the grep itself produces 1
if [[ `wc -l <<<$existing` == 1 ]]
then 
	geany -i "$target_file"
else
	while IFS= read -r line
	do
		kill `awk '{print $2}' <<<$line`
	done <<<"$existing"
fi

