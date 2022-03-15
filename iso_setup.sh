#!/bin/bash

# Ctrl+S to show advanced BIOS in Acer
# setfont solar24x32

# ----------- update iso keyring (in case it is an old build)
pacman -Syy
pacman -S archlinux-keyring --noconfirm


# ----------- create partitions

lsblk
printf "Enter device name, boot_idx, system_idx (both including suffix), g if want a new partition table"; read dname bid sid erase

(
echo $erase
echo n # Add a new partition (EFI)
echo ${bid: -1}  # default next possible partition number
echo   # First sector (Accept default: 1)
echo +35M  # Last sector (Accept default: varies)
echo n # Add a new partition (Main)
echo ${sid: -1}  # default next possible partition number
echo   # First sefdictor (Accept default: 1)
echo   # Last sector (Accept default: varies)
echo w # Write changes
) | fdisk /dev/$dname -w always -W always


# -------------- format boot partition into F32
mkfs.fat -F32 /dev/$dname$bid

# -------------- umount and close mapper in case this is not a fresh run
umount /mnt
umount /dev/mapper/croot
cryptsetup luksClose croot

# ------------ setup crypt mapper to root partition and format it to ext4
cryptsetup -y luksFormat /dev/$dname$sid
cryptsetup open /dev/$dname$sid croot
mkfs.ext4 /dev/mapper/croot
# mkfs.ext4 /dev/$dname$sid
# mount /dev/$dname$sid /mnt
printf "is everything ok?"; read

# ------------ mount the root partition
# ------------ install base package and setup fstab
mount /dev/mapper/croot /mnt
pacstrap /mnt/ base linux linux-firmware
genfstab -U /mnt >/mnt/etc/fstab
# use nano to change pass to 0 in /etc/fstab
nano /mnt/etc/fstab


curl https://raw.githubusercontent.com/SmartestKen/open/master/root_setup.sh --output /mnt/root_setup.sh
sed -i "s/dname=nvme0n1; bid=p1; sid=p2/dname=$dname; bid=$bid; sid=$sid/g" /mnt/root_setup.sh

arch-chroot /mnt
# umount /mnt
