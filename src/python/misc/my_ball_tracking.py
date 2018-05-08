# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import threading

from states import States
import lib.arduino_utils as au
import lib.firebase_utils as fbu

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(1)
# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])

# Connect to the Arduino
port = '/dev/ttyACM0'
serial_obj = au.connect(port)
prevCommand = States.FL
command = States.FR

# Use frame width and heights to define face regions
frame_width = camera.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
frame_height = camera.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
regions = [float(i) * frame_width / 5 for i in range(1, 6)]

idx = 0
# keep looping
while True:
    # Query Firebase for instruction
    if idx % 50 == 0:   
        instruction = fbu.get_instruction()

    idx = idx + 1
        
    # grab the current frame
    (grabbed, frame) = camera.read()

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
       	break

    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
	# find the largest contour in the mask, then use
	# it to compute the minimum enclosing circle and
	# centroid
	c = max(cnts, key=cv2.contourArea)
	((x, y), radius) = cv2.minEnclosingCircle(c)
	M = cv2.moments(c)
	center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if x < regions[0]:
            command = States.FL
        elif x < regions[1]:
            command = States.SL
        elif x < regions[2]:
            command = States.FF
        elif x < regions[3]:
            command = States.SR
        elif x < regions[4]:
            command = States.FR
        else:
            command = States.NA

	# only proceed if the radius meets a minimum size
	if radius > 10:
	    # draw the circle and centroid on the frame,
	    # then update the list of tracked points
	    cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
	    cv2.circle(frame, center, 5, (0, 0, 255), -1)

    # update the points queue
    pts.appendleft(center)

    # loop over the set of tracked points
    for i in xrange(1, len(pts)):
	# if either of the tracked points are None, ignore
	# them
	if pts[i - 1] is None or pts[i] is None:
	    continue

        # otherwise, compute the thickness of the line and
	# draw the connecting lines
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
	cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    if not instruction:
        command = States.NA

    if instruction['Follow'] == 'Stop':
        command = States.STOP
   
    if prevCommand != command or command == States.STOP:
        au.send(serial_obj, command)
	#send_thread = threading.Thread(target=au.send, args=(serial_obj, command,))
	#send_thread.start()
	prevCommand = command
        
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
	break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
