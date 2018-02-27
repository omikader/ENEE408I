import cv2

def main():
    cascade_path = 'lbpcascade_frontalface.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)
    video_capture = cv2.VideoCapture(1)

    while True:
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = detect_faces(face_cascade, gray)
        draw_rectangles(frame, faces)

        cv2.imshow('Video', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

def detect_faces(casc_path, gray, scaleFactor=1.1, minNeighbors=5):
    return casc_path.detectMultiScale(
        gray,
        scaleFactor,
        minNeighbors
    )

def draw_rectangles(frame, faces):    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

if __name__ == "__main__":
    main()
