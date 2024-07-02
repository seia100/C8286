import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from dask import dataframe as dd
from dask.distributed import Client
from mpi4py import MPI

class DistributedAnalyzer:
    """
    Clase para analizar datos distribuidos utilizando KMeans y escalado de características,
    aprovechando MPI para la paralelización.
    """

    def __init__(self, n_clusters=5):
        """
        Inicializa el analizador distribuido con un número específico de clusters para KMeans.
        """
        self.comm = MPI.COMM_WORLD  # Inicializa la comunicación MPI.
        self.rank = self.comm.Get_rank()  # Obtiene el rango del proceso actual.
        self.size = self.comm.Get_size()  # Obtiene el número total de procesos.

        self.n_clusters = n_clusters
        self.scaler = StandardScaler()
        self.kmeans = None  # El modelo KMeans se ajustará después de la distribución de datos.
        self.client = Client()  # Inicializa un cliente Dask para manejo distribuido de tareas.

    def preprocess_data(self, data):
        """
        Preprocesa los datos escalando características de forma distribuida.
        """
        # Convertir el DataFrame de pandas a un Dask DataFrame para procesamiento distribuido.
        ddf = dd.from_pandas(data, npartitions=self.client.ncores())
        # Escalar los datos utilizando Dask de forma distribuida.
        scaled_data = self.client.submit(self.scaler.fit_transform, ddf).result()
        return scaled_data

    def fit(self, data):
        """
        Ajusta el modelo K-means a los datos preprocesados de forma distribuida.
        """
        # Dividir los datos entre los procesos.
        data_chunk = np.array_split(data, self.size)[self.rank]

        # Preprocesar el fragmento de datos local.
        preprocessed_chunk = self.preprocess_data(data_chunk)

        # Ajustar un modelo KMeans local a los datos preprocesados.
        local_kmeans = KMeans(n_clusters=self.n_clusters)
        local_kmeans.fit(preprocessed_chunk)

        # Reunir los centroides locales de todos los procesos.
        all_centroids = self.comm.gather(local_kmeans.cluster_centers_, root=0)

        # El proceso 0 promedia los centroides para obtener un modelo global.
        if self.rank == 0:
            global_centroids = np.mean(np.concatenate(all_centroids), axis=0)
            self.kmeans = KMeans(n_clusters=self.n_clusters, init=global_centroids, n_init=1)
            self.kmeans.fit(self.preprocess_data(data))  # Ajustar el modelo global a todos los datos.

        # Transmitir el modelo KMeans global a todos los procesos.
        self.kmeans = self.comm.bcast(self.kmeans, root=0)

    def predict(self, data):
        """
        Realiza predicciones sobre los datos usando el modelo K-means entrenado.
        """
        preprocessed_data = self.preprocess_data(data)
        # Realizar predicciones de forma distribuida.
        predictions = self.client.submit(self.kmeans.predict, preprocessed_data).result()
        return predictions

    def analyze_anomalies(self, data, threshold=2.0):
        """
        Analiza y detecta anomalías en los datos basándose en las distancias al centro del cluster más cercano.
        """
        predictions = self.predict(data)
        distances = self.kmeans.transform(self.preprocess_data(data))
        # Calcular los scores de anomalía como la distancia mínima a los centros de cluster.
        anomaly_scores = np.min(distances, axis=1)
        # Determinar qué entradas son consideradas anomalías basadas en un umbral.
        anomalies = anomaly_scores > threshold
        return anomalies, anomaly_scores

# Uso del analizador
if __name__ == "__main__":
    # Ejemplo de uso con datos aleatorios.
    import pandas as pd
    data = pd.DataFrame(np.random.rand(10000, 5))  # Generar datos aleatorios.

    analyzer = DistributedAnalyzer()
    analyzer.fit(data)  # Ajustar el modelo a los datos.
    anomalies, scores = analyzer.analyze_anomalies(data)  # Analizar las anomalías.
    print(f"Anomalías detectadas: {sum(anomalies)}")  # Imprimir el número de anomalías detectadas.