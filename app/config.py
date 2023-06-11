import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


#Conexión a base de datos Firebase
cred = credentials.Certificate("app/firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()