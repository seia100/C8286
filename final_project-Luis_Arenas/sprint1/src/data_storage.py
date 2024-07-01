# Encargado de manejar el almacenamiento en mongodb

from pymongo import MongoClient
from config import *

class DataStorage:
    def __init__(self):
        """Inicializa la conexión a la base de datos MongoDB."""
        self.client = MongoClient(f'mongodb://{MONGODB_HOST}:{MONGODB_PORT}/')
        self.db = self.client[DATABASE_NAME]
        self.collection = self.db[COLLECTION_NAME]

    def store_packet(self, packet_data):
        """
        Almacena un paquete en la base de datos.
        
        :param packet_data: Diccionario con los datos del paquete.
        """
        self.collection.insert_one(packet_data)

    def get_packets(self, filter_criteria=None, limit=100):
        """
        Recupera paquetes de la base de datos.
        
        :param filter_criteria: Diccionario con criterios de filtrado (opcional).
        :param limit: Número máximo de paquetes a recuperar.
        :return: Lista de paquetes.
        """
        if filter_criteria is None:
            filter_criteria = {}
        return list(self.collection.find(filter_criteria).limit(limit))

    def close(self):
        """Cierra la conexión a la base de datos."""
        self.client.close()