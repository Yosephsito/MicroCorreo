import json
import firebase_admin
from firebase_admin import credentials, firestore
from .config import Config

def IniciarBaseDedatos():
    cred = credentials.Certificate(json.loads(Config.FIREBASE_JSON))
    firebase_admin.initialize_app(cred)
    return firestore.client()

db = IniciarBaseDedatos()