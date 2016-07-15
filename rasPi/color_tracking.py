# import the necessary packages
from collections import deque
import imutils
import cv2
from fish_pool import *

# import picamera
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import timeit

# call constructors
fish_stream = FishStream()
fish_pool = FishPool()

# output bitstream to file
test_output = open('fishData/fishBits.txt', 'w')
test_output.truncate()

# define the lower and upper boundaries of the "pink"
# fish in the HSV color space, then initialize the
# list of tracked points
orangeLower = (0, 215, 37)
orangeUpper = (255, 255, 255)
pts = deque(maxlen=64)

# init pi camera
camera = PiCamera()
camera.vflip = True
camera.hflip = True
camera.resolution = (640, 368)
camera.framerate = 60
camera.exposure_mode='verylong'
rawCapture = PiRGBArray(camera, size=(640, 368))
    
# allow camera warmup
time.sleep(0.3)

# testing variables
totalBits = 1024  #131072 = 2^17 bits
printLength = 64
lineCount = totalLines = totalBits / printLength
start = timeit.timeit()

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
   
    # grab the raw NumPy array representing the image 
    frame = frame.array

    # resize the frame, blur it, and convert it to the HSV color space
    frame = imutils.resize(frame, width=640)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, orangeLower, orangeUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:

        # lets count the fishies on the screen
        fish_count = 0    
        x_compare = -1
        y_compare = -1

        first_bit = 0
        second_bit = 0
        
        # loop through all the contours in the mask
        for c in cnts:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum  and max size
            if radius > 10: 
                # if a video path was not supplied, grab the reference:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (255, 0, 255), -1)

                
                # where are the fish at now?
                fish_count += 1
                fish_stream.add_position(fish_count, x, y)
                # print "fish#:", fish_count, "x:", x, "y:", y

            # update the points queue
            pts.appendleft(center)

    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in prep for next frame
    rawCapture.truncate(0)
    
    # testing: finished gathering bits, write out to file
    if fish_stream.get_length() > totalBits:
        for j in range(0, lineCount):
            for i in range(0, 8):
                test_output.write(" ")
                test_output.write(str(fish_stream.get_bits(8)))
            test_output.write("\n")

        end = timeit.timeit()
        print "--------------------------------------------------"
        print "--------------------------------------------------"
        print end - start, "seconds to receive", totalBits, "bits",
        print "--------------------------------------------------"
        break



    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        test_output.write(str(fish_stream.stream))
        test_output.write("\n")
        break
    
    if key == ord("p"):
        zero_prob, one_prob = fish_stream.get_probabilities()
        zero = fish_stream.add_zero()
        one = fish_stream.one_count()

        print "--------------------------------------------------"
        print "0:", zero, "/", zero + one, "=", zero_prob
        print "1:", one, "/", zero + one, "=", one_prob
        print "--------------------------------------------------"

# cleanup the camera and close any open windows
cv2.destroyAllWindows()
