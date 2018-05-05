import cv2
import sys

camera = cv2.VideoCapture(1)
ramp_frames = 30

while(True):
    for i in xrange(ramp_frames):
	ret, frame = camera.read()

    cv2.imshow('image', frame)
    k = cv2.waitKey(0)
    if k == ord('y'):
        cv2.imwrite('../img/' + sys.argv[1], frame)
        cv2.destroyAllWindows()
        break
    elif k == ord('n'):
	cv2.destroyAllWindows()
    elif k == ord('q'):
        cv2.destroyAllWindows()
        break

camera.release()

