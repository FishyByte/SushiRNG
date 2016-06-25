# nemoRNG
Fish tank random number generator.
This project uses a raspberry pi 3 with a camera to create a live stream of my fish tank. This live stream is then used to generate a random number.

## Table of contents
- Installation Guide
    - Raspberry Pi Setup
- Scope
- Configuration
- Contributions
- Features
- License

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
- ### Image Processing
- ### Random Number Generator
- ### Server
- ### Web Application
    - ###### Front-End
    - ###### Back-End
- ### Testing Analysis

This project will be using a camera to livestream Chris' fishtank.
This livestream will be used to generate a binary number to then help
create a random cryptic sequence. Matthew and Nick will be working on
the section that will generate the random cryptic sequence.

## Configuration

## Contributions

## Features

## License
Copyright (c) <2016> <Corey Aing, Christopher Asakawa, Matthew O'Brien, Nicholas Mchale>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.