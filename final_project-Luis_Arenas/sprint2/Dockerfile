# Utiliza la imagen base de Python 3.9 slim
FROM python:3.9-slim

# Instala las dependencias del sistema necesarias
RUN apt-get update && apt-get install -y libpcap-dev

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia todos los archivos Python y el requirements.txt al directorio de trabajo
COPY src/ ./src/
COPY requirements.txt ./

# Instala las dependencias de Python especificadas en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Genera los archivos gRPC
RUN python -m grpc_tools.protoc -I./src/communication --python_out=./src/communication --grpc_python_out=./src/communication ./src/communication/ids.proto

# Expone el puerto para gRPC
EXPOSE 50051

# Especifica el comando para ejecutar la app
CMD ["python", "src/main.py"]