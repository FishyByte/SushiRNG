# SushiRNG
Fish tank random number generator.
This project uses a Raspberry Pi 3 with a camera to create a live stream of my fish tank. This live stream is then used to generate a random number.

## Table of Contents
- [Installation Guide](https://github.com/FishyByte/SushiRNG/tree/readme#installation-guide)
    - [Raspberry Pi Setup](https://github.com/FishyByte/SushiRNG/tree/readme#raspberry-pi-setup)
- [Scope](https://github.com/FishyByte/SushiRNG/tree/readme#scope)
    - [Image Processing](https://github.com/FishyByte/SushiRNG/tree/readme#--image-processing)
    - [Random Number Generator](https://github.com/FishyByte/SushiRNG/tree/readme#--random-number-generator)
    - [Server](https://github.com/FishyByte/SushiRNG/tree/readme#--server)
    - [Web Application](https://github.com/FishyByte/SushiRNG/tree/readme#--web-application)
        - Front-End
        - Back-End
    - [Testing Analysis](https://github.com/FishyByte/SushiRNG/tree/readme#--testing-analysis)
- [Configuration](https://github.com/FishyByte/SushiRNG/tree/readme#configuration)
- [Contributions](https://github.com/FishyByte/SushiRNG/tree/readme#contributions)
- [Features](https://github.com/FishyByte/SushiRNG/tree/readme#features)
- [License](https://github.com/FishyByte/SushiRNG/tree/readme#license)

## Installation Guide
- #### Raspberry Pi Setup
For this project a raspberry pi 3 is used, this pi is flashed with Rasbian. Complete the following steps on the raspberry pi.

1.  The installation requires pip to be installed on the raspberry pi
    ```
    sudo apt-get install python-pip
    ```

2.  Install picamera
    ```
    sudo pip install picamera
    ```

3.  Install flash python library
    ```
    sudo pip install flask
    ```

4.  Clone the repository
    ```
    git clone https://github.com/pdxFinding/nemoRNG.git
    ```

5.  Test the pi camera locally.

    First we need to get your ip for the raspberry pi by running: 
    ```
    ifconfig
    ```
    look for inet adder and take note of it.
    
    Now we can run the app by running this command: 
    ```
    python app.py
    ```
    This should produce this output:
    ```
    pi@raspberrypi:~/nemoRNG $ python app.py 
    * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
    * Restarting with stat
    * Debugger is active!
    * Debugger pin code: 205-279-976
    ``` 
    
    While the app is running enter this url into your preferred browser.
    ```
    http://<your pi's ip>:5000
    ```

## Scope
### - Image Processing
### - Random Number Generator
### - Server
### - Web Application
    Front-End:
    
    Back-End:
    
### - Testing Analysis

This project will be using a camera to livestream Chris' fishtank.
This livestream will be used to generate a binary number to then help
create a random cryptic sequence. Matthew and Nick will be working on
the section that will generate the random cryptic sequence.

## Configuration

## Contributions
- [Adrian Roseblock](https://github.com/jrosebr1)

## Features

## License
[The MIT License](LICENSE)