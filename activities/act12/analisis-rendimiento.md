# Técnicas de balanaceo de carga

#### Ejercicio 5
EStudiar la latendcia y el ancho de banda en sistemas distribuidos y cómo influyen en la eficiencia del paralelismo.

##### Tareas
* Implementar un algoritmo de comunicación punto a punto( por ejemplo, intercambio de mensajes) utilizando MPI

* Mide la latencia y el ancho de banda para diferentes tamañosde los mensajes

* Analiza cómo estos parámetros afectan la eficiencia de un algoritmo paralelo.

* Propone mejoras para optimizar la comunuicacion en sistemas distribuidos.

```python
from mpi4py import MPI
import numpy as np
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

message_size = 1024 * 1024 # 1MB
message = np.random.rand(message_size) if rank == 0 else np.empty(message_size)

if rank == 0:
  start_time = time.time()
  com.Send([message, MPI.DPUBLE], source=0, tag=0)
  comm.Recv([message, MPI.DOUBLE], source=1, tag=1)
  end_time = time.time()
  print(f"Latencia: {end_time - start_time} segundos")
else:
    comm.Recv([message, MPI.DOUBLE], source=0, tag=0)
    comm.Send([message, MPI.DOUBLE], dest=0, tag=1)
```
