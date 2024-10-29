import smtplib
from email.mime.text import MIMEText
from .config import Config

def enviar_correo(destinatario, asunto, cuerpo):
    
    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    servidor.starttls()
    servidor.login(Config.EMAIL_USER, 
                   Config.EMAIL_PASSWORD)

    # Crear el mensaje
    mensaje = MIMEText(cuerpo)
    mensaje['From'] = Config.EMAIL_USER
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto

    # Enviar el correo
    servidor.sendmail(Config.EMAIL_USER, 
                      destinatario, 
                      mensaje.as_string())
    servidor.quit()
