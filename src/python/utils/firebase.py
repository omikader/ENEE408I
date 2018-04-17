import json
from firebase import firebase

app = firebase.FirebaseApplication('https://i-robot-f4a0c.firebaseio.com/', None)
result = app.get('/', None)

print result.values()[0].values()[0]
