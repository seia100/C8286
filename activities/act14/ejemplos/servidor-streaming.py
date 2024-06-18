# Importa el módulo futures del paquete concurrent para manejar múltiples hilos
from concurrent import futures

# Importa el módulo grpc para utilizar gRPC en Python
import grpc

# Importa las clases generadas por protobuf (example_pb2.py)
import example_pb2

# Importa las clases generadas por gRPC (example_pb2_grpc.py)
import example_pb2_grpc

# Define la clase ChatService que implementa el servicio ChatService definido en example_pb2_grpc
class ChatService(example_pb2_grpc.ChatServiceServicer):
    # Implementa el método Chat que maneja la comunicación del servicio
    def Chat(self, request_iterator, context):
        # Itera sobre los mensajes recibidos del cliente
        for chat_message in request_iterator:
            # Crea una respuesta para cada mensaje recibido
            response_message = example_pb2.ChatMessage(
                user="Server",
                message=f"Received from {chat_message.user}: {chat_message.message}"
            )
            # Yields la respuesta al cliente
            yield response_message

# Define la función para iniciar el servidor
def serve():
    # Crea un servidor gRPC con un executor de hilos, max 10 hilos
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Añade la implementación del servicio ChatService al servidor
    example_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    # Configura el servidor para escuchar en el puerto 50051 de todas las interfaces IP
    server.add_insecure_port('[::]:50051')
    # Inicia el servidor
    server.start()
    # Espera a que el servidor termine
    server.wait_for_termination()

# Punto de entrada del script
if __name__ == '__main__':
    # Llama a la función serve para iniciar el servidor
    serve()
