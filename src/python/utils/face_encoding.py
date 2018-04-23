import os
import face_recognition

def get_encodings(path):
    known_face_encodings = []
    known_face_names = []

    for fn in os.listdir(path):
        fn = path + fn 
        image = face_recognition.load_image_file(fn)
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)

        if 'omar' in fn:
	    known_face_names.append('Omar')
        elif 'tauqir' in fn:
            known_face_names.append('Tauqir')
        else:
            known_face_names.append('Renee')

    return known_face_encodings, known_face_names

