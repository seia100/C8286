import re
from typing import List, Dict, Optional
import asyncio
from dataclasses import dataclass
from enum import Enum, auto

class AttackType(Enum):
    """
    Enumeración para representar diferentes tipos de ataques.
    """
    SQL_INJECTION = auto()  # Tipo de ataque de inyección SQL.
    XSS = auto()            # Cross-Site Scripting (XSS).
    COMMAND_INJECTION = auto()  # Inyección de comandos.

@dataclass
class Signature:
    """
    Clase para almacenar la información de una firma de ataque.
    """
    name: str  # Nombre descriptivo de la firma.
    pattern: re.Pattern  # Patrón regex compilado para detectar el ataque.
    attack_type: AttackType  # Tipo de ataque que detecta esta firma.

@dataclass
class Packet:
    """
    Clase para representar un paquete de red.
    """
    payload: str  # Contenido del paquete que será analizado.

@dataclass
class DetectionResult:
    """
    Clase para almacenar el resultado de la detección.
    """
    is_threat: bool  # Indica si el paquete contiene alguna amenaza.
    attack_types: List[AttackType]  # Lista de tipos de ataques detectados.

class SignatureBasedDetector:
    """
    Clase para detectar ataques basados en firmas predefinidas.
    """
    def __init__(self, signatures: List[Dict[str, str]]):
        """
        Inicializa el detector con una lista de firmas.
        """
        self.signatures = [
            Signature(
                name=sig['name'],
                pattern=re.compile(sig['pattern'], re.IGNORECASE),
                attack_type=AttackType[sig['attack_type']]
            )
            for sig in signatures
        ]

    async def detect(self, packet: Packet) -> DetectionResult:
        """
        Detecta de forma asíncrona si un paquete contiene alguna de las firmas de ataques conocidas.
        """
        tasks = [self._check_signature(packet.payload, sig) for sig in self.signatures]
        results = await asyncio.gather(*tasks)
        detected_attacks = [attack for attack in results if attack]
        
        return DetectionResult(
            is_threat=bool(detected_attacks),
            attack_types=detected_attacks
        )

    async def _check_signature(self, payload: str, signature: Signature) -> Optional[AttackType]:
        """
        Verifica si el contenido del paquete coincide con alguna firma.
        """
        if await asyncio.to_thread(signature.pattern.search, payload):
            return signature.attack_type
        return None

# Ejemplo de uso
async def main():
    """
    Función principal para probar el detector de firmas.
    """
    signatures = [
        {'name': 'SQL Injection', 'pattern': r'(\%27)|(\')|(\-\-)|(\%23)|(#)', 'attack_type': 'SQL_INJECTION'},
        {'name': 'Cross-Site Scripting (XSS)', 'pattern': r'<script>|<\/script>|<img.*onerror|alert\(', 'attack_type': 'XSS'},
        {'name': 'Command Injection', 'pattern': r';.*\b(cat|echo|ls|pwd|id|whoami)\b', 'attack_type': 'COMMAND_INJECTION'}
    ]
    
    detector = SignatureBasedDetector(signatures)
    packets = [
        Packet(payload='GET /login.php?username=admin\' OR \'1\'=\'1'),
        Packet(payload='POST /comment.php HTTP/1.1\nContent-Type: application/x-www-form-urlencoded\n\ncomment=<script>alert("XSS")</script>'),
        Packet(payload='GET /search.php?q=test; cat /etc/passwd'),
        Packet(payload='GET /normal.php?id=123')
    ]
    
    for packet in packets:
        result = await detector.detect(packet)
        if result.is_threat:
            print(f"Threat detected in packet: {[attack.name for attack in result.attack_types]}")
        else:
            print("No threats detected in packet")

if __name__ == "__main__":
    asyncio.run(main())
