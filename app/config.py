import os 
from dotenv import load_dotenv

load_dotenv()
class Config: 
    SECRET_KEY = os.getenv('SECRET_KEY')
    FIREBASE_JSON = os.getenv('FIREBASE_JSON')
    EMAIL_USER = os.getenv('EMAIL_USER')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')




