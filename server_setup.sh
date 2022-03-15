sshtarget='root@209.182.218.253'
repo_locations="/home/ken/open
/home/ken/private
/home/ken/clips"

# -T disable remote side tty, use -t if you need one
# --------- server full update
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
	
done <<<$repo_locations
SSHCMD

# ---------- now upload local repo (note, we do not upload ssh keys here)
while IFS= read -r repo 
do
	cd $repo
	git remote add temp ssh://$sshtarget$repo
	git push temp master
	git remote remove temp

done <<<$repo_locations



# pacman -S --noconfirm gitea glibc sqlite



# useradd -d /home/ken -m ken
# printf "Create userpasswd:"; read temp
# printf "%s\n" $temp $temp | passwd ken




# now each time a new laptop, simply send the pub keys to somewhere



# curl https://raw.githubusercontent.com/acmesh-official/acme.sh/master/acme.sh -O /acme.sh
# source /acme.sh --install -m k5shao@ucsd.edu
# just list to make sure
# crontab -l
