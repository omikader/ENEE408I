from firebase import firebase
from time import sleep

import face_recognition
import json
import os
import serial

# ARDUINO #

def connect(port):
    conn = False
    while not conn:
        try:
            serial_obj = serial.Serial(port=port, baudrate=9600, timeout=5)
            conn = True
        except:
            print('Attempting to connect to the Arduino...')
            sleep(1)
    return serial_obj

def send(serial_obj, command):
    print('Instructing the Arduino to %s ...' % command.name)
    serial_obj.write(bytes(command.value))

    # Response is buffered, wait for response
    sleep(1)

    resp = serial_obj.read(serial_obj.inWaiting())
    return resp

# FIREBASE #
    
def get_instruction():
    app = firebase.FirebaseApplication('https://i-robot-f4a0c.firebaseio.com/', None)
    result = app.get('/', None)
    
    return result.values()[0]
    #return result.values()[0].values()[0]

# FACE_RECOGNITION #
    
def get_encodings(path):
    known_face_encodings = []
    known_face_names = []

    for fn in os.listdir(path):
        fn = path + fn
        image = face_recognition.load_image_file(fn)

	# Skip image if face not detected in photo
	if not face_recognition.face_encodings(image):
	    continue
 
	encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)

        if 'omar' in fn:
	    known_face_names.append('Omar')
        elif 'tauqir' in fn:
            known_face_names.append('Tauqir')
        else:
            known_face_names.append('Renee')

    return known_face_encodings, known_face_names
