import unittest
from unittest.mock import patch, MagicMock
from sprint1.src.data_storage import DataStorage  # Asumiendo que la clase DataStorage está definida en src.data_storage

class TestDataStorage(unittest.TestCase):
    """
    Clase de prueba para DataStorage que interactúa con MongoDB.
    """

    @patch('pymongo.MongoClient')
    def setUp(self, mock_client):
        """
        Método que se ejecuta antes de cada prueba. Configura el entorno de prueba.
        
        :param mock_client: Mock del cliente de MongoDB.
        """
        # Inicializa una instancia de DataStorage, que se supone que crea una conexión a MongoDB.
        self.data_storage = DataStorage()
        # Configura un mock para la colección dentro de MongoDB para poder verificar las interacciones.
        self.mock_collection = mock_client.return_value.__getitem__.return_value.get_item.return_value

    def test_store_packet(self):
        """
        Prueba el método store_packet para asegurarse de que almacena un paquete correctamente.
        """
        # Define un paquete de datos de ejemplo.
        packet_data = {'src': '192.168.1.1', 'dst': '192.168.1.2', 'proto': 6}
        # Llama al método store_packet con los datos del paquete.
        self.data_storage.store_packet(packet_data)
        # Verifica que el método insert_one fue llamado una vez y con los datos correctos.
        self.mock_collection.insert_one.assert_called_once_with(packet_data)

    def test_get_packets(self):
        """
        Prueba el método get_packets para asegurarse de que recupera paquetes correctamente.
        """
        # Configura un mock para el cursor que emula el comportamiento de MongoDB find().
        mock_cursor = MagicMock()
        mock_cursor.limit.return_value = [{'src': '192.168.1.1', 'dst': '192.168.1.2', 'proto': 6}]
        self.mock_collection.find.return_value = mock_cursor
        
        # Llama al método get_packets.
        packets = self.data_storage.get_packets()
        # Verifica que el tamaño de los paquetes recuperados sea el esperado.
        self.assertEqual(len(packets), 1)
        # Asegura que find fue llamado correctamente y que se aplicó un límite al cursor.
        self.mock_collection.find.assert_called_once_with({})
        mock_cursor.limit.assert_called_once_with(100)

    def test_close(self):
        """
        Prueba el método close para asegurarse de que cierra la conexión a la base de datos correctamente.
        """
        # Llama al método close.
        self.data_storage.close()
        # Verifica que el método close del cliente de MongoDB fue llamado una vez.
        self.data_storage.client.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
