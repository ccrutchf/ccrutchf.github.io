---
layout: post
title: (Continued) Virtual Machines on Android 14 using KVM
subtitle: 
cover-img:
thumbnail-img: 
share-img: 
tags: [android, virtual machine, kvm, crosvm]
---

Throughout this post, I will document the process that was taken to run Ubuntu 22.04 on a Pixel Fold running Android 14 as an extension of [the previous post](/2024-01-05-virtual_machines_on_android_14_using_KVM/).  I leveraged an x86_64 Ubuntu 22.04 machine for this work. `$` will be commands to run on your technician machine. `#` will be commands to run with `su` on the Android phone using a tool like `adb shell` or `termux`.

The primary goal of this is to be able to run the VM on the device without `adb` connected.  LIkewise, we aim to be able to `ssh` into the device.  Finally, the VM should be able to run `docker`.

## Mount Directories
```
$ sudo mount kvm/vm-host.ext4 vm-host
$ sudo mount ./vm-host/ubuntu-rootfs.ext4 ubuntu-rootfs
```

## Install Linux Kernel Modules
```
$ cp -r linux ./ubuntu-rootfs
$ chroot ./ubuntu-rootfs /bin/bash
$ apt install build-essential
$ cd /linux
$ make install
$ cd /
$ apt remove build-essential
$ rm -rf /linux
$ exit
```

## Start VM Network Proxy at Boot
```
$ sudo vim ./ubuntu-rootfs/lib/systemd/system/gvisor-network-proxy.service
```

Set the value to the following
```
[Unit]
Description=gvisor network proxy
After=network.target

[Service]
ExecStart=/gvisor-tap-vsock/bin/gvforwarder
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```
$ sudo chroot ./ubuntu-rootfs /bin/bash
$ systemctl enable my-service
$ exit
```

## Creating Android Scripts
Download curl-aarch64 from https://github.com/moparisthebest/static-curl and place it into the `vm-host` directory.
```
$ cd ./vm-host
$ sudo chmod +x ./curl-aarch64
$ sudo vim ./start-network.sh
```

Set the value to the following
```
#! /system/bin/sh

/storage/emulated/0/kvm/vm-host/gvisor-tap-vsock/bin/gvproxy -listen vsock://:1024 -listen unix:///storage/emulated/0/kvm/vm-host/network.sock &
sleep 1
./curl-aarch64  --unix-socket /storage/emulated/0/kvm/vm-host/network.sock http:/unix/services/forwarder/expose -X POST -d '{"local":":22","remote":"192.168.127.2:22"}'
```

```
$ sudo chmod +x ./start-network.sh
$ sudo vim ./start-vm.sh
```

Set the value to the following
```
#! /system/bin/sh

/apex/com.android.virt/bin/crosvm run --disable-sandbox -p 'init=/sbin/init' --rwroot /storage/emulated/0/kvm/vm-host/ubuntu-rootfs.ext4 /storage/emulated/0/kvm/Image --vsock 3 --mem 10240 --cpus 10
```

```
$ sudo chmod +x ./start-vm.sh
```

## Unmount Directories
``
$ umount ./ubuntu-rootfs
$ umount ./vm-host
``

## Prep the package for the phone
```
$ tar -cvf kvm.tar.gz ./kvm -I "pigz -9"
```

## Prep the phone
```
$ adb push kvm.tar.gz /storage/emulated/0
# cd /storage/emulated/0
# tar -xvf kvm.tar.gz
# cd /storage/emulated/0/kvm
# mount vm-host.ext4 vm-host
# ./start-network.sh
```

Disconnect the phone from usb.  Install `Termux` from `F-Droid`.  In `Termux`:
```
# cd /storage/emulated/0/kvm/vm-host
# ./start-vm.sh
```

## SSH into the Phone
Grab the IP Address of the phone from its setting page.

On your technician machine, `ssh <user>@<phone IP>`.  You should be connected to a machine with the hostname `android-vm`.