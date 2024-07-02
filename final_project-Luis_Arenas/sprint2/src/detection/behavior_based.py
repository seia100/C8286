from typing import Dict, List, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import asyncio
import multiprocessing as mp

@dataclass
class IPStats:
    """Clase para mantener estadísticas de tráfico de cada IP."""
    packet_count: int = 0  # Contador de paquetes recibidos de la IP
    byte_count: int = 0    # Suma del tamaño de los paquetes recibidos
    port_set: Set[int] = field(default_factory=set)  # Conjunto de puertos destino únicos

@dataclass
class Packet:
    """Representa un paquete de red básico."""
    src_ip: str           # Dirección IP de origen del paquete
    dst_port: int         # Puerto de destino del paquete
    length: int           # Longitud del paquete en bytes

@dataclass
class AnomalyResult:
    """Resultados de la detección de anomalías."""
    anomalous_ips: List[str]                # Lista de IPs consideradas anómalas
    reasons: Dict[str, List[str]]           # Diccionario de razones por las que cada IP es considerada anómala

class BehaviorBasedDetector:
    def __init__(self, threshold_packet_count: int = 1000, 
                 threshold_byte_count: int = 1_000_000, 
                 threshold_unique_ports: int = 50):
        """
        Inicializa el detector con umbrales para detección de anomalías.
        """
        self.ip_stats: Dict[str, IPStats] = defaultdict(IPStats)  # Estadísticas de IP
        self.threshold_packet_count = threshold_packet_count  # Umbral de paquetes
        self.threshold_byte_count = threshold_byte_count      # Umbral de bytes
        self.threshold_unique_ports = threshold_unique_ports  # Umbral de puertos únicos

    async def update_stats(self, packet: Packet) -> None:
        """
        Asíncronamente actualiza estadísticas para una IP dada basada en el paquete recibido.
        """
        stats = self.ip_stats[packet.src_ip]
        stats.packet_count += 1
        stats.byte_count += packet.length
        stats.port_set.add(packet.dst_port)

    async def detect_anomalies(self) -> AnomalyResult:
        """
        Detecta anomalías basadas en el comportamiento de las IPs observadas.
        """
        with mp.Pool() as pool:
            results = pool.starmap(self._check_anomaly, self.ip_stats.items())

        anomalous_ips = []
        reasons = defaultdict(list)
        for ip, anomaly_info in results:
            if anomaly_info:
                anomalous_ips.append(ip)
                reasons[ip].extend(anomaly_info)

        return AnomalyResult(anomalous_ips=anomalous_ips, reasons=dict(reasons))

    def _check_anomaly(self, ip: str, stats: IPStats) -> Tuple[str, List[str]]:
        """
        Verifica si una IP específica muestra comportamiento anómalo.
        """
        reasons = []
        if stats.packet_count > self.threshold_packet_count:
            reasons.append(f"High packet count: {stats.packet_count}")
        if stats.byte_count > self.threshold_byte_count:
            reasons.append(f"High byte count: {stats.byte_count}")
        if len(stats.port_set) > self.threshold_unique_ports:
            reasons.append(f"Many unique ports: {len(stats.port_set)}")
        return ip, reasons

    def reset_stats(self) -> None:
        """
        Resetea todas las estadísticas de IPs.
        """
        self.ip_stats.clear()

async def main():
    """
    Función principal para demostrar el uso del detector.
    """
    detector = BehaviorBasedDetector()
    
    # Simular el procesamiento de paquetes
    packets = [
        Packet(src_ip='192.168.1.100', dst_port=80, length=100),
        Packet(src_ip='192.168.1.100', dst_port=443, length=200),
        Packet(src_ip='192.168.1.101', dst_port=22, length=50),
    ] * 500  # Multiplicar para simular tráfico alto

    # Actualizar estadísticas de forma asíncrona
    update_tasks = [detector.update_stats(packet) for packet in packets]
    await asyncio.gather(*update_tasks)
    
    # Detectar anomalías
    result = await detector.detect_anomalies()
    
    if result.anomalous_ips:
        print("Anomalous IPs detected:")
        for ip in result.anomalous_ips:
            print(f"IP: {ip}")
            for reason in result.reasons[ip]:
                print(f"  - {reason}")
    else:
        print("No anomalies detected.")

if __name__ == "__main__":
    asyncio.run(main())
