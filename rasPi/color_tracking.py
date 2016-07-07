# import the necessary packages
from collections import deque
import argparse
import imutils
import cv2

# import picamera
from picamera.array import PiRGBArray
from picamera import PiCamera
import time


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "pink"
# fish in the HSV color space, then initialize the
# list of tracked points
orangeLower = (0, 195, 63)
orangeUpper = (20, 255, 255)
pts = deque(maxlen=args["buffer"])

# init pi camera
camera = PiCamera()
camera.vflip = True
camera.hflip = True
camera.resolution = (640, 368)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 368))
    
# allow camera warmup
time.sleep(0.3)



# keep looping
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the current frame
    # (grabbed, frame) = camera.read()
    
    frame = frame.array
    


    # if we are viewing a video and we did not grab a fpythrame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break

    # resize the frame, blur it, and convert it to the HSV
    # color space
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
        # loop through all the contours in the mask
        for c in cnts:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum  and max size
            if radius > 13:
                # if a video path was not supplied, grab the reference:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (255, 0, 255), -1)

            # update the points queue
            pts.appendleft(center)

    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in prep for next frame
    rawCapture.truncate(0)

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
cv2.destroyAllWindows()
