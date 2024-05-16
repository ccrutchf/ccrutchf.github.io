---
layout: post
title: Virtual Machines on Android 14 using KVM
subtitle: 
cover-img:
thumbnail-img: 
share-img: 
tags: [android, virtual machine, kvm, crosvm]
---

Throughout this post, I will document the process that was taken to run Ubuntu 22.04 on a Pixel 6A running Android 14.  I leveraged an x86_64 Ubuntu 22.04 machine for this work. `$` will be commands to run on your technician machine. `#` will be commands to run with `su` on the Android phone using a tool like `adb shell` or `termux`.

## Install dependencies
```
$ sudo apt install adb fastboot build-essential debootstrap qemu-user-static
$ rm -rf /usr/local/go && tar -C /usr/local -xzf go1.21.5.linux-amd64.tar.gz
```
Add this to your `~/.bashrc`
```
export PATH=$PATH:/usr/local/go/bin
```

## Root the device
Follow the guide [here](https://topjohnwu.github.io/Magisk/install.html) to root the device.

## Enable KVM
On Pixel 6A, pKVM is not enabled by default.
```
$ adb reboot bootloader
$ fastboot oem pkvm enable
$ fastboot reboot
```

## Build the kernel
Grab a kernel tarball from [kernel.org](https://www.kernel.org/).
```
$ tar -xvf linux-x.x.xx.tar.xz
$ cd linux-x.x.xx
$ make ARCH=arm64 defconfig
```
Enable `CONFIG_VSOCKETS`
```
$ CROSS_COMPILE=aarch64-linux-gnu- make ARCH=arm64 -j 8
```

## Cross-compile gVisor Proxy for aarch64
```
git clone https://github.com/containers/gvisor-tap-vsock gvisor-tap-vsock-arm64
GOARCH=arm64 make
```

## Cross-compile gVisor Proxy for Android
```
git clone https://github.com/containers/gvisor-tap-vsock gvisor-tap-vsock-android
GOOS=android GOARCH=arm64 make
```

## Create a rootfs
```
$ mkdir vm-host
$ truncate -s 100G vm-host.ext4
$ mkfs.ext4 vm-host.ext4
$ sudo mount vm-host.ext4 vm-host
$ sudo truncate -s 99G ./vm-host/ubuntu-rootfs.ext4
$ sudo mkfs.ext4 ./vm-host/ubuntu-rootfs.ext4
$ sudo mount ./vm-host/ubuntu-rootfs.ext4 ubuntu-rootfs
$ sudo debootstrap --arch=arm64 jammy ubuntu-rootfs
$ echo "android-vm" | sudo tee ./ubuntu-rootfs/etc/hostname
$ sudo mkdir -p ./ubuntu-rootfs/etc/systemd/resolved.conf.d/
$ sudo vim ./ubuntu-rootfs/etc/systemd/resolved.conf.d/dns_servers.conf
```

Set the value to the following
```
[Resolve]
DNS=8.8.8.8 1.1.1.1
```

```
$ sudo chroot ./ubuntu-rootfs /bin/bash
$ useradd -m -g sudo <username>
$ passwd <username>
$ chsh -s /bin/bash <username>
$ exit
$ sudo mkdir -p ./ubuntu-rootfs/gvisor-tap-vsock
$ sudo cp -r ./gvisor-tap-vsock-arm64/bin/* ./ubuntu-rootfs/gvisor-tap-vsock
$ sudo mkdir -p ./vm-host/gvisor-tap-vsock
$ sudo cp -r ./gvisor-tap-vsock-android/bin ./vm-host/gvisor-tap-vsock
$ sudo umount ./ubuntu-rootfs
$ sudo umount ./vm-host
```

## Prep the package
```
$ mkdir -p kvm/vm-host
$ mv vm-host.ext4 kvm
$ cp ./linux-x.x.xx/arch/arm64/boot/Image kvm
$ tar -cvf kvm.tar.gz ./kvm -I "pigz -9"
```

## Prep the phone
```
$ adb push kvm.tar.gz /storage/emulated/0
# cd /storage/emulated/0
# tar -xvf kvm.tar.gz
# cd /storage/emulated/0/kvm
# mount vm-host.ext4 vm-host
# /storage/emulated/0/kvm/vm-host/gvisor-tap-vsock/bin/gvproxy -debug -listen vsock://:1024 -listen unix:///storage/emulated/0/kvm/vm-host/network.sock
```
In a second terminal
```
# /apex/com.android.virt/bin/crosvm run --disable-sandbox -p 'init=/sbin/init' --rwroot /storage/emulated/0/kvm/vm-host/ubuntu-rootfs.ext4 /storage/emulated/0/kvm/Image --vsock 3 --mem 4096 --cpus 4
# sudo /gvisor-tap-vsock/bin/gvforwarder -debug &
# ping 8.8.8.8
```
