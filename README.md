# SushiRNG

![alt tag](https://github.com/FishyByte/FishFate/blob/master/www/img/fishDemo_2.gif?raw=true)

Fish tank random number generator.
This project uses a Raspberry Pi 3 with a camera to create a live stream of my fish tank. This live stream is then used to generate a random number.

## Table of Contents
- [Image Processing](#image-processing)
    - [Raspberry Pi Setup](#raspberry-pi-setup)
    - [Raspberry Pi Build](#raspberry-pi-build)
- [Server](#server)
    - [Server Setup](#server-setup)
    - [Server Build](#server-build)
- [Mobile Application](#mobile-application)
- [Configuration](#configuration)
- [Contributions](#contributions)
- [License](#license)

## Raspberry Pi Setup

### Install OpenCV
For this project we used a raspberry pi 3 and installed openCV 3, any raspberry pi and openCV version 
should work (installation took me about 6 hours). I used this tutorial from [Adrian Roseblock](http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/)
to help me install openCV on the Pi.

### Install BitStream
For this project we used the python package Bitstream 2.0.3. Information about bitstream can be located [here](https://pypi.python.org/pypi/bitstream/2.0.3). Please follow the instructions from that website.

## Mobile Application
See our application [Fish Fate](https://github.com/FishyByte/FishFate). Which uses
this project to generate random values. 

## Contributions

### Open Source Community
- [Adrian Roseblock](https://github.com/jrosebr1)

### Contact Information
To contact any specific member of the FishyByte team please refer to their personal repositories.
- [Matthew O'Brien](https://github.com/obriematt)
- [Chris Asakawa](https://github.com/c-asakawa)
- [Nick McHale](https://github.com/nmchale)
- [Corey Aing](https://github.com/aingc)

## Reporting Issues
Please report all issues on the github [issue tracker](https://github.com/FishyByte/SushiRNG/issues)

## License
[The MIT License](LICENSE)