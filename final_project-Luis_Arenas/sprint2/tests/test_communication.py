# test_communication.py
#hemos implementado comunicación gRPC.

import unittest
import grpc
from concurrent import futures
from src.communication.grpc_service import IDSService  # Asume que IDSService está correctamente implementado
import ids_pb2  # Asume que ids_pb2 está generado por el compilador de protocol buffers
import ids_pb2_grpc  # Asume que ids_pb2_grpc está generado por el compilador de protocol buffers

class TestCommunication(unittest.TestCase):
    """
    Suite de pruebas para el servicio de comunicación gRPC que maneja la detección de amenazas en paquetes de red.
    """
    
    def setUp(self):
        """
        Configura el entorno de pruebas, inicializando el servidor gRPC y añadiendo el servicio IDSService.
        """
        # Crea un servidor gRPC utilizando un ThreadPoolExecutor para manejar las solicitudes concurrentes.
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        # Añade el servicio IDSService al servidor.
        ids_pb2_grpc.add_IDSServiceServicer_to_server(IDSService(), self.server)
        # Configura el servidor para escuchar en el puerto 50051 en todas las interfaces disponibles.
        self.server.add_insecure_port('[::]:50051')
        # Inicia el servidor gRPC.
        self.server.start()

    def tearDown(self):
        """
        Limpia después de cada prueba, deteniendo el servidor gRPC.
        """
        # Detiene el servidor gRPC de forma inmediata.
        self.server.stop(0)

    def test_analyze_packet(self):
        """
        Prueba la funcionalidad de análisis de paquetes del servicio gRPC para asegurar que identifica amenazas correctamente.
        """
        # Crea un canal de comunicación gRPC inseguro para conectarse al servidor.
        with grpc.insecure_channel('localhost:50051') as channel:
            # Crea un stub (cliente) para el servicio IDSService.
            stub = ids_pb2_grpc.IDSServiceStub(channel)
            # Define un paquete con detalles específicos para enviar al servicio.
            packet = ids_pb2.Packet(
                src_ip="192.168.1.100",
                dst_ip="10.0.0.1",
                src_port=12345,
                dst_port=80,
                protocol="TCP",
                payload=b"GET /index.html HTTP/1.1"
            )
            # Envía el paquete al servicio y recibe la respuesta.
            response = stub.AnalyzePacket(packet)
            # Verifica que la respuesta indique correctamente que se trata de una amenaza.
            self.assertTrue(response.is_threat)
            # Verifica que el tipo de amenaza identificado sea el esperado.
            self.assertEqual(response.threat_type, "Suspicious IP")

if __name__ == '__main__':
    unittest.main()
