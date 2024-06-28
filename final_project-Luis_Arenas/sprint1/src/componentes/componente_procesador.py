from kafka import KafkaConsumer, KafkaProducer  # Importa KafkaConsumer y KafkaProducer de la librería kafka-python
import json  # Importa la librería JSON para serializar y deserializar los datos

# Configura el consumidor de Kafka para leer mensajes del tópico 'raw_packets'
# La opción value_deserializer deserializa los valores desde JSON y los decodifica en UTF-8
consumer = KafkaConsumer('raw_packets', bootstrap_servers=['kafka:9092'],
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))

# Configura el productor de Kafka para enviar mensajes al servidor Kafka en 'kafka:9092'
# La opción value_serializer serializa los valores en formato JSON y los codifica en UTF-8
producer = KafkaProducer(bootstrap_servers=['kafka:9092'],
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def preprocess(packet):
    # Lógica de preprocesamiento
    # Por ejemplo, normalización, extracción de características, etc.
    return packet  # Por ahora, simplemente devuelve el paquete sin cambios

# Bucle principal para consumir y procesar mensajes
for message in consumer:
    packet = message.value  # Obtiene el valor del mensaje consumido (el paquete)
    processed_packet = preprocess(packet)  # Preprocesa el paquete utilizando la función preprocess
    producer.send('processed_packets', processed_packet)  # Envía el paquete preprocesado al tópico 'processed_packets' en Kafka
