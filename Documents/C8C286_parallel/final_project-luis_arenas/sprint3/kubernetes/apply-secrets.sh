#!/bin/bash

# Generar una API key aleatoria
API_KEY=$(openssl rand -base64 32)

# Aplicar el secreto, reemplazando la variable API_KEY
sed "s|\${API_KEY}|$API_KEY|g" kubernetes/secrets.yaml | kubectl apply -f -

echo "Secreto aplicado con éxito. La API key ha sido generada y almacenada de forma segura."