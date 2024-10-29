from flask import Flask
from app.correo import registrar_correo_bp
from config import Config, init_firebase

app = Flask (__name__)
app.config.from_object(Config)

init_firebase()
app.register_blueprint(registrar_correo_bp)

if __name__ == '__main__':
    app.run()