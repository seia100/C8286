# config.py

# Puertos para los diferentes servicios
PACKET_CAPTURE_PORT = 5000 # Puerto para el servicio de captura de paquetes
DATA_ANALYSIS_PORT = 5001 # Puerto para el servicio de análisis de datos
DATABASE_PORT = 27017  # Puerto estándar de MongoDB
UI_PORT = 3000 # Puerto para la interfaz de usuario

# Otras configuraciones globales
PACKET_BUFFER_SIZE = 65535 # Tamaño del buffer para la captura de paquetes
MAX_PACKETS_PER_BATCH = 1000 # Número máximo de paquetes a insertar en la base de datos por lote
DATABASE_NAME = "ids_database" # Nombre de la base de datos
COLLECTION_NAME = "network_packets" # Nombre de la colección

# Configuración para optimización de CPU
CPU_CORES = 4  # Ajusta esto según el número de cores de tu CPU