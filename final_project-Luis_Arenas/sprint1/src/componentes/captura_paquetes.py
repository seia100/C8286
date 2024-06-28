# capturador_paquetes.py

# Importa todas las funcionalidades de la librería Scapy para la manipulación de paquetes de red
import scapy.all as scapy

# Importa la librería ZeroMQ para la comunicación entre procesos
import zmq

# Define una función de callback que se ejecutará para cada paquete capturado
def packet_callback(packet):
    # Procesamiento básico del paquete capturado
    # Crea un diccionario para almacenar información relevante del paquete
    packet_info = {
        'src_ip': packet[scapy.IP].src,  # Dirección IP de origen del paquete
        'dst_ip': packet[scapy.IP].dst,  # Dirección IP de destino del paquete
        'protocol': packet[scapy.IP].proto,  # Protocolo utilizado (TCP, UDP, etc.)
        'payload': packet[scapy.Raw].load if packet.haslayer(scapy.Raw) else None  # Carga útil del paquete si existe
    }
    
    # Enviar el paquete al Analizador de Datos usando ZeroMQ
    # Crea un contexto ZeroMQ
    context = zmq.Context()
    # Crea un socket ZeroMQ tipo PUSH para enviar datos
    socket = context.socket(zmq.PUSH)
    # Conecta el socket al servicio de análisis de datos en la dirección especificada
    socket.connect("tcp://data-analyzer-service:5555")
    # Envía el diccionario con la información del paquete como un mensaje JSON
    socket.send_json(packet_info)

# Define una función para iniciar la captura de paquetes
def start_packet_capture():
    # Configuración del filtro y la interfaz para captura de paquetes
    # Inicia la captura de paquetes de red con Scapy
    # La opción prn indica la función callback a llamar para cada paquete capturado
    # El filtro se establece para capturar solo paquetes IP
    # iface especifica la interfaz de red a usar para la captura
    # La opción store=0 indica que los paquetes no se deben almacenar en memoria después de ser procesados
    scapy.sniff(prn=packet_callback, filter="ip", iface="eth0", store=0)

# Punto de entrada del script
if __name__ == "__main__":
    # Llama a la función para iniciar la captura de paquetes
    start_packet_capture()
