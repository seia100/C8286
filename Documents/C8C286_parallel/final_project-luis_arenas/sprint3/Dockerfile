# Etapa de construcción
FROM python:3.9-slim AS builder

WORKDIR /app

# Copiar los archivos de requerimientos e instalar dependencias
COPY sprint3/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Etapa de producción
FROM python:3.9-slim

# Instalar herramientas necesarias
RUN apt-get update && apt-get install -y \
    curl \
    openssl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar los archivos necesarios desde la etapa de construcción
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copiar todos los archivos del sprint 3
COPY sprint3/ .

# Dar permisos de ejecución al script apply_secrets.sh y docker-entrypoint.sh
RUN chmod +x ./kubernetes/apply_secrets.sh && \
    chmod +x ./docker-entrypoint.sh

# Exponer el puerto de la aplicación
EXPOSE 5000

# Usar el script de entrada como punto de entrada
ENTRYPOINT ["./docker-entrypoint.sh"]

# Comando por defecto para ejecutar la aplicación
CMD ["python", "src/main.py"]