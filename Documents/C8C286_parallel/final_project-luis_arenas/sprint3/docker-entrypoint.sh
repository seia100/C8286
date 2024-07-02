#!/bin/bash
set -e

# Aplicar los secretos si estamos en un entorno Kubernetes
if [ -f "/var/run/secrets/kubernetes.io/serviceaccount/namespace" ]; then
    echo "Detectado entorno Kubernetes. Aplicando secretos..."
    ./kubernetes/apply_secrets.sh
else
    echo "No se detectó entorno Kubernetes. Omitiendo la aplicación de secretos."
fi

# Asegurarse de que las variables de entorno necesarias estén configuradas
if [ -z "$MONGODB_URI" ]; then
    echo "Error: MONGODB_URI no está configurado"
    exit 1
fi

if [ -z "$API_KEY" ]; then
    echo "Error: API_KEY no está configurado"
    exit 1
fi

# Ejecutar el comando proporcionado (normalmente, iniciar la aplicación)
exec "$@"