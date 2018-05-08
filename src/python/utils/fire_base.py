from firebase import firebase
import json

def get_instruction():
    app = firebase.FirebaseApplication('https://i-robot-f4a0c.firebaseio.com/', None)
    result = app.get('/', None)
    
    return result.values()[0]
    #return result.values()[0].values()[0]
