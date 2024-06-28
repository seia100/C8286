from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np

class DistributedAnalysis:
    def __init__(self):
        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=3)  # Asumimos 3 clusters para este ejemplo

    def preprocess_data(self, data):
        # Convertir datos a formato numérico y escalar
        numeric_data = np.array([[len(d['payload']), d['duration']] for d in data])
        return self.scaler.fit_transform(numeric_data)

    def analyze(self, data):
        preprocessed_data = self.preprocess_data(data)
        clusters = self.kmeans.fit_predict(preprocessed_data)
        
        # Identificar cluster anómalo (por ejemplo, el más pequeño)
        anomalous_cluster = np.argmin(np.bincount(clusters))
        
        anomalies = [
            data[i] for i, cluster in enumerate(clusters) if cluster == anomalous_cluster
        ]
        
        return anomalies

# Uso del microservicio
analysis_service = DistributedAnalysis()
sample_data = [
    {"payload": "GET /admin", "duration": 0.5},
    {"payload": "POST /login", "duration": 0.2},
    # ... más datos ...
]
anomalies = analysis_service.analyze(sample_data)
print(f"Anomalías detectadas: {anomalies}")
