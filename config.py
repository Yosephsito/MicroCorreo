import os 
import json
from firebase_admin import credentials, initialize_app

class Config: 
    SECRET_KEY = os.getenv('SECRET_KEY')
    FIREBASE_JSON = json.loads(os.getenv('FIREBASE_JSON'))
    EMAIL_USER = os.getenv('EMAIL_USER')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')


def init_firebase():
    cred = credentials.Certificate(Config.FIREBASE_JSON)
    initialize_app(cred)




