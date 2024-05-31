# Resumen de Memoria Compartida Distribuida

## Conceptos Clave

1. **Coherencia de Caché**:
   - **Protocolo MESI**: Explica cómo se mantiene la coherencia en sistemas de memoria compartida.
   - **Estados MESI**: Modificado, Exclusivo, Compartido, Inválido.
   - **Transiciones de Estado**:
     - Cuando un procesador lee una línea de caché por primera vez.
     - Cuando un segundo procesador lee la misma línea de caché.
     - Cuando un procesador modifica la línea de caché.
     - Cuando un segundo procesador intenta leer la línea de caché modificada.

2. **Implementación Práctica**:
   - Uso de **POSIX threads (pthread)** y **mutexes** para proteger una variable compartida.
   - Ejemplo de un programa que incrementa de manera segura una variable global compartida mediante múltiples hilos.

3. **Optimización de Algoritmos para Memoria Compartida**:
   - **Localización de Datos**: Agrupar en memoria los datos frecuentemente accedidos para aprovechar la caché.
   - **Reducción de Contención**: Utilizar estructuras de datos concurrentes y particionar tareas para minimizar el acceso simultáneo.
   - **Minimización de la Latencia de Caché**: Acceder a los datos siguiendo patrones que maximicen la eficiencia de la caché y evitar el "cache thrashing".

## Ejercicios Propuestos

1. Describir detalladamente el funcionamiento del protocolo MESI con ejemplos de transiciones de estados.
2. Programar en C usando pthreads y mutexes para demostrar la protección de una variable compartida.
3. Discutir estrategias para optimizar algoritmos en sistemas de memoria compartida, incluyendo técnicas para mejorar el rendimiento y reducir la latencia.


### Modelos de Consistencia de Memoria

1. **Consistencia Estricta**:

   - Definición: Todas las operaciones de memoria son vistas por todos los procesadores en el orden exacto en que ocurren.
   - Comportamiento Observable: Cualquier lectura a una variable siempre devuelve el valor más reciente escrito a esa variable.

Para ilustrar la consistencia estricta, podemos simular un escenario simple con dos hilos donde las operaciones de escritura y lectura deben observarse en el mismo orden exacto por todos los hilos.

```python
import threading

# Variable global para demostrar la consistencia estricta
shared_variable = 0

# Lock para asegurar la consistencia estricta
lock = threading.Lock()

def writer():
    global shared_variable
    for i in range(1, 6):
        lock.acquire()
        shared_variable = i
        print(f"Writer updated the value to {shared_variable}")
        lock.release()

def reader():
    global shared_variable
    for _ in range(5):
        lock.acquire()
        print(f"Reader reads the value {shared_variable}")
        lock.release()

# Creando hilos
t1 = threading.Thread(target=writer)
t2 = threading.Thread(target=reader)

# Iniciando hilos
t1.start()
t2.start()

# Esperando a que los hilos terminen
t1.join()
t2.join()
```

2. **Consistencia Secuencial**:

   - Definición: Las operaciones de memoria de todos los procesadores se intercalan en un orden secuencial que es consistente con el orden de programa de cada procesador.
   - Comportamiento Observable: El orden de ejecución de las operaciones de memoria parece ser secuencial, aunque las operaciones puedan ser reordenadas, siempre y cuando se mantenga la consistencia con el orden del programa.


3. **Consistencia Causal**:

   - Definición: Solo las operaciones de memoria que son causalmente relacionadas deben ser vistas en el mismo orden por todos los procesadores.
   - Comportamiento Observable: Las operaciones que tienen una relación causal (por ejemplo, una operación que depende del resultado de otra) se verán en el mismo orden por todos los procesadores, pero operaciones independientes pueden ser vistas en diferentes órdenes.


### Paso de Mensajes en Sistemas de Memoria Distribuida

- Método: Los nodos envían y reciben mensajes para compartir datos.
- Ventajas:
  - No requiere coherencia de caché.
  - Escalabilidad mejorada al disminuir el acoplamiento entre nodos.
  - Adecuado para sistemas distribuidos donde los nodos no comparten una memoria física común.
- Desventajas:
  - Latencia en la comunicación puede ser un problema, especialmente en sistemas con muchos nodos.
  - Mayor complejidad en la programación debido a la necesidad de manejar explícitamente el envío y recepción de mensajes.
  - Sobrecarga de comunicación debido a la transmisión de mensajes incluso para pequeñas cantidades de datos.


### Modelos de Consistencia Eventual vs. Fuerte

- **Consistencia Fuerte**:
  - Definición: Las actualizaciones son visibles instantáneamente a todos los nodos, proporcionando una vista consistente de los datos en todo momento.
  - Aplicaciones Adecuadas: Crucial para aplicaciones financieras o sistemas de reservas donde la exactitud de la información en tiempo real es fundamental.

- **Consistencia Eventual**:
  - Definición: Las actualizaciones se propagan gradualmente y todos los nodos eventualmente alcanzan una consistencia, pero puede haber inconsistencias temporales.
  - Aplicaciones Adecuadas: Adecuado para redes sociales, comentarios en blogs, o sistemas de caching distribuido, donde no es crítico que todos los usuarios vean la misma información al mismo tiempo.


### 2 Paso de Mensajes

Aquí mostraremos cómo los nodos (o hilos en este caso) pueden comunicarse mediante el paso de mensajes, sin compartir memoria directa.

```python
import threading
import queue

# Colas para simular el paso de mensajes
queue1 = queue.Queue()
queue2 = queue.Queue()

def node1():
    # Enviando mensajes
    for i in range(5):
        message = f"Message {i} from Node 1"
        queue2.put(message)
        print(f"Node 1 sent: {message}")

def node2():
    # Recibiendo mensajes
    while True:
        message = queue2.get()
        print(f"Node 2 received: {message}")
        if message == "Message 4 from Node 1":
            break

# Creando hilos
t1 = threading.Thread(target=node1)
t2 = threading.Thread(target=node2)

# Iniciando hilos
t1.start()
t2.start()

# Esperando a que los hilos terminen
t1.join()
t2.join()
```
**Explicación**: En este ejemplo, `node1` envía mensajes a `node2` utilizando una cola. Esto ilustra cómo los nodos pueden comunicarse sin necesidad de compartir acceso directo a la misma memoria, típico del paso de mensajes en sistemas distribuidos.

### 3. Consistencia Eventual vs. Consistencia Fuerte

Vamos a crear un ejemplo simple usando variables y retardos para mostrar la diferencia entre consistencia eventual y fuerte.

```python
import time

# Valor compartido simulado
shared_value = 0

def update_value():
    global shared_value
    shared_value = 10
    print("Value updated to 10")

def read_value_consistent():
    print("Consistently reading value:", shared_value)

def read_value_eventual():
    time.sleep(1)  # Simulando retardo en la propagación
    print("Eventually consistent read value:", shared_value)

# Actualizando el valor
update_value()

# Lectura consistente (fuerte)
read_value_consistent()

# Lectura eventual
read_value_eventual()
```

**Explicación**: En `read_value_consistent`, el valor se lee inmediatamente después de la actualización, mostrando consistencia fuerte. En `read_value_eventual`, hay un retardo antes de la lectura, ilustrando cómo, en un sistema con consistencia eventual, los cambios pueden no ser inmediatamente visibles a todos los nodos.
