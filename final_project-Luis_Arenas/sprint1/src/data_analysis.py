# Encarga del analisis de los datos capturados

from pymongo import MongoClient
import numpy as np
from scipy import stats
import multiprocessing
import time
from config import *

def analyze_traffic(collection, time_window=60):
    """
    Analiza el tráfico de red en busca de patrones sospechosos.
    
    :param collection: Colección de MongoDB con los paquetes de red.
    :param time_window: Ventana de tiempo en segundos para el análisis (por defecto 60 segundos).
    :return: Lista de alertas generadas.
    """
    current_time = time.time()  # Obtiene la hora actual en segundos desde Epoch
    start_time = current_time - time_window  # Calcula la hora de inicio de la ventana

    # Obtener paquetes en la ventana de tiempo
    packets = list(collection.find({"time": {"$gte": start_time, "$lte": current_time}}))

    alerts = []  # Inicializa una lista vacía para almacenar las alertas

    # Análisis de volumen de tráfico
    packet_counts = {}  # Diccionario para almacenar el conteo de paquetes por dirección IP origen
    for packet in packets:
        src = packet['src']
        packet_counts[src] = packet_counts.get(src, 0) + 1

    # Detectar anomalías en el volumen de tráfico
    volumes = list(packet_counts.values())
    mean_volume = np.mean(volumes)
    std_volume = np.std(volumes)
    threshold = mean_volume + 3 * std_volume  # Define el umbral como la media más 3 desviaciones estándar

    for src, count in packet_counts.items():
        if count > threshold:
            alerts.append(f"Alto volumen de tráfico detectado desde {src}: {count} paquetes")

    # Análisis de puertos de destino frecuentes (posible escaneo)
    dst_ports = [packet.get('dport') for packet in packets if 'dport' in packet]

    port_counts = {}  # Diccionario para almacenar el conteo de accesos por puerto
    for port in dst_ports:
        port_counts[port] = port_counts.get(port, 0) + 1

    for port, count in port_counts.items():
        if count > 100:  # Umbral arbitrario, ajustar según necesidades
            alerts.append(f"Posible escaneo de puertos detectado. Puerto {port} accedido {count} veces")

    return alerts

def analyze_worker(db_client):
    """
    Función de trabajo para el análisis continuo de datos.
    
    :param db_client: Cliente de conexión a MongoDB.
    """
    db = db_client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    while True:
        alerts = analyze_traffic(collection)
        if alerts:
            print("Alertas detectadas:")
            for alert in alerts:
                print(alert)
        time.sleep(10)  # Espera 10 segundos antes del próximo análisis

def main():
    # Conexión a MongoDB
    client = MongoClient(f'mongodb://{MONGODB_HOST}:{MONGODB_PORT}/')
    
    # Iniciar múltiples procesos de análisis
    process_pool = []
    for _ in range(CPU_CORES):
        p = multiprocessing.Process(target=analyze_worker, args=(client,))
        p.start()
        process_pool.append(p)
    
    # Esperar a que los procesos terminen (esto no ocurrirá en una ejecución normal)
    for p in process_pool:
        p.join()

if __name__ == "__main__":
    main()