import smtplib
from email.mime.text import MIMEText
from flask import current_app

def enviar_correo(destinatario, asunto, cuerpo):
    
    remitente = current_app.config['EMAIl_USER']
    contraseña = current_app.config['EMAIL_PASSWORD']
    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    servidor.starttls()
    servidor.login(remitente, contraseña)

    # Crear el mensaje
    mensaje = MIMEText(cuerpo)
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto

    # Enviar el correo
    servidor.sendmail(remitente, destinatario, mensaje.as_string())
    servidor.quit()
