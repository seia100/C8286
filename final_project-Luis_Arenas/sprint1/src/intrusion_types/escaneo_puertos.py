# Port Scanning Detection Service
# Importamos las bibliotecas necesarias.
from collections import defaultdict  # defaultdict para crear diccionarios con valores por defecto.

# Definimos los parámetros.
THRESHOLD = 100  # Número máximo de escaneos de puertos permitidos.
TIME_FRAME = 300  # 5 minutos en segundos.

# Creamos un diccionario para almacenar los escaneos de puertos.
# La estructura del diccionario es: {ip_address: {port: [timestamps]}}
port_scans = defaultdict(lambda: defaultdict(list))  # Cada dirección IP tendrá un diccionario de puertos con listas de timestamps.

# Definimos la función para detectar escaneos de puertos.
def detect_port_scanning(ip_address, port, timestamp):
    # Añadimos el timestamp del escaneo de puerto a la lista correspondiente a la dirección IP y el puerto.
    port_scans[ip_address][port].append(timestamp)
    # Mantenemos solo los intentos que ocurrieron dentro del TIME_FRAME.
    for p in port_scans[ip_address]:
        port_scans[ip_address][p] = [t for t in port_scans[ip_address][p] if t > timestamp - TIME_FRAME]

    # Calculamos el número total de escaneos de puertos para la dirección IP dentro del TIME_FRAME.
    total_scans = sum(len(port_scans[ip_address][p]) for p in port_scans[ip_address])
    
    # Si el número total de escaneos de puertos excede el THRESHOLD, retornamos True (se detecta un escaneo de puertos).
    if total_scans > THRESHOLD:
        return True
    # Si no se excede el THRESHOLD, retornamos False.
    return False

# Ejemplo de uso del servicio de detección.
if __name__ == "__main__":
    # Ejemplo de logs de escaneos de puertos.
    logs = [("192.168.1.1", 22, int(time.time()))]  # Aquí puedes agregar la lógica para analizar los logs.

    # Iteramos sobre los logs.
    for ip, port, timestamp in logs:
        # Verificamos si se detecta un escaneo de puertos para la dirección IP y el puerto con el timestamp actual.
        if detect_port_scanning(ip, port, timestamp):
            # Si se detecta un escaneo de puertos, imprimimos un mensaje de alerta.
            print(f"Port scanning detected from IP: {ip}")
