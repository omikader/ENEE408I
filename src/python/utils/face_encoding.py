import os
import face_recognition

def get_face_encodings():
    known_face_encodings = []
    known_face_names = []

    for fn in os.listdir('img/'):
        image = face_recognition.load_image_file(fn)
        encoding = face_recognition(image)[0]
        known_face_encodings.append(encoding)
        if fn.startswith('omar'):
	    known_face_names.append('Omar')
        elif fn.startswith('tauqir'):
            known_face_names.append('Tauqir')
        else:
            known_face_names.append('Renee')

    return known_face_encodings, known_face_names

