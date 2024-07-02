import grpc
from concurrent import futures
import time
from . import ids_pb2  # Importa las definiciones protobuf para los tipos de mensaje
from . import ids_pb2_grpc  # Importa las definiciones protobuf para los servicios gRPC

class IDSService(ids_pb2_grpc.IDSServiceServicer):
    def AnalyzePacket(self, request, context):
        """
        Método para analizar paquetes de red y determinar si representan una amenaza.
        
        :param request: El paquete de red recibido como un objeto definido por protobuf.
        :param context: Contexto de gRPC para la llamada actual.
        :return: Resultado del análisis como objeto protobuf AnalysisResult.
        """
        # Lógica inicial para determinar si un paquete es una amenaza.
        # Por ahora, es una lógica simple basada en una IP específica.
        is_threat = False
        threat_type = "None"
        if request.src_ip == "192.168.1.100":  # Simulando una amenaza para una IP específica
            is_threat = True
            threat_type = "Suspicious IP"
        return ids_pb2.AnalysisResult(is_threat=is_threat, threat_type=threat_type)

def serve():
    """
    Configura y ejecuta el servidor gRPC.
    """
    # Crea un servidor gRPC utilizando un ThreadPoolExecutor para gestionar las solicitudes concurrentes.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Añade el servicio IDSService al servidor gRPC.
    ids_pb2_grpc.add_IDSServiceServicer_to_server(IDSService(), server)
    # Configura el servidor para escuchar en el puerto 50051 en todas las interfaces de red.
    server.add_insecure_port('[::]:50051')
    # Inicia el servidor gRPC.
    server.start()
    print("Servidor gRPC iniciado en el puerto 50051")
    try:
        # Mantiene el servidor ejecutándose indefinidamente, con un ciclo que espera un día antes de revisar de nuevo.
        while True:
            time.sleep(86400)  # Un día en segundos
    except KeyboardInterrupt:
        # Permite detener el servidor de manera segura usando Ctrl+C.
        server.stop(0)

if __name__ == '__main__':
    serve()
