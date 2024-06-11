# Técnicas de balanaceo de carga

#### Ejercicio 5
EStudiar la latendcia y el ancho de banda en sistemas distribuidos y cómo influyen en la eficiencia del paralelismo.

##### Tareas
* Implementar un algoritmo de comunicación punto a punto( por ejemplo, intercambio de mensajes) utilizando MPI

* Mide la latencia y el ancho de banda para diferentes tamañosde los mensajes

* Analiza cómo estos parámetros afectan la eficiencia de un algoritmo paralelo.

* Propone mejoras para optimizar la comunuicacion en sistemas distribuidos.

```python
# Importamos las bibliotecas necesarias
from mpi4py import MPI
import numpy as np
import time

# Inicializamos el comunicador global y obtenemos el rango del proceso actual
comm = MPI.COMM_WORLD # comunica procesos ejecutados
rank = comm.Get_rank() # 

# Definimos el tamaño del mensaje que vamos a enviar
message_size = 1024 * 1024  # 1MB
# El proceso con rango 0 inicializa el mensaje con números aleatorios
# Los demás procesos inicializan un array vacío del mismo tamaño
message = np.random.rand(message_size) if rank == 0 else np.empty(message_size)

# Comprobamos si el proceso es el líder (rango 0)
if rank == 0:
    # Marcamos el tiempo de inicio
    start_time = time.time()
    # El líder envía el mensaje al proceso con rango 1
    comm.Send([message, MPI.DOUBLE], dest=1, tag=0)
    # Luego espera recibir un mensaje de vuelta del proceso con rango 1
    comm.Recv([message, MPI.DOUBLE], source=1, tag=1)
    # Marcamos el tiempo de finalización y calculamos la latencia
    end_time = time.time()
    # Imprimimos la latencia calculada
    print(f"Latencia: {end_time - start_time} segundos")
else:
    # Los procesos que no son líder esperan recibir un mensaje del líder
    comm.Recv([message, MPI.DOUBLE], source=0, tag=0)
    # Después de recibir el mensaje, lo envían de vuelta al líder
    comm.Send([message, MPI.DOUBLE], dest=0, tag=1)

```
