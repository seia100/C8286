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

#### Umbrales y criterios obligatorios🔒:
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

#### Umbrales a realizarse posteriormente 🔓:
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
- Captura de tráfico de red en tiempo real utilizando técnicas de bypass de kernel.
- Filtrado inicial de paquetes basado en reglas predefinidas.
   - Basado en BPF (Berkeley Packet Filter).
     
- Preprocesamiento y normalizacion de paquetes para su análisis posterior.

**Tecnologías**:
- Contenedor Docker basado en imagen de Python con Scapy instalado
- ZeroMQ para la transmisión eficiente de paquetes.
- eBPF compilado dentro del contenedor para filtrado a nivel de kernel
- Apache Flink desplegado como Job en Kubernetes

**Escalabilidad**:
- Utilizar DaemonSets y nodeSelector para asegurar que las instancias de la aplicación estén desplegadas en nodos con las capacidades necesarias.
-  Configurar securityContext y asignar recursos optimizados (CPU/memoria) para aplicaciones de alto rendimiento en captura de paquetes (opcional).
-   Implementar técnicas de sharding y balanceo de carga para manejar grandes volúmenes de datos de manera distribuida y eficiente.
-   Aplicar NUMA-aware computing para mejorar el rendimiento en sistemas multi-core.
-   Utilizar Kubernetes para gestionar el escalado y la administración de la infraestructura de manera eficiente.

#### 2.2.2 Analizador de Datos (Data Analysis Service)

**Responsabilidades**:
- Análisis en tiempo real de los paquetes capturados.
- Aplicación de algoritmos de detección de intrusiones.
   - Correlación de eventos multi-fuente para detección de amenazas avanzadas persistentes (APT). 
- Generación de alertas basadas en los umbrales definidos.
   - Análisis heurístico y modelos de machine learning. Dado la complejidad de la implementacion se considera en mejoras del proyecto (opcional).

**Tecnologías**:
- Python con bibliotecas como NumPy y Pandas para análisis de datos.
- TensorFlow o PyTorch para modelos de _machine & deep learning_ avanzados.
- Apache Kafka desplegado como StatefulSet en Kubernetes.
- Apache Spark para procesamiento distribuido de datos a gran escala.
   - Apache Spark configurado como Spark-on-Kubernetes

**Escalabilidad**:
- Utilizar un Deployment con HorizontalPodAutoscaler para desplegar la aplicación principal, asegurando que escale automáticamente según la demanda.
- Utilizar PersistentVolumeClaims para garantizar el almacenamiento persistente de modelos y datos temporales.
- Implementar NodeAffinity para desplegar pods que requieren GPU en nodos específicos con capacidades de GPU.
- Utilizar Apache Spark para manejar el procesamiento distribuido de datos, aplicando técnicas de _consistent hashing_ para una distribución equitativa de la carga.
   - Aplicar técnicas de paralelismo dentro de Spark para optimizar el rendimiento de las tareas de procesamiento de datos.
   - Configurar los entornos de ejecución de Spark para aprovechar las capacidades de GPU cuando sea relevante para las tareas de machine learning.


#### 2.2.3 Gestor de Alertas (Alert Manager Service)

**Responsabilidades**:
- Recepción y procesamiento de alertas generadas por el Analizador de Datos.
   - Para reducción de falsos positivos.
- Correlación de alertas para identificar patrones de ataque complejos.
   - Implementación de workflows de respuesta automatizada a incidentes.
- Notificación a los administradores a través de diversos canales (email, SMS, etc.).
   - Notificación multi-canal con soporte para escalamiento y SLAs.

**Tecnologías**: (consideraciones)
- Contenedor Docker basado en Node.js
- RabbitMQ para la gestión de colas de mensajes de alertas, considero más accesible para implementar. 
   - Apache Kafka para implementación de arquitectura de mensajería distribuida. Ademas estrategisas como lo es MPI, _Actor Model_, Cola de mensajes.
   - Relacion con la información: [Message Queue](https://medium.com/@rcougil/software-colas-de-mensajes-qu%C3%A9-son-y-para-qu%C3%A9-sirven-1a1d8e7f63f3)
   - RabbitMQ desplegado como StatefulSet en Kubernetes.
- Rundeck para orquestación de tareas de respuesta a incidentes.
   - Es importante mencionar e implementar técnicas de [SOAR](https://www.ibm.com/es-es/topics/security-orchestration-automation-response) o también se puede consultar el siguiente _link_: [Security Orchestration, Automation and Response](https://ciberseguridadmax.com/soar/)

**Escalabilidad**:
- Implementar un sistema de colas distribuido (por ejemplo, Apache Kafka o RabbitMQ) para gestionar picos de tráfico y alertas.
- Desplegar la aplicación como un Deployment en Kubernetes con la estrategia de RollingUpdate para asegurar actualizaciones sin interrupciones.
- Configurar readinessProbe y livenessProbe para monitorear la salud de los pods y garantizar que solo los pods saludables manejen tráfico.
- Utilizar ConfigMaps para gestionar las configuraciones de la aplicación, permitiendo cambios dinámicos y centralizados.
- Implementar PodDisruptionBudget para asegurar que siempre haya un número mínimo de pods disponibles durante actualizaciones o eventos de mantenimiento.


#### 2.2.4 Base de Datos (Database Service)
Servicio de Persistencia y Consulta de Datos (DPQS)

**Responsabilidades**:
- Almacenamiento persistente de logs, alertas y configuraciones.
- Gestión de consultas para análisis históricos y generación de informes.
- Soporte para consultas complejas y análisis forense (opcional)

**Tecnologías**:
- MongoDB para almacenamiento de datos no estructurados (logs y alertas).
   - MongoDB desplegado como StatefulSet en Kubernetes 
- PostgreSQL para datos estructurados (configuraciones y metadatos).
   - PostgreSQL desplegado como StatefulSet con operador específico
- Redis para caché y almacenamiento en memoria de datos frecuentemente accedidos.
   - Redis desplegado como StatefulSet para caché distribuido 

**Escalabilidad**:
- Configurar StorageClass en Kubernetes para proporcionar almacenamiento persistente dinámicamente según las necesidades de los pods.
- Implementar CronJobs para realizar backups automáticos de los datos críticos, asegurando la recuperación de datos en caso de fallo.
- Implementar servicios headless para permitir la comunicación directa entre los pods, mejorando la eficiencia.
- Configurar MongoDB con sharding basado en rangos temporales para distribuir los datos de manera eficiente.
- Implementar la replicación de bases de datos para asegurar alta disponibilidad y mejorar el rendimiento de lectura.
- Utilizar técnicas de compresión avanzada y tiering de almacenamiento para optimizar el uso y el rendimiento del almacenamiento.

#### 2.2.5 Interfaz de Usuario (UI Service)
Servicio de Interfaz de Usuario y Visualización (UIVS)

**Responsabilidades**:
- Presentación de dashboards y visualizaciones de alertas y estadísticas.
- Interfaz para configuración del sistema y gestión de reglas de detección.
- Visualización de logs y herramientas de búsqueda avanzada.

**Tecnologías**:
- React.js para el frontend, permitiendo una interfaz de usuario dinámica y responsive. React con TypeScript para desarrollo de frontend robusto y tipado (tratare de interactuar con estas tecnologías). Caso contrario usaré herremientas como lo es Dart(Flutter).
- D3.js y WebGL para visualizaciones de datos de alto rendimiento.
- GraphQL ocn Apollo para una API flexible que permita consultas eficientes desde el frontend.

**Escalabilidad**:
- Implementación de server-side rendering para mejorar el rendimiento.
   - Implementación de técnicas de Code Splitting y Lazy Loading para optimización de carga.
- Uso de [CDN](https://aws.amazon.com/es/what-is/cdn/) para distribución global de assets estáticos. Es decir, la autilizacion de [_Edge Computing_](https://www.ibm.com/es-es/topics/edge-computing) para la distribucion global de contenido estático y dinámico nos permite ver diferentes directrices de desarrollo.


#### 2.2.6 Servicio de Autenticación (Authentication Service)
Servicio de Autenticación y Control de Acceso (AACS)

**Responsabilidades**:
- Gestión de autenticación y autorización de usuarios basada en roles (RBAC) y atributos (ABAC)
- Implementación de single sign-on (SSO) y multi-factor authentication (MFA).

**Tecnologías**:
- OAuth 2.0 y OpenID Connect para autenticación segura.
- Keycloak para gestión centralizada de identidad y acceso.
- JWT (JSON Web Tokens) para manejo de sesiones.
- LDAP y Active Directory para integración con directorios corporativos.

**Escalabilidad**:
- Uso de servicios de directorio distribuidos para almacenamiento de credenciales.
   - Caching distribuido de tokens y sesiones.
- 
#### 2.2.7 Servicio de Configuración (Configuration Service)
Servicio de Gestión de Configuración y Políticas (CPMS)

**Responsabilidades**:
- Gestión centralizada de configuraciones y politicas de seguridad para todos los microservicios.
- Actualizaciones dinámicas de configuración sin necesidad de reiniciar servicios.
   - Versionado y rollback de configuraciones.
- 

**Tecnologías**:
- [_Spring Cloud Config_](https://spring.io/projects/spring-cloud-config) para gestión centralizada de configuraciones.
- [ZooKeeper](https://www.geeksforgeeks.org/what-is-apache-zookeeper/) para coordinación distribuida y gestión de configuraciones dinámicas. También considerar [Consul] 
- [etcd](https://www.ibm.com/topics/etcd) para almacenamiento distribuido de configuraciones.

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
      - Utilizado por UIVS para actualizaciones en tiempo real de alertas y métricas. 

6. **GraphQL**:
   - Utilizado por la Interfaz de Usuario para realizar consultas flexibles a los datos almacenados.
      - UIVS para realizar queries flexibles a DPQS.
   - Implementación de Federation para composición de schemas distribuidos.

### 2.4 Seguridad en la Comunicación

- Implementación de TLS/SSL para todas las comunicaciones entre microservicios.
- Uso de mTLS (mutual TLS) para autenticación y encriptación mutua entre servicios.
- Implementación de API Gateway para centralizar la autenticación y autorización.
   - Ttécnicas de ofuscación y tokenización para datos sensibles en tránsito y reposo.
- Rotación regular de claves y certificados.
   - Uso de protocolos como ACME

### 2.5 Monitoreo y Observabilidad

- Implementación de Prometheus para la recolección de métricas de todos los microservicios.
- Uso de Grafana para la visualización de métricas y creación de dashboards.
- Implementación de tracing distribuido con Jaeger para seguimiento de transacciones a través de múltiples servicios.
- Alertas automáticas basadas en umbrales de rendimiento y disponibilidad.

## Conclusión

Esta arquitectura de microservicios para el Sistema Distribuido de Detección de Intrusiones (IDS) está diseñada para proporcionar una solución escalable, resiliente y de alto rendimiento. La división en microservicios independientes permite una mayor flexibilidad en el desarrollo, despliegue y escalado de componentes individuales. La implementación de tecnologías modernas y protocolos eficientes asegura que el sistema pueda manejar grandes volúmenes de tráfico y detectar intrusiones en tiempo real. 

La arquitectura propuesta también facilita la evolución continua del sistema, permitiendo la integración de nuevos algoritmos de detección y la adaptación a nuevas amenazas de seguridad. Con un enfoque en la observabilidad y el monitoreo, el sistema puede ser gestionado y optimizado de manera proactiva, asegurando un alto nivel de disponibilidad y rendimiento.
