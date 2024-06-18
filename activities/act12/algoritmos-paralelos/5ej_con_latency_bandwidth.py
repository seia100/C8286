# Importamos las librerías necesarias para manejar comunicación en entornos distribuidos y medir el tiempo
from mpi4py import MPI
import numpy as np
import time

# Inicialización del comunicador global de MPI
comm = MPI.COMM_WORLD
# Obtención del rango del proceso actual
rank = comm.Get_rank()
# Número total de procesos en el comunicador
size = comm.Get_size()

# Definimos el tamaño del mensaje que vamos a enviar
message_size = 1024 * 1024  # 1MB (1024**2) # 1KB para simplificar el ejemplo
# El proceso con rango 0 genera datos aleatorios para enviar
if rank == 0:
    message = np.random.rand(message_size)
    # Comenzamos a medir el tiempo antes de iniciar el envío de mensajes
    start_time = time.time()
    # Envío de datos a todos los demás procesos de manera estática
    for i in range(1, size):
        comm.Send([message, MPI.DOUBLE], dest=i, tag=0)
    # Terminamos de medir el tiempo después de enviar todos los mensajes
    end_time = time.time()
    # Calculamos y mostramos la latencia total del envío
    print(f"Tiempo total de envío: {end_time - start_time} segundos")
else:
    # Todos los procesos que no son el líder reciben el mensaje
    message = np.empty(message_size, dtype='d')  # Preparación del array para recibir datos
    comm.Recv([message, MPI.DOUBLE], source=0, tag=0)

# Este código ahora mide el tiempo que toma para que el líder envíe mensajes a todos los otros nodos.
# Esto proporciona una métrica simple para evaluar el overhead de comunicación en un enfoque sin balanceo de carga.
