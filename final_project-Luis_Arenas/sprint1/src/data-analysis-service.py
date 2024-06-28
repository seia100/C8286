# data_analysis.py

from pymongo import MongoClient
import numpy as np
from scipy import stats
import multiprocessing
import time # Importamos el módulo time para la función sleep()
from config import * # Importamos las configuraciones globales

def analyze_traffic(collection, time_window=60):
    """
    Analiza el tráfico de red en busca de patrones sospechosos.
    
    :param collection: Colección de MongoDB con los paquetes de red.
    :param time_window: Ventana de tiempo en segundos para el análisis (por defecto 60 segundos).
    :return: Lista de alertas generadas.
    """
    current_time = time.time() # Obtiene la hora actual en segundos desde Epoch
    start_time = current_time - time_window # Calcula la hora de inicio de la ventana

    # Obtener paquetes en la ventana de tiempo
    packets = list(collection.find({"time": {"$gte": start_time, "$lte": current_time}}))
    # Encuentra los documentos en la colección que tengan un campo "time" 
    # mayor o igual a start_time y menor o igual a current_time.

    alerts = [] # Inicializa una lista vacía para almacenar las alertas

    # Análisis de volumen de tráfico
    packet_counts = {} # Diccionario para almacenar el conteo de paquetes por dirección IP origen
    for packet in packets:
        src = packet['src'] # Obtiene la dirección IP origen del paquete
        packet_counts[src] = packet_counts.get(src, 0) + 1 
        # Incrementa el conteo de paquetes para la dirección IP origen. 
        # Si no existe, se crea una nueva entrada con valor inicial 0.

    # Detectar anomalías en el volumen de tráfico
    volumes = list(packet_counts.values()) # Crea una lista con los conteos de paquetes
    mean_volume = np.mean(volumes) # Calcula la media de los conteos
    std_volume = np.std(volumes) # Calcula la desviación estándar de los conteos
    threshold = mean_volume + 3 * std_volume  # Define el umbral como la media más 3 desviaciones estándar

    for src, count in packet_counts.items():
        if count > threshold: # Si el conteo de paquetes supera el umbral
            alerts.append(f"Alto volumen de tráfico detectado desde {src}: {count} paquetes")
            # Agrega una alerta a la lista

    # Análisis de puertos de destino frecuentes (posible escaneo)
    dst_ports = [packet.get('dport') for packet in packets if 'dport' in packet]
    # Crea una lista con los puertos de destino de los paquetes que tienen el campo 'dport'

    port_counts = {} # Diccionario para almacenar el conteo de accesos por puerto
    for port in dst_ports:
        port_counts[port] = port_counts.get(port, 0) + 1
        # Incrementa el conteo de accesos para el puerto. Si no existe, se crea una nueva entrada con valor 0.

    for port, count in port_counts.items():
        if count > 100:  # Umbral arbitrario, ajustar según necesidades
            alerts.append(f"Posible escaneo de puertos detectado. Puerto {port} accedido {count} veces")
            # Agrega una alerta si el conteo de accesos al puerto supera el umbral

    return alerts # Retorna la lista de alertas

def analyze_worker(db_client):
    """
    Función de trabajo para el análisis continuo de datos.
    
    :param db_client: Cliente de conexión a MongoDB.
    """
    db = db_client[DATABASE_NAME] # Obtiene la base de datos
    collection = db[COLLECTION_NAME] # Obtiene la colección

    while True:
        alerts = analyze_traffic(collection) # Realiza el análisis de tráfico
        if alerts: # Si hay alertas
            print("Alertas detectadas:")
            for alert in alerts:
                print(alert) # Imprime cada alerta
        time.sleep(10)  # Espera 10 segundos antes del próximo análisis

def main():
    # Conexión a MongoDB
    client = MongoClient(f'mongodb://localhost:{DATABASE_PORT}/') # Crea un cliente de MongoDB
    
    # Iniciar múltiples procesos de análisis
    process_pool = [] # Lista para almacenar los procesos
    for _ in range(CPU_CORES): # Crea un proceso por cada núcleo de CPU definido en config.py
        p = multiprocessing.Process(target=analyze_worker, args=(client,))
        # Crea un proceso que ejecuta la función analyze_worker con el cliente de MongoDB como argumento
        p.start() # Inicia el proceso
        process_pool.append(p) # Agrega el proceso a la lista
    
    # Esperar a que los procesos terminen (esto no ocurrirá en una ejecución normal)
    for p in process_pool:
        p.join() # Espera a que cada proceso termine

if __name__ == "__main__":
    main() # Ejecuta la función main si el script se ejecuta directamente