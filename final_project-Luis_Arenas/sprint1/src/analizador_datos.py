# analizador_datos.py

from kafka import KafkaConsumer, KafkaProducer
import json
import redis
import zmq
from pymongo import MongoClient



consumer = KafkaConsumer('processed_packets', bootstrap_servers=['kafka:9092'],
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))

producer = KafkaProducer(bootstrap_servers=['kafka:9092'],
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

redis_client = redis.Redis(host='redis', port=6379, db=0)

def detect_brute_force(packet):
    ip = packet['src_ip']
    current_count = redis_client.incr(f"auth_attempts:{ip}")
    if current_count > 5:
        return True
    return False

def detect_port_scan(packet):
    ip = packet['src_ip']
    port = packet.get('dst_port')
    if port:
        key = f"port_scan:{ip}"
        redis_client.sadd(key, port)
        redis_client.expire(key, 300)  # Expira en 5 minutos
        if redis_client.scard(key) > 100:
            return True
    return False




# Configuración de la conexión a MongoDB
client = MongoClient("mongodb://database-service:27017/")
db = client.ids
collection = db.packet_data

def analyze_packet(packet):
    # Análisis básico del paquete y almacenamiento en MongoDB
    if packet['protocol'] == 6:  # TCP
        # Realizar análisis adicional si es necesario
        collection.insert_one(packet)

def start_data_analyzer():
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://0.0.0.0:5555")

    while True:
        packet = socket.recv_json()
        analyze_packet(packet)

# if __name__ == "__main__":
#     start_data_analyzer()


# Implementar otras funciones de detección aquí

# for message in consumer:
#     packet = message.value
    
#     if detect_brute_force(packet):
#         alert = {"type": "brute_force", "details": packet}
#         producer.send('alerts', alert)
    
#     if detect_port_scan(packet):
#         alert = {"type": "port_scan", "details": packet}
#         producer.send('alerts', alert)

    # En caso ubiese llamar otras funciones de deteccion aqui 
