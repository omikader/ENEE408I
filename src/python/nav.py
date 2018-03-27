import numpy as np
import cv2

from utils.states import States

import utils.arduino as au
# import imutils
import face_recognition

# Global Variables
PORT = 'COM5'
camera = cv2.VideoCapture(1)

def main():
    #s = au.connect(PORT)
    
    omar_image = face_recognition.load_image_file('img/omar.png')
    omar_face_encoding = face_recognition.face_encodings(omar_image)[0]

    tauqir_image = face_recognition.load_image_file('img/tauqir.jpg')
    tauqir_face_encoding = face_recognition.face_encodings(tauqir_image)[0]

    renee_image = face_recognition.load_image_file('img/renee.png')
    renee_face_encoding = face_recognition.face_encodings(renee_image)[0]

    tauqir2_image = face_recognition.load_image_file('img/tauqir2.jpg')
    tauqir2_face_encoding = face_recognition.face_encodings(tauqir2_image)[0]

    known_face_encodings = [
        omar_face_encoding,
        tauqir_face_encoding,
        renee_face_encoding,
        tauqir2_face_encoding,
    ]

    known_face_names = [
        "Omar",
        "Tauqir",
        "Renee",
        "Tauqir",
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        ret, frame = camera.read()

        # Resize frame to 1/4 size for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color to RGB color
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Barack"

                # If a match is found in known_face_encodings, just use the first one
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale face locations back up since the frame was originally scaled down to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.cv.CV_FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
