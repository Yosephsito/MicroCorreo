from flask import Blueprint, request, jsonify, url_for, current_app

from .Firebase import db

from .EnviarToken import generar_token, verificar_token
from .Enviar_correo import enviar_correo

registrar_correo_bp = Blueprint('registrar_correo_bp', __name__)

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

    doc_ref = db.collection('Usuarios').document(correo)
    if doc_ref.get().exists:
       return jsonify({'sucess': False,
                       'message': 'El cooreo ya existe'})
    

    DatosTemporales[correo]={
        'tipo': tipo,
        'nombre': nombre,
        'contraseña': contraseña,
        'estado': estado
    }

    # Generar el token para activación de la cuenta
    token = generar_token(correo)

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

    correo = verificar_token(token)

    if not correo:
        return jsonify({'sucess': False,
                        'message': 'Token invalido o expirado'})
    
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