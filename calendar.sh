#!/bin/bash

target_file="/home/ken/open/config"

# remove calendar part (including border)
extra=`sed -n '/-=-=-=-=-=-=-=-=/,$p' $target_file | tail -n +2`
# separate the on_stage tasks with second border
on_stage=`sed '/-#-#-#-#-#-#-#-#/q' <<< $extra`
# sort the remaning off_stage ones (after -#-#-#-#-#), for each section, add a \0 as delim, sort, and remove \0 (otherwise sort will sort line by line)
extra=`sed -n '/-#-#-#-#-#-#-#-#/,$p' <<<$extra | tail -n +2 | sed 's/^\[/\x0\[/' | sort -b -z | tr -d '\000'`


# echo "$extra"
# sleep 1000000000


cal -n 2 >$target_file
echo "-=-=-=-=-=-=-=-=`date`-=-=-=-=-=-=-=-=" >>$target_file
echo "$on_stage" >>$target_file
echo "$extra" >>$target_file

existing=`ps aux | grep "geany -i $target_file"`
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

