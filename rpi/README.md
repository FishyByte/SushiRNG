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
