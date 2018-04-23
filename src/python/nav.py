import cv2
import face_recognition

import utils.arduino as au
import utils.face_encoding as feu
from utils.states import States

# Global Variables
PORT = '/dev/ttyACM0'
camera = cv2.VideoCapture(1)

def main():
    # Connect to the Arduino
    serial_obj = au.connect(PORT)

    # Initialize some variables
    path = 'img/'
    known_face_encodings, known_face_names = feu.get_encodings(path)

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    # Use frame width and heights to define face regions
    width = camera.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
    height = camera.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
    regions = [float(i) * width / 5 for i in range(1, 6)]

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
            command = States.STOP

        res = ""
        while res == "":
            res = au.send(serial_obj, command)
            
        # Hit 'q' on the keyboard to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
