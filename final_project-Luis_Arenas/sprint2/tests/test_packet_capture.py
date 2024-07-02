import unittest
from unittest.mock import patch, MagicMock
from src.packet_capture import capture_packets, process_packets

class TestPacketCapture(unittest.TestCase):

    @patch('scapy.all.sniff')
    def test_capture_packets(self, mock_sniff):
        # Simula una cola de paquetes
        mock_queue = MagicMock()
        
        # Llama a la función capture_packets
        capture_packets(mock_queue)
        
        # Verifica que se llamó a scapy.sniff
        mock_sniff.assert_called_once()

    @patch('pymongo.MongoClient')
    def test_process_packets(self, mock_client):
        # Simula una cola de paquetes y un cliente MongoDB
        mock_queue = MagicMock()
        mock_queue.get.side_effect = [
            MagicMock(src='192.168.1.1', dst='192.168.1.2', proto=6, time=1234567890),
            None  # Para terminar el bucle
        ]
        
        # Llama a la función process_packets
        process_packets(mock_queue, mock_client)
        
        # Verifica que se insertó un paquete en la base de datos
        mock_client.__getitem__().assert_called_once()
        mock_client.__getitem__().__getitem__().insert_many.assert_called_once()

if __name__ == '__main__':
    unittest.main()