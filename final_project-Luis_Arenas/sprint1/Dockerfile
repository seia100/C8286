# Utiliza la imagen base de Python 3.9 slim
FROM python:3.9-slim

# Install las dependencias del sistema necesarias para Scapy
RUN apt-get update && apt-get install -y libpcap-dev

# Establece el directorio de trabajo dentro del contenedor
WORKDIR  /app

# Copia todos los archivos Python y el requirements.txt al directorio de trabajo
COPY src/*.py config.py requirements.txt ./

# Install las dependencias de Python especificadas en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Especifica el comando para ejecutar la app
CMD ["python","main.py"]
