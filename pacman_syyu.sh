#!/bin/bash

dname=nvme0n1; bid=p1; sid=p2

mkdir /efi
mount /dev/$dname$bid /efi

pacman -Syy
pacman -S archlinux-keyring --noconfirm
pacman -Syyu --noconfirm

cp /boot/vmlinuz-linux /efi/
# use kernel for console font, equivalent.
sed -i '/^HOOKS=/ s/.*/HOOKS=(base udev autodetect keyboard modconf block encrypt filesystems fsck)/g' /etc/mkinitcpio.conf
mkinitcpio -g /efi/initramfs-linux.img -c /etc/mkinitcpio.conf -k /efi/vmlinuz-linux

umount /efi
rmdir /efi


# to check current kernel version, use
# pacman -Q linux && uname -r
# to install virtualbox (and select option 2 for virtualbox-dkms) and reboot, qt5ct is there for font consistency
# pacman -S linux-headers virtualbox qt5ct
