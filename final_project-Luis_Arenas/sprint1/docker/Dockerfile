# Dockerfile
FROM python:3.9-slim # Utiliza la imagen base de Python 3.9 slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y libpcap-dev 
# Actualiza los repositorios de paquetes e instala libpcap-dev (necesaria para scapy)

# Establecer directorio de trabajo
WORKDIR /app # Define el directorio de trabajo dentro del contenedor

# Copiar archivos necesarios
COPY packet_capture.py config.py requirements.txt ./ 
# Copia los archivos necesarios al directorio de trabajo

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt 
# Instala las dependencias de Python desde el archivo requirements.txt

# Ejecutar el script
CMD ["python", "packet_capture.py"] 
# Define el comando a ejecutar al iniciar el contenedor
