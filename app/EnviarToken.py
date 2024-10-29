from itsdangerous import URLSafeTimedSerializer
from .config import Config

s = URLSafeTimedSerializer(Config.SECRET_KEY)

def generar_token(correo):

    return s.dumps(correo, 
                   salt = "token-activacion")


def verificar_token(token, max_age=3000):
    
    try:
        correo = s.loads(token, salt="token-activacion", max_age=max_age)
        return correo
    except Exception as e:
        return None
