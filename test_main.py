__author__ = '1605615'

from firebase import firebase
from User import User

fb = firebase.FirebaseApplication('https://crowdsourcing101-357ca.firebaseio.com/', None)

rs = fb.get('News', None)

print(len(rs))