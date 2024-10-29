from flask import Blueprint, request, jsonify, url_for, current_app

import firebase_admin
from firebase_admin import credentials, firestore

import smtplib
from email.mime.text import MIMEText
from itsdangerous import URLSafeTimedSerializer

from .Enviar_correo import enviar_correo

# Instalar
# # pip install firebase-admin
# install itsdangerous
# npm install -g firebase-tools

registrar_correo_bp = Blueprint('registrar_correo_bp', __name__)

# Configuración con firebase

db = firestore.client()

# Inicialización del serializador para generar tokens
s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

DatosTemporales = {}

@registrar_correo_bp.route('/registrar_correo', methods=['POST'])
def registrar_correo():

    # Obtener los datos enviados desde el cliente
    data = request.get_json()
    correo = data.get('Correo')
    tipo = data.get('Tipo', 'Usuario')
    nombre = data.get('Nombre')
    contraseña = data.get('Contraseña')
    estado = data.get('Estado', True)

    # Verificar si el correo ya existe en firebase
    ReferenciasDeUsuario = db.collection('Usuarios').document(correo)

    usuario_existente = ReferenciasDeUsuario.get()

    if usuario_existente.exists:
        return jsonify({'success': False, 
                        'message': 'El correo ya existe'})

    DatosTemporales[correo]={
        'tipo': tipo,
        'nombre': nombre,
        'contraseña': contraseña,
        'estado': estado
    }

    # Generar el token para activación de la cuenta
    token =  s.dumps(correo, 
                   salt="token-activacion")

    url_activacion = url_for('registrar_correo_bp.activar_cuenta', 
                             token=token, 
                             _external=True)
    
    asunto = "Activa tu cuenta"
    cuerpo = f"Por favor haz clic en el siguiente enlace para activar tu cuenta: {url_activacion}, con nombre {nombre} contraseña {contraseña}"
    # Enviar el correo con el token
    enviar_correo(correo, asunto, cuerpo)

    return jsonify({'success': True, 
                    'message': 'Correo de activación enviado'})


@registrar_correo_bp.route('/activar/<token>', methods=['GET'])
def activar_cuenta(token):

 try:
    try:
        # Verificar el token y obtener el correo asociado
        correo = s.loads(token, 
                         salt="token-activacion", 
                         max_age=3000)  # El token expira en 5 minutos
    except:
        return jsonify({'success': False, 
                        'message': 'Token inválido o expirado'})
    
    #obtener los datos del usuario almacenados temporalmente
    InfoUsuario= DatosTemporales.pop(correo, None)

    if InfoUsuario is None:
        return jsonify({'sucess': False, 
                        'message': 'No se encontraron datos para este correo'})

    db.collection('Usuarios').document(correo).set({

        'Correo': correo,
        'Tipo': InfoUsuario['tipo'],
        'Nombre': InfoUsuario['nombre'],
        'Contraseña': InfoUsuario['contraseña'],
        'Estado': InfoUsuario['estado']
    })

    return jsonify({'success': True, 'message': 'Cuenta activada exitosamente'})

 except Exception as e:
    return jsonify({'sucess': False, 'message': str(e)})