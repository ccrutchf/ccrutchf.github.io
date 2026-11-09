---
layout: post
title: FishSense-Lite Live Demo at the NOAA AI Workshop
subtitle: 5th NOAA Workshop on Leveraging AI in Environmental Sciences
cover-img:
thumbnail-img:
share-img:
tags: [fishsense, e4e, noaa, demo, citizen science]
---

**Update:** You can watch the recording [here](https://ncsu.zoom.us/rec/share/dz9AKmrLh5hxw79GNqa7oPdXIWr4lmVmH0x7PQ_-91CYz9XOa5Fjg5z2uiFk4r0f.07dFy3rVz7Y2pHHR?startTime=1695414619000).

Live demos are always a little nerve-wracking, but this one should be fun. On Friday, September 22, 2023, at 2:30 PM Mountain (1:30 PM Pacific), I'll be walking through FishSense-Lite at the virtual [5th NOAA Workshop on Leveraging AI in Environmental Sciences](https://noaaai2023.sched.com/). The demo is 25 minutes on Zoom, and the [session page](https://noaaai2023.sched.com/event/1SA5J/live-demo-fishsense-lite-a-laser-based-single-camera-system-for-in-situ-fish-length-measurements) has the details.

The plan is to take real photos from our dives with [REEF](https://www.reef.org/) citizen scientists and follow them through the pipeline, from the raw image to a fish length. Each photo has a laser dot on the fish. A neural network finds that dot, and since the laser is rigidly mounted to the camera, the dot's position tells us how far away the fish is. [Fishial](https://www.fishial.ai/)'s models then find the fish's head and tail, and with the distance in hand, the pixels between them become centimeters. From there, we can estimate biomass.

The hardware side is deliberately boring: an Olympus TG-6, a dive laser, and a 3D-printed mount. That is the point. Anyone should be able to build one.
