#!/bin/bash

# Iniciar el servidor en segundo plano
python3 servidor.py &

# Espera breve para asegurar que el servidor esté listo
sleep 5

# Ejecutar el cliente
python3 cliente.py

