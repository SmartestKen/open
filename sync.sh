#!/bin/bash 

# same repo and branch ensures that whichever computer in use, we can get the latest data with no operations
# but you always need to connect to some sort of server to fetch/push files. Hence github may be the most convenient to go (rather than setup a network drive yourself)

sync_repo() {
    cd $1

    if git fetch origin master -q 2>/dev/null
    then

        # first add (but do not commit) to compare with origin/master, add a placemholder to prevent useless commit        
        ignore_files=`find . -type f -size +75M -not -path '*/\.git/*'`
        if [[ $ignore_files != "" ]]
        then
			sed 's|^\./||g' >"$1"/.git/info/exclude <<< "$ignore_files"
			echo "$ignore_files" | xargs git rm --cached 2>/dev/null
		fi
		
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
        
        # soft reset to avoid updating those files that we obtained from the remote just now (imagine without reset, the HEAD and working tree now also differs at those files we obtained from remote just now and therefore they get commited again.) reset ensures if commit only contains file that we updated from our side
        # it is fine to use --soft as only the last add becomes commit, but it causes previous add blobs to be saved as well, hence --mixed can save extra space without waiting for gc. but --soft let git second add to partially use git first add's blobs, which saves computation
        # no need to worry about edge case of newly inited repo. once reset, those git log will have all equal timestamp, thus allowing new stuff to be worked and pushed
        
        # openssl -K raw -k passphrase, which will be used along with -S salt to produce raw. Note raw and salt are hex only
        
        git reset --mixed origin/master -q
        git add . -A --ignore-errors &&
        git commit -m "$2" -q >/dev/null &&
        git push -f origin master -q
    fi
}

loop() {
    # eval needed to initialize ssh environment
    pkill ssh-agent
    eval $(ssh-agent -s)
    ssh-add /home/ken/.ssh/id_rsa
    
    if xrandr | grep 'HDMI1 connected' >/dev/null
    then
        xrandr --output HDMI1 --mode 2560x1440 --rate 75
        xrandr --output eDP1 --off
    else
        xrandr --output eDP1 --mode 1920x1080 --rate 60
        xrandr --output HDMI1 --off
    fi
    # use the following to manually update preferences (e.g. when there is a new extension)
    # cp -u /home/ken/.config/BraveSoftware/Brave-Browser/Default/Preferences /home/ken/private/.config/BraveSoftware/Brave-Browser/Default/Preferences
    
    if ! ls /home/ken/clips >/dev/null 2>&1
    then
		mkdir -p /home/ken/clips
		cd /home/ken/clips
		git init
		git remote add origin git@github.com:SmartestKen/clips.git
		git fetch origin master
		git reset --hard origin/master
	fi
    
    
    index=`tail -c 2 /etc/hostname`
 
	# daily update on .config
	cur_date=`date -I`
 
    while true
    do

        # sync now contains both up (push) and down, albeit in a different directory
        sync_repo /home/ken/open laptop$index
        
        temp_date=`date -I`
		# file update from /home/ken/.config to /home/ken/private/.config
		if [[ $index == 2 && $temp_date != $cur_date ]] 
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

        sync_repo /home/ken/private laptop$index
        
        sync_repo /home/ken/clips laptop$index
                
        sleep 300
    done

}

for pid in $(pidof -o $$ -x "sync.sh")
do
    kill $pid
done
  
loop &
