'''
#### Memoria compartida distribuida

10.Implementa un programa en Python que simule un sistema de snoop bus 
utilizando hilos. Cada hilo representa un núcleo con su propia caché y 
observa una lista compartida de operaciones de memoria.

'''
# mantener la coherencia de caché entre varios 
# procesadores que comparten una memoria común

import threading
import time

# Inicializa una memoria compartida simulada y una lista de operaciones sobre el bus.
shared_memory = [0] * 10
bus_operations = []
bus_lock = threading.Lock()  # Mutex para controlar el acceso a las operaciones del bus.

class Cache:
    def __init__(self, id):
        self.id = id  # Identificador del núcleo o caché.
        self.cache = [0] * 10  # Caché local para el núcleo, inicialmente vacía.

    def read(self, index):
        # Registra una operación de lectura en la lista compartida de operaciones del bus.
        with bus_lock:
            bus_operations.append((self.id, 'read', index))
        return self.cache[index]  # Devuelve el valor actual en la caché local.

    def write(self, index, value):
        # Registra y ejecuta una operación de escritura, actualizando la caché local y el bus.
        with bus_lock:
            bus_operations.append((self.id, 'write', index, value))
        self.cache[index] = value  # Actualiza la caché local con el nuevo valor.

    def snoop(self):
        # Proceso continuo que verifica las operaciones del bus para mantener la coherencia de caché.
        while True:
            with bus_lock:
                if bus_operations:
                    op = bus_operations.pop(0)  # Extrae la operación más antigua del bus.
                    if op[1] == 'write':
                        # Si la operación es una escritura, actualiza la caché local con el nuevo valor.
                        self.cache[op[2]] = op[3]
            time.sleep(0.01)  # Pequeño retardo para evitar el uso excesivo de CPU.

def cpu_task(cache, index, value):
    # Tarea simulada para un procesador: escribe y luego lee de su caché.
    cache.write(index, value)  # Escribe un valor en la caché.
    print(f"CPU {cache.id} wrote {value} at index {index}")
    time.sleep(1)  # Simula tiempo de procesamiento.
    read_value = cache.read(index)  # Lee el valor de la caché.
    print(f"CPU {cache.id} read {read_value} from index {index}")


def main():
    caches = [Cache(i) for i in range(4)]
    threads = []

    for cache in caches:
        t = threading.Thread(target=cache.snoop)
        t.daemon = True
        t.start()

    for i, cache in enumerate(caches):
        t = threading.Thread(target=cpu_task, args=(cache, i % 10, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()