# Diseño y Arquitectura del Sistema Distribuido de Detección de Intrusiones (dIDS)

## Tabla de Contenidos
1. [Visión General](#visión-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Componentes Principales](#componentes-principales)
4. [Flujo de Datos](#flujo-de-datos)
5. [Tecnologías Utilizadas](#tecnologías-utilizadas)
6. [Consideraciones de Diseño](#consideraciones-de-diseño)
7. [Diagramas](#diagramas)
8. [Referencias](#referencias)
9. [Conclusiones](#conclusiones)

## Visión General

El Sistema Distribuido de Detección de Intrusiones (dIDS) es una solución de seguridad de red diseñada para identificar y alertar sobre actividades sospechosas en tiempo real. Utiliza técnicas de análisis distribuido y aprendizaje automático para procesar grandes volúmenes de tráfico de red de manera eficiente.

## Arquitectura del Sistema

El dIDS sigue una arquitectura de microservicios containerizada, desplegada en un clúster de Kubernetes. Esta arquitectura permite una alta escalabilidad, resistencia a fallos y facilidad de mantenimiento.

### Diagrama de Arquitectura

```mermaid
graph TD
    A[Tráfico de Red] --> B[Capturador de Paquetes]
    B --> C[Cola de Mensajes]
    C --> D[Analizador de Datos]
    D --> E[Base de Datos MongoDB]
    E --> F[Interfaz de Usuario]
    G[Kubernetes Cluster] --> B
    G --> C
    G --> D
    G --> E
    G --> F

```
## Componentes Principales

- **Capturador de Paquetes:**

   - Implementado en packet_capture.py
   - Utiliza Scapy para capturar tráfico de red en tiempo real
   - Ejecuta múltiples procesos para un rendimiento óptimo


- **Analizador de Datos:**

   - Implementado en data_analysis.py
   - Procesa los paquetes capturados para detectar patrones sospechosos
   - Utiliza algoritmos de detección de anomalías y aprendizaje automático


- **Almacenamiento de Datos:**

   - Implementado en data_storage.py
   - Utiliza MongoDB para almacenar paquetes de red y resultados de análisis
   - Proporciona una interfaz para operaciones CRUD


- **Interfaz de Usuario:**

   - Implementada como un servicio web separado
   - Muestra alertas, estadísticas y permite la configuración del sistema


- **Orquestación de Contenedores:**

   - Utiliza Kubernetes para gestionar y escalar los componentes del sistema

## Flujo de Datos

- El Capturador de Paquetes intercepta el tráfico de red.
- Los paquetes capturados se envían a una cola de mensajes para su procesamiento.
- El Analizador de Datos consume los paquetes de la cola y realiza análisis en tiempo real.
- Los resultados del análisis y los paquetes relevantes se almacenan en MongoDB.
- La Interfaz de Usuario consulta la base de datos para mostrar alertas y estadísticas.

## Tecnologías Utilizadas

- Lenguaje de Programación: Python 3.9
- Captura de Paquetes: Scapy
- Base de Datos: MongoDB
- Análisis de Datos: NumPy, SciPy
- Containerización: Docker
- Orquestación: Kubernetes
- Comunicación entre Servicios: gRPC
- Interfaz de Usuario: Flask (backend), React (frontend)

## Consideraciones de Diseño

**Escalabilidad**:

- Uso de microservicios para escalar componentes individualmente
- Implementación de procesamiento paralelo en la captura y análisis de paquetes


**Rendimiento**:

- Optimización de algoritmos de análisis para procesamiento en tiempo real
- Uso de índices en MongoDB para consultas eficientes


**Seguridad**:

- Implementación de autenticación y autorización en todos los servicios
- Cifrado de datos en tránsito y en reposo


**Tolerancia a Fallos**:

- Replicación de servicios críticos
- Implementación de mecanismos de recuperación automática


**Mantenibilidad**:

- Diseño modular para facilitar actualizaciones y pruebas
- Uso de contenedores para garantizar la consistencia entre entornos

## Diagramas
### Diagrama de Componentes
```mermaid
classDiagram
    class PacketCapture {
        +capture_packets()
        +process_packets()
    }
    class DataAnalysis {
        +analyze_traffic()
        +detect_anomalies()
    }
    class DataStorage {
        +store_packet()
        +get_packets()
    }
    class UserInterface {
        +display_alerts()
        +show_statistics()
    }
    PacketCapture --> DataStorage : stores
    DataAnalysis --> DataStorage : reads/writes
    UserInterface --> DataStorage : reads
```
Este diagrama muestra las principales clases y sus relaciones en el sistema dIDS.

### Diagrama de Secuencia

```mermaid
sequenceDiagram
    participant N as Network
    participant PC as PacketCapture
    participant DA as DataAnalysis
    participant DS as DataStorage
    participant UI as UserInterface

    N->>PC: Network Traffic
    PC->>DS: Store Raw Packets
    PC->>DA: Send for Analysis
    DA->>DS: Store Analysis Results
    DA->>UI: Send Alerts
    UI->>DS: Fetch Data
    UI->>UI: Display to User
```

Este diagrama ilustra el flujo de datos y la secuencia de operaciones en el sistema dIDS.




### Diagrama de Flujo de Datos
```mermaid
graph TD
    A[Tráfico de Red] --> B[Capturador de Paquetes]
    B --> C[Cola de Mensajes]
    C --> D[Analizador de Datos]
    D --> E[Base de Datos]
    D --> F[Motor de Reglas]
    F --> G[Generador de Alertas]
    G --> H[Interfaz de Usuario]
    E --> H
    I[Módulo de Machine Learning] --> D
    J[Módulo de Análisis de Comportamiento] --> D
```
Este diagrama detallado muestra el flujo de datos a través de los diferentes componentes del sistema dIDS:

- El tráfico de red es interceptado por el Capturador de Paquetes.
- Los paquetes capturados se envían a una Cola de Mensajes para su procesamiento asíncrono.
- El Analizador de Datos procesa los paquetes de la cola.
- El análisis se apoya en un Módulo de Machine Learning y un Módulo de Análisis de Comportamiento para detectar anomalías y patrones sospechosos.
- Los resultados del análisis se almacenan en la Base de Datos y se pasan al Motor de Reglas.
- El Motor de Reglas evalúa los resultados del análisis según las reglas predefinidas.
- Si se detectan actividades sospechosas, el Generador de Alertas crea las alertas correspondientes.
- La Interfaz de Usuario muestra las alertas y permite acceder a los datos almacenados en la Base de Datos.

Esta arquitectura permite un procesamiento eficiente y escalable del tráfico de red, combinando técnicas de análisis en tiempo real con aprendizaje automático para una detección de intrusiones más precisa y adaptativa.

### Diagrama de la arquitectura
![architecture_diagram](https://github.com/seia100/C8286/blob/main/final_project-Luis_Arenas/sprint1/data/diagram_arch_dIDS.drawio.svg)

- Kubernetes Cluster: Todo el sistema está encapsulado dentro de un clúster de Kubernetes, lo que permite una gestión y escalado eficientes de los componentes.
- Capturador de Paquetes: Intercepta el tráfico de red entrante.
- Cola de Mensajes: Actúa como buffer entre la captura de paquetes y el análisis, permitiendo un procesamiento asíncrono.
- Analizador de Datos: Procesa los paquetes de la cola, apoyándose en los módulos de Machine Learning y Análisis de Comportamiento.
- Motor de Reglas: Evalúa los datos analizados contra un conjunto de reglas predefinidas.
- Generador de Alertas: Crea alertas basadas en las actividades sospechosas identificadas.
- MongoDB: Almacena todos los datos, incluyendo paquetes capturados, resultados de análisis y alertas.
- API Backend: Proporciona una interfaz para que la UI acceda a los datos y funcionalidades del sistema.
- Interfaz de Usuario: Permite a los usuarios interactuar con el sistema, visualizar alertas y configurar parámetros.
- Módulos de ML y Análisis de Comportamiento: Asisten al Analizador de Datos en la detección de anomalías y patrones sospechosos.

Este diagrama muestra claramente el flujo de datos a través del sistema, desde la captura de paquetes hasta la generación de alertas y la interacción del usuario. También ilustra cómo los diferentes componentes se comunican entre sí dentro del clúster de Kubernetes.

## Referencias

- [Kubernetes Documentation](https://kubernetes.io/es/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Scapy Documentation ](https://scapy.net/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [gRPC Documentation](https://grpc.io/docs/)
- [Flask Documentation](https://www.geeksforgeeks.org/flask-tutorial/)
- [React Documentation](https://react.dev/)
- [Microservices Architecture](https://microservices.io/)
- [Distributed Systems Design](https://medium.com/@nilesh.dabholkar/distributed-systems-design-patterns-architecting-for-scalability-and-reliability-d937a56ff347)

## Conclusiones
Este documento `DESIGN.md` proporciona una visión técnica y detallada de la arquitectura y diseño del sistema dIDS. Incluye diagramas para una mejor comprensión visual de la arquitectura, los componentes y el flujo de datos. Los diagramas se han creado utilizando la sintaxis de Mermaid, que es compatible con muchos visualizadores de Markdown y plataformas como GitHub.

El diseño abarca los tres sprints del proyecto, considerando la captura de paquetes, el análisis de datos y la interfaz de usuario. También se han incluido consideraciones importantes como la escalabilidad, el rendimiento y la seguridad.

Las referencias proporcionadas al final del documento ofrecen recursos adicionales para profundizar en las tecnologías y conceptos utilizados en el diseño del sistema.
