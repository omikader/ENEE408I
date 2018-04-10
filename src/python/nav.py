import numpy as np
import cv2

from utils.states import States

import utils.arduino as au
import utils.face_encoding as feu

# import imutils
import face_recognition

# Global Variables
PORT = '/dev/ttyACM0'
camera = cv2.VideoCapture(1)

def main():
    s = au.connect(PORT)

    # Face Regions 0-128 FL; 128-256 SL; 256-384 FF; 384-512 SR; 512-640 FR;
    known_face_encodings, known_face_names = feu.get_face_encodings()

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        ret, frame = camera.read()
	#width, height = frame.shape[:2]

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
                name = "Unknown"

                # If a match is found in known_face_encodings, just use the first one
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        x = 0
	y = 0

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale face locations back up since the frame was originally scaled down to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

	    if name == 'Omar':
	        x = (left + right)/2
                y = (top + bottom)/2

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.cv.CV_FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        if x < 128:
            command = States.FL
	elif x < 256:
            command = States.SL
	elif x < 384:
            command = States.FF
	elif x < 512:
            command = States.SR
	elif x < 640:
            command = States.FR
        else:
            command = States.STOP

        print command

        res = ""
        while res == "":
            res = au.send(s, command)
        print res
            
        # Hit 'q' on the keyboard to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
