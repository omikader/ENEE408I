import serial
from time import sleep

def connect(port):
    conn = False
    while not conn:
        try:
            s = Serial(port=port, baudrate=9600, timeout=5)
            conn = True
        except:
            print('Attempting to connect to the Arduino...')
            time.sleep(1)
    return s

def send(serial_obj, command):
    print('Instructing the Ardunio to %s ...' % command.name)
    serial_obj.write(bytes(command))
    
    # Response is buffered, wait for response
    time.sleep(2)
    
    resp = serial_obj.read(serial_obj.inWaiting())
    return resp
