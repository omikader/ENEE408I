import serial
from time import sleep

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
    
    #resp = serial_obj.read(8)
    #return resp

