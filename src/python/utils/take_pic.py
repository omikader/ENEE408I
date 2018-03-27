import cv2

def main():
    camera = cv2.VideoCapture(1)

    ramp_frames = 30

    for i in xrange(ramp_frames):
        ret, frame = camera.read()

    while(True):
        cv2.imshow('image', frame)
        if cv2.waitKey(1) & 0xFF == ord('y'):
            cv2.imwrite('../img/omar.png', frame)
            cv2.destroyAllWindows()
            break

    camera.release()

if __name__ == "__main__":
    main()

