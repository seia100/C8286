# Detalles del Diseño y Arquitectura del Sistema Distribuido de Detección de Intrusiones (IDS)

## 1. Requisitos del IDS

### 1.1 Tipos de Intrusiones a Detectar

El sistema debe ser capaz de detectar los siguientes tipos de intrusiones:

1. **Ataques de Fuerza Bruta**: Intentos repetidos de autenticación fallidos.
2. **Escaneo de Puertos**: Detección de escaneos sistemáticos de puertos en la red.
3. **Inyección SQL**: Identificación de patrones de inyección SQL en las solicitudes HTTP.
4. **Cross-Site Scripting (XSS)**: Detección de intentos de inyección de scripts maliciosos.
5. **Denegación de Servicio (DoS)**: Identificación de patrones de tráfico anormales que puedan indicar un ataque DoS.
6. **Malware y Botnets**: Detección de comunicaciones sospechosas que puedan indicar infecciones de malware o actividad de botnets.
7. **Exfiltración de Datos**: Identificación de transferencias de datos anormales que puedan indicar fuga de información.
8. **Man-in-the-Middle (MitM)**: Detección de intentos de interceptación de tráfico.

### 1.2 Umbrales de Alerta y Criterios de Análisis

Para cada tipo de intrusión, se establecerán los siguientes umbrales y criterios:

1. **Ataques de Fuerza Bruta**:
   - Umbral: Más de 5 intentos fallidos de autenticación en 1 minuto.
   - Criterio: Monitoreo de logs de autenticación y análisis de patrones de intentos fallidos.
   - Metodología: Análisis de series temporales con algoritmos ARIMA y detección de outliers.

2. **Escaneo de Puertos**:
   - Umbral: Más de 100 intentos de conexión a diferentes puertos desde una misma IP en 5 minutos.
   - Criterio: Análisis de patrones de tráfico TCP/UDP.
   - Metodología: Implementación de algoritmos de detección de patrones basados en grafos.

3. **Inyección SQL**:
   - Umbral: Detección de 3 o más patrones sospechosos en solicitudes HTTP en 10 minutos.
   - Criterio: Análisis de payload de solicitudes HTTP utilizando expresiones regulares.
   - Metodología: Análisis léxico y sintáctico de payloads HTTP utilizando árboles de parsing.

4. **Cross-Site Scripting (XSS)**:
   - Umbral: Detección de 2 o más intentos de inyección de scripts en 5 minutos.
   - Criterio: Análisis de parámetros de solicitudes HTTP y respuestas del servidor.
   - Metodología: Implementación de sanitización y análisis de contexto de entrada de usuario.

5. **Denegación de Servicio (DoS)**:
   - Umbral: Aumento del 200% en el tráfico normal hacia un servicio específico en 1 minuto.
   - Criterio: Análisis estadístico del volumen y patrón de tráfico.
   - Metodología: Análisis multivariante de características de tráfico y clasificación mediante SVM.

6. **Malware y Botnets**:
   - Umbral: Detección de 5 o más conexiones a direcciones IP conocidas como maliciosas en 1 hora al host.
   - Criterio: Comparación de tráfico con listas negras de IPs y dominios conocidos.
   - Metodología: Implementación de modelos de aprendizaje profundo para clasificación de tráfico malicioso.

7. **Exfiltración de Datos**:
   - Umbral: Transferencia de datos superior a 100MB hacia direcciones IP externas no autorizadas en 1 hora.
   - Criterio: Análisis de volumen y destino del tráfico saliente.
   - Metodología: Análisis de flujo de datos mediante técnicas de procesamiento de big data.

8. **Man-in-the-Middle (MitM)**:
   - Umbral: Detección de 3 o más intentos de ARP spoofing o DNS en 10 minutos por segmento de red.
   - Criterio: Monitoreo de tablas ARP y análisis de cambios sospechosos.
   - Metodología: Implementación de algoritmos de detección de anomalías en protocolos de red.

### 1.3 Requisitos de Rendimiento y Disponibilidad

1. **Rendimiento**:
   - Capacidad de procesar al menos 10,000 paquetes por segundo en tiempo real.
   - Latencia máxima de 100ms desde la captura del paquete hasta la generación de una alerta.
   - Capacidad de escalar horizontalmente para manejar aumentos en el tráfico de red.
     - Throughput de análisis: Capacidad de escalar linealmente con el aumento de nodos de procesamiento. 

2. **Disponibilidad**:
   - Tiempo de actividad del 99.99% (menos de 52 minutos de inactividad al año).
     - SLA (Service Level Agreement) de tiempo de actividad: se espera en un caso ideal o en el mejor de los casos. 
   - Implementación de redundancia en todos los componentes críticos con redundancia N+1 en componentes críticos.
     - importante mencionar que la implentacion de servicios o servidores sera con Docker y con un escalado proporcional gestionado por Kubernetes.Lo cual automatiza el escalado y, balanceo de carga y tolerancia a fallos.  
   - Capacidad de recuperación automática en caso de fallo de un nodo.
   - Balanceo de carga entre múltiples instancias de cada microservicio.

3. **Almacenamiento**:
   - Capacidad de almacenar y analizar logs de al menos 30 días.
   - Tiempo de respuesta máximo de 5 segundos para consultas históricas.

4. **Escalabilidad**:
   - Capacidad de escalar automáticamente basado en la carga del sistema.
   - Soporte para múltiples instancias de cada microservicio.

## 2. Arquitectura del Sistema usando Microservicios

### 2.1 División en Microservicios Independientes

El sistema se dividirá en los siguientes microservicios:

1. **Capturador de Paquetes (Packet Capture Service)**
2. **Analizador de Datos (Data Analysis Service)**
3. **Gestor de Alertas (Alert Manager Service)**
4. **Base de Datos (Database Service)**
5. **Interfaz de Usuario (UI Service)**
6. **Servicio de Autenticación (Authentication Service)**
7. **Servicio de Configuración (Configuration Service)**
8. **Servicio de Logs (Logging Service)**

### 2.2 Componentes Principales

#### 2.2.1 Capturador de Paquetes (Packet Capture Service)

**Responsabilidades**:
- Captura de tráfico de red en tiempo real.
- Filtrado inicial de paquetes basado en reglas predefinidas.
- Preprocesamiento de paquetes para su análisis posterior.

**Tecnologías**:
- Python con la biblioteca Scapy para la captura de paquetes.
- ZeroMQ para la transmisión eficiente de paquetes capturados al Analizador de Datos.

**Escalabilidad**:
- Despliegue en múltiples nodos de red para una cobertura completa.
- Balanceo de carga entre instancias para manejar alto volumen de tráfico.

#### 2.2.2 Analizador de Datos (Data Analysis Service)

**Responsabilidades**:
- Análisis en tiempo real de los paquetes capturados.
- Aplicación de algoritmos de detección de intrusiones.
- Generación de alertas basadas en los umbrales definidos.

**Tecnologías**:
- Python con bibliotecas como NumPy y Pandas para análisis de datos.
- TensorFlow o PyTorch para modelos de machine learning avanzados.
- Apache Kafka para el procesamiento de streams de datos en tiempo real.

**Escalabilidad**:
- Implementación de procesamiento distribuido utilizando Apache Spark.
- Uso de técnicas de paralelismo para optimizar el rendimiento.

#### 2.2.3 Gestor de Alertas (Alert Manager Service)

**Responsabilidades**:
- Recepción y procesamiento de alertas generadas por el Analizador de Datos.
- Correlación de alertas para identificar patrones de ataque complejos.
- Notificación a los administradores a través de diversos canales (email, SMS, etc.).

**Tecnologías**:
- Node.js para un manejo eficiente de operaciones asíncronas.
- RabbitMQ para la gestión de colas de mensajes de alertas.

**Escalabilidad**:
- Implementación de un sistema de colas distribuido para manejar picos de alertas.

#### 2.2.4 Base de Datos (Database Service)

**Responsabilidades**:
- Almacenamiento persistente de logs, alertas y configuraciones.
- Gestión de consultas para análisis históricos y generación de informes.

**Tecnologías**:
- MongoDB para almacenamiento de datos no estructurados (logs y alertas).
- PostgreSQL para datos estructurados (configuraciones y metadatos).
- Redis para caché y almacenamiento en memoria de datos frecuentemente accedidos.

**Escalabilidad**:
- Implementación de sharding en MongoDB para distribución de datos.
- Replicación de bases de datos para alta disponibilidad y rendimiento de lectura.

#### 2.2.5 Interfaz de Usuario (UI Service)

**Responsabilidades**:
- Presentación de dashboards y visualizaciones de alertas y estadísticas.
- Interfaz para configuración del sistema y gestión de reglas de detección.
- Visualización de logs y herramientas de búsqueda avanzada.

**Tecnologías**:
- React.js para el frontend, permitiendo una interfaz de usuario dinámica y responsive.
- GraphQL para una API flexible que permita consultas eficientes desde el frontend.

**Escalabilidad**:
- Implementación de server-side rendering para mejorar el rendimiento.
- Uso de CDN para distribución global de assets estáticos.

#### 2.2.6 Servicio de Autenticación (Authentication Service)

**Responsabilidades**:
- Gestión de autenticación y autorización de usuarios.
- Implementación de single sign-on (SSO) y multi-factor authentication (MFA).

**Tecnologías**:
- OAuth 2.0 y OpenID Connect para autenticación segura.
- JWT (JSON Web Tokens) para manejo de sesiones.

**Escalabilidad**:
- Uso de servicios de directorio distribuidos para almacenamiento de credenciales.

#### 2.2.7 Servicio de Configuración (Configuration Service)

**Responsabilidades**:
- Gestión centralizada de configuraciones para todos los microservicios.
- Actualizaciones dinámicas de configuración sin necesidad de reiniciar servicios.

**Tecnologías**:
- Spring Cloud Config para gestión centralizada de configuraciones.
- ZooKeeper para coordinación distribuida y gestión de configuraciones dinámicas.

**Escalabilidad**:
- Replicación de configuraciones en múltiples nodos para alta disponibilidad.

#### 2.2.8 Servicio de Logs (Logging Service)

**Responsabilidades**:
- Recopilación y almacenamiento centralizado de logs de todos los microservicios.
- Indexación y búsqueda eficiente de logs para análisis y debugging.

**Tecnologías**:
- ELK Stack (Elasticsearch, Logstash, Kibana) para gestión y visualización de logs.
- Fluentd para recolección y forwarding de logs.

**Escalabilidad**:
- Clusterización de Elasticsearch para manejo de grandes volúmenes de logs.

### 2.3 Interfaces y Protocolos de Comunicación entre Microservicios

1. **API RESTful**:
   - Utilizada para la comunicación entre la mayoría de los microservicios.
   - Implementación de OpenAPI (Swagger) para documentación y pruebas de API.

2. **gRPC**:
   - Usado para comunicación de alta eficiencia entre el Capturador de Paquetes y el Analizador de Datos.
   - Permite streaming bidireccional para procesamiento en tiempo real.

3. **Apache Kafka**:
   - Implementado para el streaming de datos entre el Analizador de Datos y el Gestor de Alertas.
   - Proporciona un buffer resiliente para manejar picos de tráfico.

4. **RabbitMQ**:
   - Utilizado para la gestión de colas de mensajes, especialmente para la distribución de alertas.

5. **WebSocket**:
   - Implementado en la Interfaz de Usuario para actualizaciones en tiempo real de alertas y estadísticas.

6. **GraphQL**:
   - Utilizado por la Interfaz de Usuario para realizar consultas flexibles a los datos almacenados.

### 2.4 Seguridad en la Comunicación

- Implementación de TLS/SSL para todas las comunicaciones entre microservicios.
- Uso de mTLS (mutual TLS) para autenticación mutua entre servicios.
- Implementación de API Gateway para centralizar la autenticación y autorización.
- Rotación regular de claves y certificados.

### 2.5 Monitoreo y Observabilidad

- Implementación de Prometheus para la recolección de métricas de todos los microservicios.
- Uso de Grafana para la visualización de métricas y creación de dashboards.
- Implementación de tracing distribuido con Jaeger para seguimiento de transacciones a través de múltiples servicios.
- Alertas automáticas basadas en umbrales de rendimiento y disponibilidad.

## Conclusión

Esta arquitectura de microservicios para el Sistema Distribuido de Detección de Intrusiones (IDS) está diseñada para proporcionar una solución escalable, resiliente y de alto rendimiento. La división en microservicios independientes permite una mayor flexibilidad en el desarrollo, despliegue y escalado de componentes individuales. La implementación de tecnologías modernas y protocolos eficientes asegura que el sistema pueda manejar grandes volúmenes de tráfico y detectar intrusiones en tiempo real. 

La arquitectura propuesta también facilita la evolución continua del sistema, permitiendo la integración de nuevos algoritmos de detección y la adaptación a nuevas amenazas de seguridad. Con un enfoque en la observabilidad y el monitoreo, el sistema puede ser gestionado y optimizado de manera proactiva, asegurando un alto nivel de disponibilidad y rendimiento.
