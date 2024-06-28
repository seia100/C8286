import grpc
from concurrent import futures
import analysis_pb2
import analysis_pb2_grpc

class AnalysisService(analysis_pb2_grpc.AnalysisServiceServicer):
    def AnalyzeTraffic(self, request, context):
        # Implementar lógica de análisis aquí
        result = f"Análisis completado para {request.data}"
        return analysis_pb2.AnalysisResponse(result=result)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    analysis_pb2_grpc.add_AnalysisServiceServicer_to_server(AnalysisService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

# Cliente gRPC
class AnalysisClient:
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = analysis_pb2_grpc.AnalysisServiceStub(self.channel)

    def analyze_traffic(self, data):
        request = analysis_pb2.AnalysisRequest(data=data)
        response = self.stub.AnalyzeTraffic(request)
        return response.result

# Uso del cliente
client = AnalysisClient()
result = client.analyze_traffic("Datos de tráfico de ejemplo")
print(result)
