server="209.182.218.253"
sshtarget='root@'$server
echo "$sshtarget"
repo_locations="/home/ken/open
/home/ken/private
/home/ken/clips"
device=`cat /etc/hostname`

printf "Upload local ssh pub key? (y/n)"; read temp
if [[ $temp == "y" ]]
then 
	ssh-copy-id -i /home/ken/.ssh/id_rsa.pub $sshtarget
fi

# -T disable remote side tty, use -t if you need one
# --------- server full update
ssh-keyscan $server >>/home/ken/.ssh/known_hosts
ssh -T $sshtarget << SSHCMD

pacman -Syy
pacman -S archlinux-keyring --noconfirm
pacman -Syyu --noconfirm

# extra software
pacman -S git rsync --noconfirm

reboot
SSHCMD

printf "Once server reboots successfully, press any key"; read

# ---------- now upload local repo (note, we do not upload ssh keys here)
printf "Upload repo/Download repo/do nothing? (u/d)"; read temp

if [[ $temp == "u" || $temp == "d" ]]
then
	pkill sync.sh
	if [[ $temp == "u" ]]
	then
		ssh -T $sshtarget << SSHCMD
			while IFS= read -r repo 
			do
				mkdir -p \$repo
				cd \$repo
				git --bare init
				
			done <<<"$repo_locations"
SSHCMD	
	fi
		
	while IFS= read -r repo 
	do
		cd $repo
	
	
		git remote remove origin
		git remote add origin ssh://$sshtarget$repo
		
	fi
	

	if [[ $temp == "y" ]]
	then 
		git push temp master
	fi
	done <<<"$repo_locations"
fi
	
# if "u", clean up and upload
# if "d", rm -rf local except those config and download clean copy
# else skip


# pacman -S --noconfirm gitea glibc sqlite

# curl https://raw.githubusercontent.com/acmesh-official/acme.sh/master/acme.sh -O /acme.sh
# source /acme.sh --install -m k5shao@ucsd.edu
# just list to make sure
# crontab -l
