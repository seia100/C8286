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
