# Guía de Despliegue del Sistema IDS

## Requisitos Previos
- Kubernetes cluster v1.19+
- kubectl configurado
- Helm v3+
- Docker

## Pasos de Despliegue

1. Clonar el repositorio:
   ```
   git clone https://github.com/your-org/ids-system.git
   cd ids-system
   ```

2. Construir y pushear las imágenes Docker:
   ```
   docker build -t your-registry.com/ids-system:v3 .
   docker push your-registry.com/ids-system:v3
   ```

3. Configurar secrets:
   ```
   kubectl create secret generic ids-secrets --from-literal=mongodb-uri='mongodb://user:pass@host:port/db'
   ```

4. Desplegar el sistema:
   ```
   kubectl apply -f kubernetes/
   ```

5. Verificar el despliegue:
   ```
   kubectl get pods
   kubectl get services
   kubectl get ingress
   ```

6. Configurar DNS para el Ingress.

7. Acceder al dashboard:
   Abrir https://ids.yourdomain.com en un navegador.

## Monitoreo y Mantenimiento

- Revisar logs: `kubectl logs deployment/ids-system`
- Escalar: `kubectl scale deployment/ids-system --replicas=5`
- Actualizar: Modificar la imagen en `deployment.yaml` y aplicar los cambios.

## Solución de Problemas

- Si los pods no arrancan, revisar los logs y los eventos:
  ```
  kubectl describe pod <pod-name>
  ```

- Para problemas de red, verificar los servicios e ingress:
  ```
  kubectl get services
  kubectl get ingress
  ```

- Si hay problemas de rendimiento, considerar ajustar los recursos en `deployment.yaml`.