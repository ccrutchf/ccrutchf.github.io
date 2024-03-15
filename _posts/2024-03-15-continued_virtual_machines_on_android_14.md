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