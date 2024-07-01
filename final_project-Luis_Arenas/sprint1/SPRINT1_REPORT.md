# Informe del Sprint 1: Diseño e Implementación Básica del IDS

## Resumen Ejecutivo

En este primer sprint, nos enfocamos en establecer la base del Sistema Distribuido de Detección de Intrusiones (dIDS). Implementamos la captura de paquetes, el almacenamiento básico de datos y configuramos el entorno de desarrollo con Docker y Kubernetes.

## Objetivos Alcanzados

1. Definición de requisitos del IDS
2. Diseño de la arquitectura del sistema utilizando microservicios
3. Implementación del capturador de paquetes
4. Configuración del entorno de desarrollo con Docker y Kubernetes
5. Creación de un microservicio básico para la captura y almacenamiento de datos

## Detalles Técnicos

### 1. Capturador de Paquetes

Implementamos el capturador de paquetes en el archivo `src/packet_capture.py`. Utilizamos la biblioteca Scapy para la captura de tráfico de red en tiempo real.

Características principales:
- Utiliza la función `scapy.sniff()` para capturar paquetes en modo promiscuo.
- Implementa un callback `packet_callback()` que procesa cada paquete capturado.
- Utiliza multiprocessing para mejorar el rendimiento de la captura.

Código relevante:
```python
def capture_packets(queue):
    def packet_callback(packet):
        if IP in packet:
            queue.put(packet)
    scapy.sniff(prn=packet_callback, store=0)
```

### 2. Almacenamiento de Datos
Implementamos el almacenamiento de datos en MongoDB a través del archivo `src/data_storage.py`.

**Características principales:**

Utiliza PyMongo para la conexión y operaciones con MongoDB.
Implementa métodos para almacenar y recuperar paquetes de red.
Utiliza batch inserts para optimizar el rendimiento de escritura.

**codigo_relevante**:

```python
class DataStorage:
    def __init__(self):
        self.client = MongoClient(f'mongodb://{MONGODB_HOST}:{MONGODB_PORT}/')
        self.db = self.client[DATABASE_NAME]
        self.collection = self.db[COLLECTION_NAME]

    def store_packet(self, packet_data):
        self.collection.insert_one(packet_data)
```

### 3. Configuración del Entorno
**Docker**
Creamos un Dockerfile para containerizar nuestra aplicación:
```Dockerfile
FROM python:3.9-slim
RUN apt-get update && apt-get install -y libpcap-dev
WORKDIR /app
COPY src/*.py config.py requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "main.py"]
```

**Kubernetes**

Configuramos Kubernetes para el despliegue y gestión de nuestros microservicios. El archivo `kubernetes/deployment.yaml` define el despliegue del sistema IDS:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ids-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ids-system
  template:
    metadata:
      labels:
        app: ids-system
    spec:
      containers:
      - name: ids-system
        image: ids-system:latest
        imagePullPolicy: Never
        securityContext:
          capabilities:
            add: ["NET_ADMIN", "NET_RAW"]
```

### 4. Implementación del Microservicio Básico

Creamos el archivo `src/main.py` como punto de entrada para nuestro microservicio:
```python
import multiprocessing
from packet_capture import main as packet_capture_main
from data_analysis import main as data_analysis_main

def main():
    packet_capture_process = multiprocessing.Process(target=packet_capture_main)
    packet_capture_process.start()

    data_analysis_process = multiprocessing.Process(target=data_analysis_main)
    data_analysis_process.start()

    packet_capture_process.join()
    data_analysis_process.join()

if __name__ == "__main__":
    main()
```
Este script inicia los procesos de captura de paquetes y análisis de datos en paralelo.

**Pruebas**

Implementamos pruebas unitarias para el capturador de paquetes y el almacenamiento de datos en los archivos `tests/test_packet_capture.py` y `tests/test_data_storage.py` respectivamente.
Ejemplo de prueba para el capturador de paquetes:

```python
@patch('scapy.all.sniff')
def test_capture_packets(self, mock_sniff):
    mock_queue = MagicMock()
    capture_packets(mock_queue)
    mock_sniff.assert_called_once()
```
## Desafíos y Soluciones

Rendimiento de la captura de paquetes: Implementamos multiprocessing para mejorar la capacidad de captura en redes de alto tráfico.
Eficiencia del almacenamiento: Utilizamos inserciones por lotes en MongoDB para optimizar el rendimiento de escritura.
Configuración de Kubernetes: Ajustamos los recursos y capacidades del contenedor para permitir la captura de paquetes a nivel de sistema.

## Próximos Pasos
Para el **Sprint 2**, nos enfocaremos en:

- Implementar algoritmos de detección de intrusiones.
- Desarrollar el análisis distribuido de los datos capturados.
- Mejorar la comunicación entre microservicios utilizando gRPC o RESTful APIs.
- Realizar pruebas de integración y optimización del sistema.

## Conclusión
El Sprint 1 ha establecido una base sólida para nuestro Sistema Distribuido de Detección de Intrusiones. Hemos logrado implementar la captura de paquetes, el almacenamiento básico de datos y la configuración del entorno de desarrollo. Estos logros nos posicionan bien para abordar los desafíos más complejos de detección y análisis en los próximos sprints.
