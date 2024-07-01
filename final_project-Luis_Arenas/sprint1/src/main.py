import multiprocessing
from packet_capture import main as packet_capture_main
from data_analysis import main as data_analysis_main

def main():
    # Iniciar el proceso de captura de paquetes
    packet_capture_process = multiprocessing.Process(target=packet_capture_main)
    packet_capture_process.start()

    # Iniciar el proceso de análisis de datos
    data_analysis_process = multiprocessing.Process(target=data_analysis_main)
    data_analysis_process.start()

    # Esperar a que los procesos terminen (esto no ocurrirá en una ejecución normal)
    packet_capture_process.join()
    data_analysis_process.join()

if __name__ == "__main__":
    main()