import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from typing import List, Dict
import multiprocessing as mp

class ClusteringAnalyzer:
    def __init__(self, eps: float = 0.5, min_samples: int = 5):
        """
        Inicializa el analizador de clustering con configuración específica para DBSCAN.
        
        :param eps: Radio máximo de la vecindad para considerar puntos como parte del mismo cluster.
        :param min_samples: Número mínimo de puntos necesarios para formar un cluster.
        """
        # Escalador para normalizar los datos antes de aplicar DBSCAN.
        self.scaler = StandardScaler()
        # Inicializa DBSCAN con los parámetros dados.
        self.dbscan = DBSCAN(eps=eps, min_samples=min_samples)

    def preprocess_data(self, data: List[Dict[str, float]]) -> np.ndarray:
        """
        Preprocesa los datos para que sean aptos para el análisis de clustering.
        
        :param data: Lista de diccionarios con información de los paquetes.
        :return: Datos normalizados como array de numpy.
        """
        # Extrae características específicas de cada paquete para el análisis.
        features = np.array([[d['packet_size'], d['protocol'], d['src_port'], d['dst_port']] for d in data])
        # Normaliza las características para mejorar la efectividad de DBSCAN.
        return self.scaler.fit_transform(features)

    def detect_anomalies(self, data: List[Dict[str, float]]) -> List[int]:
        """
        Detecta paquetes anómalos utilizando DBSCAN sobre los datos preprocesados.
        
        :param data: Lista de diccionarios con información de los paquetes.
        :return: Índices de los paquetes considerados anómalos.
        """
        # Preprocesa los datos para normalizarlos.
        preprocessed_data = self.preprocess_data(data)
        # Usa multiprocessing para dividir la tarea de clustering entre los procesadores disponibles.
        with mp.Pool() as pool:
            # Divide los datos normalizados en partes iguales según el número de CPUs.
            chunks = np.array_split(preprocessed_data, mp.cpu_count())
            # Aplica clustering a cada parte en paralelo.
            results = pool.map(self._cluster_chunk, chunks)
        # Concatena los resultados de cada proceso.
        clusters = np.concatenate(results)
        # Identifica los índices de los puntos clasificados como ruido (-1).
        return np.where(clusters == -1)[0].tolist()

    def _cluster_chunk(self, chunk: np.ndarray) -> np.ndarray:
        """
        Aplica DBSCAN a un fragmento de los datos.
        
        :param chunk: Fragmento de datos normalizados.
        :return: Etiquetas de cluster para el fragmento.
        """
        # Aplica DBSCAN al fragmento y devuelve las etiquetas de cluster.
        return self.dbscan.fit_predict(chunk)

# Ejemplo de uso
if __name__ == "__main__":
    analyzer = ClusteringAnalyzer()
    sample_data = [
        {'packet_size': 100, 'protocol': 6, 'src_port': 80, 'dst_port': 12345},
        {'packet_size': 200, 'protocol': 17, 'src_port': 53, 'dst_port': 54321},
        # ... más datos ...
    ]
    # Detecta anomalías en los datos de muestra.
    anomalies = analyzer.detect_anomalies(sample_data)
    print(f"Índices de paquetes anómalos: {anomalies}")
