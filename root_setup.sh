#!/bin/bash

ln -sf /usr/share/zoneinfo/America/Los_Angeles /etc/localtime
date -s "$(curl --head http://google.com 2>&1 | grep Date: | cut -d' ' -f3-6)Z"
hwclock --systohc

echo "en_US.UTF-8 UTF-8" >/etc/locale.gen
locale-gen

printf "Laptop index (>0):"; read index
echo "laptop$index" >/etc/hostname
echo "127.0.0.1 localhost
::1 localhost" >/etc/hosts

printf "Create userpasswd:"; read temp
printf "%s\n" $temp $temp | passwd root
useradd -d /home/ken -m ken
printf "%s\n" $temp $temp | passwd ken

printf "is everything ok?"; read


# use blkid to obtain PARTUUID and remove all other entries
# https://linux.die.net/man/8/efibootmgr#:~:text=efibootmgr%20is%20a%20userspace%20application,running%20boot%20option%2C%20and%20more.
# https://www.rodsbooks.com/efi-bootloaders/efistub.html
# https://wiki.archlinux.org/title/EFISTUB#Using_UEFI_directly
# rw read-write ro read-only
# https://manpages.ubuntu.com/cgi-bin/search.py?titles=Title&q=kernel-command-line.7

# add encrypt into hook and regenerate (can use mkinitcpio -p linux, which uses /etc/mkinitcpio.d/linux.preset to deduce all those arguments), the initramfs file name should correspond to what is cp below. Also note that 

# the following will be replaced by iso_setup.sh to reduce duplicate entry, bid -> boot id; sid -> system id, there cannot be a inductive sed as that will modify the downstream commands itself
dname=nvme0n1; bid=p1; sid=p2
mkdir /efi
mount /dev/$dname$bid /efi

cp /boot/vmlinuz-linux /efi/
# use kernel for console font, equivalent.
sed -i '/^HOOKS=/ s/.*/HOOKS=(base udev autodetect keyboard modconf block encrypt filesystems fsck)/g' /etc/mkinitcpio.conf
mkinitcpio -g /efi/initramfs-linux.img -c /etc/mkinitcpio.conf -k /efi/vmlinuz-linux
# cp /boot/initramfs-linux.img /efi/

umount /efi
rmdir /efi



pacman -Syy 
# pacman -S grub
# grub-install --efi-directory=/efi /dev/$dname
# grub-mkconfig -o /boot/grub/grub.cfg
pacman -S efibootmgr --noconfirm
efibootmgr -B -b 0000 -q
# disble check and log, 
efibootmgr -d /dev/$dname -p ${bid: -1} -c -L "arch" -l /vmlinuz-linux -u "cryptdevice=UUID=`blkid -s UUID -o value /dev/$dname$sid`:croot root=UUID=`blkid -s UUID -o value /dev/mapper/croot` rw initrd=\initramfs-linux.img vconsole.font=solar24x32 quiet"

# for manual testing
# efibootmgr -d /dev/nvme0n1 -p 1 -c -L "arch" -l /vmlinuz-linux -u "cryptdevice=UUID=`blkid -s UUID -o value /dev/nvme0n1p2`:croot root=UUID=`blkid -s UUID -o value /dev/mapper/croot` rw initrd=\initramfs-linux.img vconsole.font=solar24x32 quiet"

pacman -Rns efibootmgr --noconfirm
printf "CHECKPOINT (BOOTABLE)?"; read


# now step by step towards dekstop environment
# openssh used for keygen in user_setup.sh
# fakeroot needed by makepkg for brave-bin

# philosophy, find a satisfactory mainstream desktop, then try to strip it down as much as possible. DO NOT try to construct desktop from scratch
# https://wiki.archlinux.org/title/Comparison_of_desktop_environments
# !!! try to grab from as less de as possible
# latte-dock, lxterminal not usable
# never attempt to figure out dependencies yourself
# the goal is to select one that 1. satisfy the need 2., do not install an entire framework. Do not attempt to minimize the size, it is not productive.
# thunar does not have content search
# https://wiki.archlinux.org/title/Xorg#Installation for graphic driver instructions, no graphic driver causes tear when scrolling
# android-tools for adb connection through usb
# xorg-xrandr for monitor
pacman -S base-devel archlinux-keyring xorg-server xorg-xinit xf86-video-intel dhcpcd wpa_supplicant openbox plank xfce4-terminal thunar thunar-archive-plugin xarchiver unzip unrar geany redshift git openssh nano android-tools xorg-xrandr alsa-utils sof-firmware pulseaudio pavucontrol noto-fonts-cjk python3 xorg-xprop xdotool ffmpeg physlock xorg-xset pyenv --noconfirm

pacman -Rns sudo --noconfirm
python -m ensurepip --upgrade



su ken -c "
git clone --depth=1 https://aur.archlinux.org/brave-bin.git /home/ken/brave-bin
cd /home/ken/brave-bin
makepkg -sirc
rm -rf /home/ken/brave-bin"
printf "is everything ok?"; read


# note, must escape those that will be evaluate inside the child shell
# startup now all in .xinitrc (not using user_init any more)
# prevent screen auto close
echo '
Section "ServerLayout"
    Identifier "ServerLayout0"
    Option     "StandbyTime"   "0"
    Option     "SuspendTime"   "0"
    Option     "OffTime"       "0"
    Option     "BlankTime"     "0"
EndSection' >/etc/X11/xorg.conf


su ken -c "cp /etc/X11/xinit/xinitrc /home/ken/.xinitrc"
cat /home/ken/.xinitrc
printf "How many lines to remove from .xinitrc?"; read N
# existing file will retain its permission
echo "$(head -n -$N /home/ken/.xinitrc)" >/home/ken/.xinitrc
# leave qt5ct variable there for qt5 font support
echo 'redshift -O 3000K &
/home/ken/open/sync.sh &
export QT_QPA_PLATFORMTHEME=qt5ct
XDG_SESSION_TYPE=x11 plank &
geany -i &
xfce4-terminal &

if xrandr | grep "HDMI1 connected" >/dev/null
then
	xrandr --output HDMI1 --mode 2560x1440 --rate 75
	xrandr --output eDP1 --off
	max_width=2560
	max_height=1440
	target_width=1860
	target_height=440
else
	xrandr --output eDP1 --mode 1920x1080 --rate 60
    xrandr --output HDMI1 --off
	max_width=1920
	max_height=1080
	target_width=1370
	target_height=350
fi

sleep 2
noteid=$(xdotool search --name untitled)

xprop -id $noteid -format _NET_WM_STRUT_PARTIAL 32c -set _NET_WM_STRUT_PARTIAL 0,0,0,$target_height,0,0,0,0,0,0,0,$target_width
xdotool windowmove $noteid 0 $((max_height-target_height))
xdotool windowsize $noteid $target_width $target_height

xprop -id $noteid -format _NET_WM_WINDOW_TYPE 32a -set _NET_WM_WINDOW_TYPE _NET_WM_WINDOW_TYPE_DESKTOP
xprop -id $noteid -format _NET_WM_STATE 32a -set _NET_WM_STATE _NET_WM_STATE_STICKY,_NET_WM_STATE_SKIP_TASKBAR,_NET_WM_STATE_SKIP_PAGER

cmdid=$(xdotool search --name "Terminal - ")

xprop -id $cmdid -format _NET_WM_STRUT_PARTIAL 32c -set _NET_WM_STRUT_PARTIAL 0,0,0,$target_height,0,0,0,0,0,0,$target_width,$max_width
xdotool windowmove $cmdid $target_width $((max_height-target_height))
xdotool windowsize $cmdid $((max_width-target_width)) $target_height
 
xprop -id $cmdid -format _NET_WM_WINDOW_TYPE 32a -set _NET_WM_WINDOW_TYPE _NET_WM_WINDOW_TYPE_DESKTOP
xprop -id $cmdid -format _NET_WM_STATE 32a -set _NET_WM_STATE _NET_WM_STATE_STICKY,_NET_WM_STATE_SKIP_TASKBAR,_NET_WM_STATE_SKIP_PAGER

pactl set-sink-mute @DEFAULT_SINK@ false
pactl set-source-mute @DEFAULT_SOURCE@ false

exec openbox --replace' >>/home/ken/.xinitrc
echo "startx" >>/home/ken/.bash_profile
echo '
export PATH="/home/ken/.pyenv/shims:$PATH"
eval "$(pyenv init -)"' >>/home/ken/.bashrc



systemctl enable dhcpcd
echo "noarp" >>/etc/dhcpcd.conf

systemctl disable systemd-journal-flush systemd-journald systemd-journal-catalog-update lvm2-monitor wpa_supplicant ldconfig
systemctl mask systemd-journal-flush systemd-journald systemd-journal-catalog-update lvm2-monitor wpa_supplicant


# plasma -Rsn to remove package and its dependencies
pacman -Scc --noconfirm


# init
server='209.182.218.253'
sshtarget="root@"$server
rsync $sshtarget:/home/ken/open/init.sh /init.sh
chmod 744 /init.sh

# After=network-online.target
# After=network.target
echo '
[Unit]
After=multi-user.target
[Service]
Type=forking
ExecStart=/init.sh
Restart=on-failure
RestartSec=2
[Install]
WantedBy=multi-user.target' >/etc/systemd/system/init.service
systemctl enable init

# everything later is about git, if no enough time, then stop here and start system
printf "CHECKPOINT (GENERIC DESKTOP)?"; read


# ------- ssh key and git repo setup

su ken -c "
mkdir /home/ken/.ssh
ssh-keygen -t rsa -b 4096 -f /home/ken/.ssh/id_rsa"
ssh-copy-id -i /home/ken/.ssh/id_rsa.pub $sshtarget
printf "is everything ok?"; read

git config --system user.email no-reply@princeton.edu
git config --system user.name ken
printf "private repo encrypt and salt"; read temp1 temp2
repo_locations='/home/ken/open
/home/ken/private
/home/ken/clips'

# use ssh key to setup repo, any $() that stricitly require ken must escape $
su ken -c "
eval \$(ssh-agent)
ssh-add /home/ken/.ssh/id_rsa
# public key of server is required to avoid fingerprint prompt
ssh-keyscan $server >/home/ken/.ssh/known_hosts

while IFS= read -r repo
do
	mkdir -p \$repo
	cd \$repo
	git init
	git remote add origin ssh://$sshtarget\$repo
	
	if [[ \$repo == '/home/ken/private' ]]
	then
		# https://gist.github.com/polonskiy/7e5d308ca6412765927a96bd74601a5e
		printf \"%s\n    %s\n    %s\n    %s\n%s\n    %s\n\" \"[filter \\\"openssl\\\"]\" \"clean = openssl aes-256-cbc -k $temp1 -S $temp2 2>/dev/null\" \"smudge = openssl aes-256-cbc -d -k $temp1 2>/dev/null\" \"required\" \"[diff \\\"openssl\\\"]\" \"textconv = openssl aes-256-cbc -d -k $temp1 -in \\\"\\\$1\\\" 2>/dev/null || cat\" >>/home/ken/private/.git/config
		
		chmod 600 /home/ken/private/.git/config
		echo '* filter=openssl  diff=openssl' >/home/ken/private/.git/info/attributes
		
		cp -r /home/ken/private/.config /home/ken/
	fi 

	if [[ \$repo != '/home/ken/clips' ]]
	then	
		git fetch origin master
		git reset --hard origin/master
	fi

done <<<\"$repo_locations\"
chmod 744 /home/ken/open/sync.sh"

printf "CHECKPOINT (PERSONAL DEKSTOP)?"; read

exit
