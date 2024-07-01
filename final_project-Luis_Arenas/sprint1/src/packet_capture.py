import scapy.all as scapy
from scapy.layers.inet import IP # monitoring IPv4
import multiprocessing
from pymongo import MongoClient
from config import *

def capture_packets(queue):
    """
    Captura paquetes de red y los envia a una cola para su procesamiento.

    :param queue: Cola multiporceso para enviar los paquetes capturados.
    """
    def packet_callback(packet):
        if IP in packet: # verificar si el paquete contiene una capa IP
            queue.put(packet) # Agrega el paquete a la col

    # Inicia la captura de paquetes en modo promiscuo
    scapy.sniff(prn=packt_callback, store=0)

def process_packets(queue, db_client):
    """
    Procesa los paquetes de la cola y los almacena en la base de datos

    :param  queue: Cola multiproceso con los paquetes capturados.
    :param db_cliente: Cliente de conexion a MongoDB
    """
    db = db_client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    batch = [] # Lista para almacenar los paquetes antes de insertalos en la base de datos
    while True:
        packet = queue.get() # Obtiene un paquete de la cola
        if packet is None:
            break # sale del bucle si el paquete es None

        packet_dict = {
            "src": packet[IP].src,
            "dst": packet[IP].dst,
            "proto": packet[IP].proto,
            "len": len(packet),
            "time": packet.time

        }
        batch.append(packet_dict)


        if len(batch)>= MAX_PACKETS_PER_BATCH:
            collection.insert_many(batch) # Inserta los paquetes en la base de datos 
            batch = [] # limpia la lista

def main():
    # Conexion a MongoDB
    client = MongoClient(f'mongodb://{MONGO_HOST}:{MONGODB_PORT}/')

    # Crear una cola multiproceso para compartir paquetes entre procesos
    packet_queue = multiprocessing.Queue()

    # Iniciar el proceso de captura de paquetes
    capture_process = multiprocessing.Process(target=capture_packets, args=(packet_queue,))
    capture_process.start()

    # Iniciar multiples procesos para procesar paquetes
    process_pool = []
    for _ in range(CPU_CORES):
        p = multiprocessing.Process(target=process_packets, args=(packet_queue,client, ))
        p.start()
        process_pool.append(p)

    # Esperar a que los procesos terminen (esto no ocurrira en una ejecucion normal)
    capture_process.join()
    for p in process_pool:
        p.join()

if __name__ == "__main__":
    main()

    