#!/bin/bash

dname=nvme0n1; bid=p1; sid=p2

mkdir /efi
mount /dev/$dname$bid /efi

pacman -Syyu --noconfirm

cp /boot/vmlinuz-linux /efi/
# use kernel for console font, equivalent.
sed -i '/^HOOKS=/ s/.*/HOOKS=(base udev autodetect keyboard modconf block encrypt filesystems fsck)/g' /etc/mkinitcpio.conf
mkinitcpio -g /efi/initramfs-linux.img -c /etc/mkinitcpio.conf -k /efi/vmlinuz-linux

umount /efi
rmdir /efi
