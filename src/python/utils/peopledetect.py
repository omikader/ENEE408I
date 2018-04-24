import numpy as np
import cv2


def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh

def intersects(self, other):
    return not (self.top_right.x < other.bottom_left.x or self.bottom_left.x > other.top_right.x or self.top_right.y < other.bottom_left.y or self.bottom_left.y > other.top_right.y)
    

def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (255, 255, 255), thickness)


if __name__ == '__main__':

    hog = cv2.HOGDescriptor()
    #upperBody_cascade = cv2.CascadeClassifier('haarcascade_upperbody.xml')
    #fullBody_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')    
    #lowerBody_cascade = cv2.CascadeClassifier('haarcascade_lowerbody.xml')
    hs_cascade = cv2.CascadeClassifier('HS.xml')    
    #hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
    cap=cv2.VideoCapture(0)
    while True:
        _,frame=cap.read()
        h, w = frame.shape[:2]
        print(h)
        print(w)
        arrBody = hs_cascade.detectMultiScale(frame)
        if arrBody[0] != ():
            (x,y,w,h) = arrBody[0]
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,0),2)
        #found,w=hog.detectMultiScale(frame, winStride=(8,8), padding=(32,32), scale=1.1)
        #draw_detections(frame,found)
        cv2.imshow('feed',frame)
        ch = 0xFF & cv2.waitKey(1)
        if ch == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
