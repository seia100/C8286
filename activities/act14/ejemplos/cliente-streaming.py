# Importa el módulo grpc para utilizar gRPC en Python
import grpc

# Importa las clases generadas por protobuf (example_pb2.py)
import example_pb2

# Importa las clases generadas por gRPC (example_pb2_grpc.py)
import example_pb2_grpc

# Función que genera mensajes de chat
def generate_messages():
    # Lista de mensajes de chat que se van a enviar
    messages = [
        example_pb2.ChatMessage(user="Client1", message="Hello!"),
        example_pb2.ChatMessage(user="Client1", message="How are you?"),
        example_pb2.ChatMessage(user="Client1", message="Goodbye!")
    ]
    # Itera sobre cada mensaje y lo retorna utilizando 'yield'
    for msg in messages:
        yield msg

# Función principal que ejecuta el cliente gRPC
def run():
    # Crea un canal inseguro (sin cifrado) hacia el servidor gRPC en localhost:50051
    with grpc.insecure_channel('localhost:50051') as channel:
        # Crea un stub (cliente) para interactuar con el servicio ChatService definido en example_pb2_grpc
        stub = example_pb2_grpc.ChatServiceStub(channel)
        # Llama al método Chat del stub y pasa los mensajes generados por generate_messages
        responses = stub.Chat(generate_messages())
        # Itera sobre las respuestas recibidas del servidor
        for response in responses:
            # Imprime cada respuesta recibida con el formato "user: message"
            print(f"Received: {response.user}: {response.message}")

# Punto de entrada del script
if __name__ == '__main__':
    # Llama a la función run para iniciar el cliente gRPC
    run()
