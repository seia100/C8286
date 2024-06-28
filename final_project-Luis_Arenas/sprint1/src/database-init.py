# db_init.py

from pymongo import MongoClient
from config import * # Importa las configuraciones globales

def init_database():
    """
    Inicializa la base de datos y crea las colecciones necesarias.
    """
    client = MongoClient(f'mongodb://localhost:{DATABASE_PORT}/') # Crea un cliente de MongoDB
    db = client[DATABASE_NAME] # Obtiene la base de datos

    # Crear colección para paquetes de red
    if COLLECTION_NAME not in db.list_collection_names(): # Verifica si la colección ya existe
        db.create_collection(COLLECTION_NAME) # Crea la colección si no existe
        print(f"Colección {COLLECTION_NAME} creada.")

    # Crear índices para mejorar el rendimiento de las consultas
    db[COLLECTION_NAME].create_index("time") # Crea un índice para el campo "time"
    db[COLLECTION_NAME].create_index("src") # Crea un índice para el campo "src"
    db[COLLECTION_NAME].create_index("dst") # Crea un índice para el campo "dst"

    print("Inicialización de la base de datos completada.")

if __name__ == "__main__":
    init_database() # Ejecuta la función init_database si el script se ejecuta directamente