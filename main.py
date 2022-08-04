import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from methods.add import add

## Insert your firebase credentials path here
cred = credentials.Certificate("accountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

add(db)
