import cv2

def main():
    camera = cv2.VideoCapture(1)
    # Number of frames to throw away while the camera adjusts to light levels
    ramp_frames = 30

    for i in xrange(ramp_frames):
        _, temp = camera.read()

    print 'Take image ... '
    _, camera_capture = camera.read()
    file_name = '~/git/ENEE408I/src/python/pics/test_image.png'

    cv2.imwrite(file_name, camera_capture)
    del(camera)

if __name__ == "__main__":
    main()

