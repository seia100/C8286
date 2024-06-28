# Algoritmos de detección y análisis distribuido
## Mejoras Implementadas

1. Algoritmos de Detección de Intrusiones Mejorados
Se ha desarrollado una clase `ImprovedIntrusionDetection` que implementa:

* Análisis basado en firmas utilizando reglas predefinidas.
* Análisis de comportamiento utilizando un modelo simple (puede ser reemplazado por un modelo de ML más complejo).
* Procesamiento asíncrono para analizar paquetes en tiempo real.

```python
async def analyze_packet(self, packet):
    if IP in packet:
        # Análisis basado en firmas
        if packet[IP].src in self.signature_rules["malicious_ip"]:
            print(f"Alerta: Tráfico detectado desde IP maliciosa {packet[IP].src}")

        # Análisis basado en comportamiento
        if self.behavior_model(packet):
            print(f"Alerta: Comportamiento sospechoso detectado de {packet[IP].src}")
```

2. Análisis Distribuido con Machine Learning
Se ha implementado un microservicio DistributedAnalysis que utiliza técnicas de machine learning para detectar anomalías:

- Preprocesamiento de datos utilizando StandardScaler.
- Clustering con KMeans para identificar patrones anómalos.
- Identificación de clusters potencialmente maliciosos.

```python
def analyze(self, data):
    preprocessed_data = self.preprocess_data(data)
    clusters = self.kmeans.fit_predict(preprocessed_data)
    
    # Identificar cluster anómalo (por ejemplo, el más pequeño)
    anomalous_cluster = np.argmin(np.bincount(clusters))
    
    anomalies = [
        data[i] for i, cluster in enumerate(clusters) if cluster == anomalous_cluster
    ]
    
    return anomalies
```

3. Comunicación entre Microservicios con gRPC
Se ha implementado un sistema de comunicación entre microservicios utilizando gRPC:

- Definición de servicios y mensajes utilizando Protocol Buffers.
- Implementación de un servidor gRPC para el servicio de análisis.
- Cliente gRPC para facilitar la comunicación entre microservicios.

```python
class AnalysisService(analysis_pb2_grpc.AnalysisServiceServicer):
    def AnalyzeTraffic(self, request, context):
        # Implementar lógica de análisis aquí
        result = f"Análisis completado para {request.data}"
        return analysis_pb2.AnalysisResponse(result=result)
```

4. Mejoras en Docker y Kubernetes
Se han realizado importantes mejoras en la containerización y orquestación del sistema:

__Docker__:

Implementación de builds multi-etapa para optimizar el tamaño de las imágenes.
Adición de healthchecks para monitorear el estado de los contenedores.
Optimización de las capas de la imagen para mejorar el tiempo de build y reducir el tamaño.

```Dockerfile
# Etapa de construcción
FROM python:3.9-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Etapa de producción
FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY . .

# Configuración de healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8080/health')"

CMD ["python", "main.py"]
```

__Kubernetes__:

- Configuración de Deployments para cada microservicio con estrategias de rollout.
- Implementación de Horizontal Pod Autoscalers (HPA) para escalar automáticamente basado en la utilización de recursos.
- Uso de ConfigMaps y Secrets para manejar la configuración y datos sensibles.

```yaml
apiVersion: autoscaling/v2beta1
kind: HorizontalPodAutoscaler
metadata:
  name: intrusion-detection-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: intrusion-detection
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      targetAverageUtilization: 70
```
5. Despliegue en Clúster de Kubernetes
Se ha implementado un proceso de despliegue y pruebas en un clúster de Kubernetes:

- Configuración del despliegue de microservicios en el clúster.
- Realización de pruebas de carga para evaluar rendimiento y escalabilidad.
- Ajuste de la configuración del clúster y microservicios según resultados.

```bash
#!/bin/bash

# Desplegar microservicios
kubectl apply -f kubernetes/

# Realizar pruebas de carga
kubectl run -i --tty load-test --image=busybox --restart=Never -- /bin/sh -c "wget -qO- http://intrusion-detection-service/test-endpoint & pid=$! && sleep 30 && kill $pid"

# Monitorear el rendimiento
kubectl top pods

# Ajustar la configuración según los resultados
kubectl scale deployment intrusion-detection --replicas=5

# Verificar el estado del despliegue
kubectl get pods
kubectl get hpa
```

### Flujo
![image]([https://github.com/seia100/c8286](https://github.com/seia100/C8286/blob/main/final_project-Luis_Arenas/sprint2/assets/flujograma-algoritmos.png))

- Containerización con Docker:
Cada componente del sistema (captura de datos, análisis, etc.) ahora se ejecuta en contenedores Docker, lo que proporciona consistencia y portabilidad.
- Orquestación con Kubernetes:
Todo el sistema se despliega en un clúster de Kubernetes, lo que permite una gestión eficiente de los contenedores y una mejor escalabilidad.
- ConfigMaps y Secrets:
Se utilizan para manejar la configuración y los datos sensibles de manera segura dentro del clúster.
Horizontal Pod Autoscaler:
Permite que el sistema escale automáticamente basado en la carga de trabajo.
- Load Balancer:
Distribuye el tráfico entrante entre las diferentes instancias del sistema.
Monitoreo y Logging:
Se ha añadido un componente dedicado para el monitoreo continuo del sistema y la recolección de logs.
- CI/CD Pipeline:
Se ha integrado un pipeline de integración y despliegue continuo para automatizar el proceso de actualización del sistema.
- Pruebas de Carga:
Se realizan pruebas de carga regulares para evaluar y optimizar el rendimiento del sistema.

## Importancia de las Mejoras

- Detección en Tiempo Real:
La implementación asíncrona permite analizar múltiples paquetes simultáneamente, mejorando la capacidad de respuesta del sistema.
- Análisis Más Sofisticado:
La combinación de análisis basado en firmas y comportamiento aumenta la precisión en la detección de amenazas conocidas y desconocidas.
- Escalabilidad y Flexibilidad:
La arquitectura de microservicios facilita la distribución de la carga de trabajo y la adición de nuevas funcionalidades.
Detección de Anomalías Avanzada:
El uso de técnicas de machine learning permite identificar patrones de ataque complejos que podrían pasar desapercibidos con métodos tradicionales.
- Comunicación Eficiente:
gRPC proporciona una comunicación rápida y eficiente entre microservicios, crucial para el análisis en tiempo real.
- Despliegue Eficiente:
La containerización con Docker y la orquestación con Kubernetes permiten un despliegue más rápido, consistente y fácil de manejar.
- Alta Disponibilidad:
Kubernetes proporciona características como auto-healing y load balancing, mejorando la disponibilidad del sistema.
- Escalabilidad Automática:
Los Horizontal Pod Autoscalers permiten que el sistema se adapte automáticamente a las variaciones en la carga de trabajo.

## Resultados esperados
![resultados esperados](https://github.com/seia100/C8286/blob/main/final_project-Luis_Arenas/sprint2/assets/Screenshot%202024-06-28%20160330.png)

## Conclusión
Las mejoras implementadas en este sprint representan un avance significativo en la capacidad del sistema para detectar y responder a amenazas de seguridad. La combinación de procesamiento asíncrono, análisis distribuido con machine learning y comunicación eficiente entre microservicios sienta las bases para un sistema de detección de intrusiones más robusto, escalable y adaptable a nuevas amenazas.
