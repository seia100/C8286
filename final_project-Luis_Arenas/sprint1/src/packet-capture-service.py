# packet_capture.py

import scapy.all as scapy
from scapy.layers.inet import IP
import multiprocessing
from pymongo import MongoClient
from config import * # Importa las configuraciones globales

def capture_packets(queue):
    """
    Captura paquetes de red y los envía a una cola para su procesamiento.

    :param queue: Cola multiproceso para enviar los paquetes capturados.
    """
    def packet_callback(packet):
        if IP in packet: # Verifica si el paquete contiene una capa IP
            queue.put(packet) # Agrega el paquete a la cola

    # Inicia la captura de paquetes en modo promiscuo
    scapy.sniff(prn=packet_callback, store=0) # Captura paquetes y ejecuta la función packet_callback por cada paquete

def process_packets(queue, db_client):
    """
    Procesa los paquetes de la cola y los almacena en la base de datos.

    :param queue: Cola multiproceso con los paquetes capturados.
    :param db_client: Cliente de conexión a MongoDB.
    """
    db = db_client[DATABASE_NAME] # Obtiene la base de datos
    collection = db[COLLECTION_NAME] # Obtiene la colección

    batch = [] # Lista para almacenar los paquetes antes de insertarlos en la base de datos
    while True:
        packet = queue.get() # Obtiene un paquete de la cola
        if packet is None:
            break # Sale del bucle si el paquete es None

        packet_dict = {
            "src": packet[IP].src, # Obtiene la dirección IP origen del paquete
            "dst": packet[IP].dst, # Obtiene la dirección IP destino del paquete
            "proto": packet[IP].proto, # Obtiene el protocolo del paquete
            "len": len(packet), # Obtiene la longitud del paquete
            "time": packet.time # Obtiene la hora de captura del paquete
        }
        batch.append(packet_dict) # Agrega el diccionario del paquete a la lista

        if len(batch) >= MAX_PACKETS_PER_BATCH: # Si la lista alcanza el tamaño máximo
            collection.insert_many(batch) # Inserta los paquetes en la base de datos
            batch = [] # Vacía la lista

def main():
    # Conexión a MongoDB
    client = MongoClient(f'mongodb://localhost:{DATABASE_PORT}/') # Crea un cliente de MongoDB

    # Crear una cola multiproceso para compartir paquetes entre procesos
    packet_queue = multiprocessing.Queue() # Crea una cola multiproceso

    # Iniciar el proceso de captura de paquetes
    capture_process = multiprocessing.Process(target=capture_packets, args=(packet_queue,))
    # Crea un proceso que ejecuta la función capture_packets con la cola como argumento
    capture_process.start() # Inicia el proceso

    # Iniciar múltiples procesos para procesar paquetes
    process_pool = [] # Lista para almacenar los procesos
    for _ in range(CPU_CORES): # Crea un proceso por cada núcleo de CPU
        p = multiprocessing.Process(target=process_packets, args=(packet_queue, client))
        # Crea un proceso que ejecuta la función process_packets con la cola y el cliente de MongoDB como argumentos
        p.start() # Inicia el proceso
        process_pool.append(p) # Agrega el proceso a la lista

    # Esperar a que los procesos terminen (esto no ocurrirá en una ejecución normal)
    capture_process.join() # Espera a que el proceso de captura termine
    for p in process_pool:
        p.join() # Espera a que cada proceso de procesamiento termine

if __name__ == "__main__":
    main() # Ejecuta la función main si el script se ejecuta directamente