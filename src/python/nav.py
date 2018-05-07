import cv2
import face_recognition
import numpy as np
import states
import tplibutils

# Define web camera
camera = cv2.VideoCapture(1)

# Connect to the Arduino
port = '/dev/ttyACM0'
#serial_obj = tplibutils.connect(port)

# Save face encodings from images of Team 8 members
img_path = '/home/nvidia/git/ENEE408I/img/'
known_face_encodings, known_face_names = tplibutils.get_encodings(img_path)

# Use frame width and heights to define face regions
frame_width = camera.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
frame_height = camera.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
regions = [float(i) * frame_width / 5 for i in range(1, 6)]

# Define starting values
hsv_lower = 0
hsv_upper = 0
process_this_frame = True
prev_command = states.States.STOP

while True:
    # Query Firebase for instruction
    #instruction = tplibutils.get_instruction()
    instruction = True

    # If no instruction available, spin idly
    if not instruction:
        command = states.States.NA

    # If instruction is to follow, get name and encodings of person to follow
    elif instruction: #instruction.keys()[0] == 'Follow':
        guide = 'Omar' #instruction['Follow']
        indices = [i for i, x in enumerate(known_face_names) if x == guide]
        guide_face_encodings = [known_face_encodings[i] for i in indices]
        found_guide = False

        # Extract frame from video feed and resize for faster processing
        ret, frame = camera.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color to RGB color
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)

            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(
                    guide_face_encodings, face_encoding)

                # If a match is found in follow_face_encodings, save location
                if True in matches:
                    found_guide = True
                    match_index = matches.index(True)
                    (top, right, bottom, left) = face_locations[match_index]
                    break

        process_this_frame = not process_this_frame
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        if found_guide:
            # Scale face locations back up since the frame was originally scaled
            # down to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, top + 250), (right, bottom + 250), (0, 255, 0), 2)
            x = (left + right)/2

            # Define ROI (region of interest) on guide's shirt
            roi = hsv[(top + 250):(bottom + 250) , left:right]
            hue, sat, val = roi[:, :, 0], roi[:, :, 1], roi[:, :, 2]

            # Define HSV color range of ROI
            h_mean, h_std = np.mean(hue), np.std(hue)
            s_mean, s_std = np.mean(sat), np.std(sat)
            v_mean, v_std = np.mean(val), np.std(val)
            hsv_lower = (h_mean - h_std, s_mean - s_std, v_mean - v_std)
            hsv_upper = (h_mean + h_std, s_mean + s_std, v_mean + v_std)

        else:
            if (hsv_lower and hsv_upper):
                # Construct a mask and perform a series of dilations and
                # erosions to remove any small blobs left in the mask
                mask = cv2.inRange(hsv, hsv_lower, hsv_upper)
                mask = cv2.erode(mask, None, iterations=2)
                mask = cv2.dilate(mask, None, iterations=2)
                
                # Find contours in the mask
                cnts = cv2.findContours(
                    mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

                # Only proceed if at least one contour was found
                if len(cnts) > 0:
                    # Find the largets contour and use it to compute the
                    # minimum enclosing circle
                    c = max(cnts, key=cv2.contourArea)
                    ((x, y), radius) = cv2.minEnclosingCircle(c)
                    cv2.circle(
                        frame, (int(x),int(y)), int(radius), (0,255,255), 2)
            else:
                x = 1000000000

        # Set speed and direction state based on position of x coordinate within
        # the frame
        if x < regions[0]:
            command = states.States.FL
        elif x < regions[1]:
            command = states.States.SL
        elif x < regions[2]:
            command = states.States.FF
        elif x < regions[3]:
            command = states.States.SR
        elif x < regions[4]:
            command = states.States.FR
        else:
            command = states.States.NA

    # Send command to the Arduino only if state has changed
    #if prevCommand != command:
        #tplibutils.send(serial_obj, command)
        #prev_command = command

    # Display results on video frame
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
