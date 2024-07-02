import asyncio
import multiprocessing as mp
from typing import Any
from sprint1.src.packet_capture import PacketCapture  # Módulo personalizado para capturar paquetes
from sprint1.src.data_analysis import DataAnalyzer  # Módulo personalizado para analizar los datos capturados
from communication.grpc_service import serve as grpc_serve  # Servicio gRPC para comunicación externa

async def run_packet_capture(queue: asyncio.Queue) -> None:
    """
    Función asincrónica para capturar paquetes de red y encolarlos para análisis.
    
    :param queue: Cola asyncio donde se encolarán los paquetes capturados.
    """
    capture = PacketCapture()
    await capture.capture_packets(queue)  # Captura paquetes y los encola

async def run_data_analysis(queue: asyncio.Queue) -> None:
    """
    Función asincrónica para analizar paquetes de red desencolados.
    
    :param queue: Cola asyncio de donde se desencolarán los paquetes para análisis.
    """
    analyzer = DataAnalyzer()
    await analyzer.analyze_packets(queue)  # Analiza paquetes desencolados

def run_grpc_service() -> None:
    """
    Función para ejecutar el servicio gRPC que permitirá la comunicación del sistema con clientes externos.
    """
    grpc_serve()  # Lanza el servidor gRPC

async def main() -> None:
    """
    Función principal que organiza y coordina las tareas asincrónicas y los procesos.
    """
    queue: asyncio.Queue[Any] = asyncio.Queue()  # Cola para comunicación entre tareas de captura y análisis
    
    # Iniciar el servicio gRPC en un proceso separado
    grpc_process = mp.Process(target=run_grpc_service)
    grpc_process.start()
    
    # Crear tareas asincrónicas para la captura y el análisis de paquetes
    capture_task = asyncio.create_task(run_packet_capture(queue))
    analysis_task = asyncio.create_task(run_data_analysis(queue))
    
    try:
        # Ejecuta y espera a que ambas tareas asincrónicas completen su ejecución
        await asyncio.gather(capture_task, analysis_task)
    except KeyboardInterrupt:
        # Captura la interrupción por teclado para permitir una salida controlada
        print("Deteniendo el sistema...")
    finally:
        # Asegura que el proceso gRPC se detenga limpiamente al finalizar
        grpc_process.terminate()
        grpc_process.join()

if __name__ == "__main__":
    mp.set_start_method('spawn')  # Configura el método de inicio de procesos, necesario en algunos sistemas
    asyncio.run(main())  # Inicia el loop de eventos de asyncio ejecutando la función principal
