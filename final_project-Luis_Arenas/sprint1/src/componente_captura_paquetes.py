import scapy.all as scapy  # Importa todas las funcionalidades de la librería Scapy para la manipulación de paquetes de red
from kafka import KafkaProducer  # Importa KafkaProducer de la librería kafka-python para enviar mensajes a Kafka
import json  # Importa la librería JSON para serializar los datos

# Configura el productor de Kafka para enviar mensajes al servidor Kafka en 'kafka:9092'
# La opción value_serializer serializa los valores en formato JSON y los codifica en UTF-8
producer = KafkaProducer(bootstrap_servers=['kafka:9092'],
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Define una función de callback que se ejecutará para cada paquete capturado
def packet_callback(packet):
    # Verifica si el paquete tiene una capa IP
    if packet.haslayer(scapy.IP):
        # Si el paquete tiene una capa IP, extrae información relevante del paquete
        packet_info = {
            "src_ip": packet[scapy.IP].src,  # Dirección IP de origen
            "dst_ip": packet[scapy.IP].dst,  # Dirección IP de destino
            "proto": packet[scapy.IP].proto,  # Protocolo utilizado (TCP, UDP, etc.)
            "len": len(packet),  # Longitud total del paquete
            "time": packet.time  # Timestamp de cuándo se capturó el paquete
        }
        # Envía la información del paquete al tópico 'raw_packets' en el servidor Kafka
        producer.send('raw_packets', packet_info)

# Inicia la captura de paquetes de red con Scapy
# Para cada paquete capturado, se llama a la función packet_callback
# La opción store=0 indica que los paquetes no se deben almacenar en memoria después de ser procesados
scapy.sniff(prn=packet_callback, store=0)
