from flask import Flask
from app.correo import registrar_correo_bp
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(registrar_correo_bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=5000)