import json
from firebase import firebase

def get_instruction():
    app = firebase.FirebaseApplication('https://i-robot-f4a0c.firebaseio.com/', None)
    result = app.get('/', None)
    
    return result.values()[0]
    #return result.values()[0].values()[0]
