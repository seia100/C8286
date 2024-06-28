# Importamos las bibliotecas necesarias.
from kafka import KafkaConsumer  # KafkaConsumer para consumir mensajes de Kafka.
import json  # json para deserializar los mensajes recibidos.
import smtplib  # smtplib para enviar correos electrónicos.
from email.message import EmailMessage  # EmailMessage para estructurar el correo electrónico.

# Creamos un consumidor de Kafka que escucha en el tópico 'alerts'.
# Configuramos el servidor de Kafka y especificamos cómo deserializar los valores de los mensajes (de JSON a diccionario).
consumer = KafkaConsumer('alerts', 
                         bootstrap_servers=['kafka:9092'],  # Dirección del servidor de Kafka.
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))  # Deserialización del mensaje.

# Definimos una función para enviar alertas por correo electrónico.
def send_email_alert(alert):
    # Creamos un objeto EmailMessage y configuramos el contenido del correo.
    msg = EmailMessage()
    msg.set_content(json.dumps(alert, indent=2))  # El contenido del correo será el alerta en formato JSON, con sangría para mejor lectura.
    
    # Configuramos el asunto del correo electrónico.
    msg['Subject'] = f"DIDS Alert: {alert['type']}"  # El asunto del correo incluye el tipo de alerta.
    
    # Configuramos el remitente y el destinatario del correo electrónico.
    msg['From'] = "luiss.arenast@gmail.com"  # Dirección de correo del remitente.
    msg['To'] = "admin@example.com"  # Dirección de correo del destinatario.

    # Creamos una conexión SMTP con el servidor de correo local.
    s = smtplib.SMTP('localhost')  # Conexión al servidor SMTP local.
    s.send_message(msg)  # Enviamos el mensaje.
    s.quit()  # Cerramos la conexión SMTP.

# Iniciamos un bucle para consumir mensajes de Kafka.
for message in consumer:
    alert = message.value  # Obtenemos el valor del mensaje (la alerta deserializada).
    send_email_alert(alert)  # Enviamos la alerta por correo electrónico.
    # Aquí también podrías implementar otras formas de notificación como Slack, SMS, etc.
