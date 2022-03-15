server="209.182.218.253"
sshtarget='root@'$server
echo "$sshtarget"
repo_locations="/home/ken/open
/home/ken/private
/home/ken/clips"

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

reboot
SSHCMD

printf "Once server reboots successfully, press any key"; read

# ----------- setup software and git repo
ssh -T $sshtarget << SSHCMD
pacman -S git rsync --noconfirm

while IFS= read -r repo 
do
	mkdir -p \$repo
	cd \$repo
	git --bare init
	
done <<<"$repo_locations"
SSHCMD

# ---------- now upload local repo (note, we do not upload ssh keys here)
printf "Upload local repo copy? (y/n)"; read temp

while IFS= read -r repo 
do
	cd $repo
	git remote remove origin
	git remote add origin ssh://$sshtarget$repo
	if [[ $temp == "y" ]]
	then 
		git push temp master
	fi
done <<<"$repo_locations"
	



# pacman -S --noconfirm gitea glibc sqlite

# curl https://raw.githubusercontent.com/acmesh-official/acme.sh/master/acme.sh -O /acme.sh
# source /acme.sh --install -m k5shao@ucsd.edu
# just list to make sure
# crontab -l
