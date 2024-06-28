# Ataques de fuerza bruta
# Ejemplo de ataque de fuerza bruta con python https://www.youtube.com/watch?v=2iLy6kaYLhw)

# Brute Force Detection Service
# Importamos las bibliotecas necesarias.
import time  # Biblioteca para manejar el tiempo.
from collections import defaultdict  # defaultdict para crear diccionarios con valores por defecto.

# Definimos los parámetros.
THRESHOLD = 5  # Número máximo de intentos fallidos permitidos.
TIME_FRAME = 60  # 1 minuto en segundos.

# Creamos un diccionario para almacenar los intentos fallidos de inicio de sesión.
failed_attempts = defaultdict(list)  # Cada dirección IP tendrá una lista de timestamps de intentos fallidos.

# Definimos la función para detectar ataques de fuerza bruta.
def detect_brute_force(ip_address, timestamp):
    # Añadimos el timestamp del intento fallido a la lista correspondiente a la dirección IP.
    failed_attempts[ip_address].append(timestamp)
    # Mantenemos solo los intentos que ocurrieron dentro del TIME_FRAME.
    failed_attempts[ip_address] = [t for t in failed_attempts[ip_address] if t > timestamp - TIME_FRAME]

    # Si el número de intentos fallidos excede el THRESHOLD, retornamos True (se detecta un ataque de fuerza bruta).
    if len(failed_attempts[ip_address]) > THRESHOLD:
        return True
    # Si no se excede el THRESHOLD, retornamos False.
    return False

# Ejemplo de uso del servicio de detección.
if __name__ == "__main__":
    # Ejemplo de logs de intentos de inicio de sesión fallidos.
    logs = [("192.168.1.1", int(time.time()))]  # Para mejorar agregar la lógica para analizar los logs.

    # Iteramos sobre los logs.
    for ip, timestamp in logs:
        # Verificamos si se detecta un ataque de fuerza bruta para la dirección IP y el timestamp actual.
        if detect_brute_force(ip, timestamp):
            # Si se detecta un ataque, imprimimos un mensaje de alerta.
            print(f"Brute force attack detected from IP: {ip}")


