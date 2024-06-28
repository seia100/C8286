import asyncio
from scapy.all import sniff, IP

class ImprovedIntrusionDetection:
    def __init__(self):
        self.signature_rules = self.load_signature_rules()
        self.behavior_model = self.load_behavior_model()

    def load_signature_rules(self):
        # Cargar reglas de firmas desde una base de datos o archivo
        return {"malicious_ip": ["192.168.1.100", "10.0.0.1"]}

    def load_behavior_model(self):
        # Cargar modelo de comportamiento (podría ser un modelo de ML)
        return lambda packet: sum(byte for byte in packet[IP].payload) > 1000

    async def analyze_packet(self, packet):
        if IP in packet:
            # Análisis basado en firmas
            if packet[IP].src in self.signature_rules["malicious_ip"]:
                print(f"Alerta: Tráfico detectado desde IP maliciosa {packet[IP].src}")

            # Análisis basado en comportamiento
            if self.behavior_model(packet):
                print(f"Alerta: Comportamiento sospechoso detectado de {packet[IP].src}")

    async def capture_and_analyze(self):
        while True:
            packet = await asyncio.to_thread(sniff, count=1, store=1)
            await self.analyze_packet(packet[0])

    def run(self):
        asyncio.run(self.capture_and_analyze())

if __name__ == "__main__":
    detector = ImprovedIntrusionDetection()
    detector.run()
