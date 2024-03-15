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
