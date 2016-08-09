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
- [NIST Testing](#nist-testing)
- [Mobile Application](#mobile-application)
- [Configuration](#configuration)
- [Contributions](#contributions)
- [License](#license)

## Image Processing

### Raspberry Pi Setup

#### Install OpenCV
For this project we used a raspberry pi 3 and installed openCV 3, any raspberry pi and openCV version 
should work (installation took me about 6 hours). I used this tutorial from [Adrian Roseblock](http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/)
to help me install openCV on the Pi.

#### Install BitStream
For this project we used the python package Bitstream 2.0.3. Information about bitstream can be located [here](https://pypi.python.org/pypi/bitstream/2.0.3). Please follow the instructions from that website.

### Raspberry Pi Build
At this point we should have all dependencies installed on the raspberry pi, so go ahead and clone this repo

```
git clone https://github.com/FishyByte/SushiRNG.git
```

For the raspberry pi we only care about the `rpi` directory. Before we can fire up the openCV script we're going to
need to tweak the color ranges in `rpi/app.py`. Grab some still images from the pi with the `raspistill` command and then
use the provided range detector script to find the HSV color space range of the image, this is how the fish will be tracked.

```
cd rpi/testing
python range-detector -f HSV -i path/to/image.jpg
```

Take note of these values and adjust the color range param to match in the `rpi/app.py` file. Also while
your in that file find line 97 and uncomment it out, this is turned off for production.

We are finally ready to test out the openCV code, make sure you are in the `rpi` directory and run
```
python app.py
```

## Server

### Server Setup

### Server Build

## NIST Testing
To test against our random numbers that we generate and make sure it's crypographically secure we used the official NIST
Testing Suite. (Credits to [National Institute of Standards and Technology](http://csrc.nist.gov/groups/ST/toolkit/rng/stats_tests.html))
This runs specific tests against a stream of binary bits that we have generated from our algorithm for randomness.
To run these tests against your bits of data, first go the the `NIST` directory and run this command:

---NOTE: It would help to put your data set in the `data` directory---

```
python bitStreamTesting.py __NumberOfBitsToTest__ PATH_TO_FILE
```

Example code that you can try with one of our data sets that comes with this repo:

```
python bitStreamTesting.py 32768 data/fishBits3.txt
```

You can learn more about the statistical NIST Testing, the organization itself, and the NIST Test Suite at the provided link below

[National Institute of Standards and Technology](http://csrc.nist.gov/groups/ST/toolkit/rng/stats_tests.html)
[NIST Statistical Test Suite](http://csrc.nist.gov/groups/ST/toolkit/rng/documentation_software.html)

## Mobile Application
See our application [Fish Fate](https://github.com/FishyByte/FishFate). Which uses
this project to generate random values. 

## Contributions

### Open Source Community
- [Adrian Roseblock](https://github.com/jrosebr1)
- [National Institute of Standards and Technology](http://csrc.nist.gov/groups/ST/toolkit/rng/stats_tests.html)
	- [Andrew Rukhin, Elaine Barker, & Larry Bassham](http://csrc.nist.gov/groups/ST/toolkit/rng/contacts.html)

### Contact Information
To contact any specific member of the FishyByte team please refer to their personal github profiles.
- [Matthew O'Brien](https://github.com/obriematt)
- [Chris Asakawa](https://github.com/c-asakawa)
- [Nick McHale](https://github.com/nmchale)
- [Corey Aing](https://github.com/aingc)

## Reporting Issues
Please report all issues on the github [issue tracker](https://github.com/FishyByte/SushiRNG/issues)

## License
[The MIT License](LICENSE)
