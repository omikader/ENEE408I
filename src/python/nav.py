import numpy as np
import utils.arduino as au
import cv2
from states import States

# import imutils
# import face_recognition

# Global Variables
PORT = 'COM5'

camera = cv2.VideoCapture(1)

def main():
    s = au.connect(PORT)
