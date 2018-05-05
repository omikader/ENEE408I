import cv2
import face_recognition
import numpy as np
import threading

from states import States
import lib.arduino_utils as au
import lib.firebase_utils as fbu
import lib.facial_recognition_utils as feu

# Define web camera
camera = cv2.VideoCapture(1)

# Connect to the Arduino
port = '/dev/ttyACM0'
serial_obj = au.connect(port)

# Save face encodings from images of Team 8 members
img_path = '/home/nvidia/git/ENEE408I/img/'
known_face_encodings, known_face_names = feu.get_encodings(img_path)

# Use frame width and heights to define face regions
frame_width = camera.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
frame_height = camera.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
regions = [float(i) * frame_width / 5 for i in range(1, 6)]

# Define starting values
face_locations = []
face_encodings = []
face_names = []
hsv_lower = 0
hsv_upper = 0
process_this_frame = True
prevCommand = States.NA

while True:
    # Query Firebase for instruction
    instruction = fbu.get_instruction()

    instruction = True

    if not instruction:
        # If no instruction available, spin idly
        x = 100000000

    elif instruction.keys()[0] == 'Follow':
        # Get name and encodings of person to be followed
        follow = instruction['Follow']
        indices = [i for i, x in enumerate(known_face_names) if x == follow]
        follow_face_encodings = [known_face_encodings[i] for i in indices]
        follow_face_names = [known_face_names[i] for i in indices]

        # Extract frame from video feed and resize for faster processing
        ret, frame = camera.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color to RGB color
        rgb_small_frame = small_frame[:, :, ::-1]

        face_found = False
        
        # Only process every other frame to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(follow_face_encodings, face_encoding)

                # If a match is found in follow_face_encodings, save location
                if True in matches:
                    face_found = True
                    match_index = matches.index(True)
                    (top, right, bottom, left) = face_locations[match_index]
                    break

        process_this_frame = not process_this_frame
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        
        if face_found:
            # Scale face locations back up since the frame was originally scaled down to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            x, y = (left + right)/2, (top + bottom)/2

            if not (hsv_lower and hsv_upper):
                roi = hsv[left:right, (top + 250):(bottom + 250)]
                hue, sat, val = roi[:, :, 0], roi[:, :, 1], roi[:, :, 2]
                h_mean, h_std = np.ndarray.flatten(hue).mean(), np.ndarray.flatten(hue).std()
                s_mean, s_std = np.ndarray.flatten(sat).mean(), np.ndarray.flatten(sat).std()
                v_mean, v_std = np.ndarray.flatten(val).mean(), np.ndarray.flatten(val).std()
                hsv_lower = (h_mean - h_std, s_mean - s_std, v_mean - v_std)
                hsv_upper = (h_mean + h_std, s_mean + s_std, v_mean + v_std)
        else:
            if (hsv_lower and hsv_upper):
                # Construct a mask and perform a series of dilations and erosions to remove
                # any small blobs left in the mask
                mask = cv2.inRange(hsv, hsv_lower, hsv_upper)
                mask = cv2.erode(mask, None, iterations=2)
                mask = cv2.dilate(mask, None, iterations=2)

                # Find contours in the mask
                cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

                # Only proceed if at least one contour was found
                if len(cnts) > 0:
                    # Find the largets contour and use it to compute the min enclosing circle
                    c = max(cnts, key=cv2.contourArea)
                    ((x, y), radius) = cv2.minEnclosingCircle(c)
                    #cv2.circle(frame, (int(x),int(y)),int(radius), (0,255,255),2)
            else:
                x = 1000000000
    
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

    if prevCommand != command:
	send_thread = threading.Thread(target=au.send, args=(serial_obj, command,))
	send_thread.start()
	prevCommand = command

    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
