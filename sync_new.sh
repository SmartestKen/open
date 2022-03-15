#!/bin/bash 

loop() {
    # eval needed to initialize ssh environment
    pkill ssh-agent
    eval $(ssh-agent -s)
    ssh-add /home/ken/.ssh/id_rsa
    
    # use the following to manually update preferences (e.g. when there is a new extension)
    # cp -u /home/ken/.config/BraveSoftware/Brave-Browser/Default/Preferences /home/ken/private/.config/BraveSoftware/Brave-Browser/Default/Preferences
    
    
    # assume the set server part is done in root_setup.sh
    if [ -z "$(ls /home/ken/clips 2>&1)" ]
    then
		cd /home/ken/clips
		git fetch origin master
		git reset --hard origin/master
	fi
    
    
    device=`cat /etc/hostname`
    repo_locations="/home/ken/open
	/home/ken/private
	/home/ken/clips"
 
	# daily update on .config
	cur_date=`date -I`
 
    while true
    do

        temp_date=`date -I`
		# file update from /home/ken/.config to /home/ken/private/.config
		if [[ $device == "laptop2" && $temp_date != $cur_date ]] 
		then
			while read -r file
			do
				src=$(sed 's/\/private//g' <<<"$file")
				if [[ -f "$src" ]]
				then
					cp -u "$src" "$file"
				else
					rm -f "$file"
				fi
			done < <(find /home/ken/private/.config -name \* -type f)
			
			# update extensions as well
			cp -R -u /home/ken/.config/BraveSoftware/Brave-Browser/Default/Extensions/* /home/ken/private/.config/BraveSoftware/Brave-Browser/Default/Extensions
			
			cur_date=$temp_date
		fi

		# ---------- syncing each repo
		while IFS= read -r repo
		do
			cd $repo

			echo "checking $repo"
			if git fetch origin master -q 2>/dev/null
			then
				echo "updating $repo"
				git add . -A --ignore-errors
				
				# read from git diff (avoid for loop for reading command output!)
				while read -r file
				do
					remote_time=`git log origin/master -1 --pretty="format:%at" -- "$file" 2>/dev/null`
					# note, using `date +%s -r` may have trouble when file is deleted, in which case local_time='' and mix the case of "deleted locally" and "added remotely"
					local_time=`git log -1 --pretty="format:%at" -- "$file" 2>/dev/null`
					
					# essentially 4(2x2) cases, remote is empty or not (multiply) local is empty or not
					# echo $file $remote_time $local_time
					if [[ $remote_time != '' && ($local_time == '' || $remote_time > $local_time) ]]
					then
						# echo $file $remote_time $local_time
						# --no-overlay remove empty directory as well 
						git checkout origin/master --no-overlay -- "$file" 2>/dev/null
					fi
				done < <(git diff --cached --name-only --no-renames origin/master 2>/dev/null)
				# --name-only compares the hash only, the below commands compare the content (so that immune to e.g. sudden change of encryption), but obviously --name-only is much cheaper
				# sed -n 's/^diff --git .*b\///p' < <(git diff --cached origin/master --no-color)

				# it is fine to use --soft as only the last add becomes commit, but it causes previous add blobs to be saved as well, hence --mixed can save extra space without waiting for gc. but --soft let git second add to partially use git first add's blobs, which saves computation
				
				git reset --mixed origin/master -q
				git add . -A --ignore-errors &&
				git commit -m "$device" -q >/dev/null &&
				git push -f origin master -q
			fi
		done <<<"$repo_locations"

        sleep 300
    done

}

for pid in $(pidof -o $$ -x "sync.sh")
do
    kill $pid
done
  
loop &
