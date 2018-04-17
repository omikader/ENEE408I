import json
#firebase code 
#that will send commands from the alexa to firebase
#these commands will be parsed by the jetson and then will trigger the arduino
#to move the robot accordingly
from firebase import firebase
firebase = firebase.FirebaseApplication('https://i-robot-f4a0c.firebaseio.com/', None)
result = firebase.get('/', None)
print result.values()[0].values()[0]
#print result['OmarCommand']
#current_request = json.load(result)
#current_request['OmarCommand']


