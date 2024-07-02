import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

class OptimizedDetector:
    """
    Clase para detectar anomalías utilizando RandomForest y KMeans optimizados en paralelo.
    """
    def __init__(self, n_estimators=100, n_clusters=5):
        """
        Inicializa los modelos y el escalador, junto con un pool de procesos para la ejecución paralela.
        """
        self.rf_model = RandomForestClassifier(n_estimators=n_estimators, n_jobs=-1)  # Modelo RandomForest
        self.kmeans_model = KMeans(n_clusters=n_clusters, n_init=10)  # Modelo KMeans
        self.scaler = StandardScaler()  # Escalador para normalización
        self.executor = ProcessPoolExecutor(max_workers=multiprocessing.cpu_count())  # Executor para paralelismo

    def fit(self, X, y):
        """
        Entrena los modelos RandomForest y KMeans en paralelo.
        """
        # Envía las tareas de entrenamiento a los procesadores en paralelo
        rf_future = self.executor.submit(self._fit_random_forest, X, y)
        kmeans_future = self.executor.submit(self._fit_kmeans, X)
        
        # Espera a que las tareas finalicen y actualiza los modelos con los resultados
        self.rf_model = rf_future.result()
        self.kmeans_model = kmeans_future.result()

    def _fit_random_forest(self, X, y):
        """
        Entrena el modelo RandomForest.
        """
        return self.rf_model.fit(X, y)

    def _fit_kmeans(self, X):
        """
        Escala los datos y entrena el modelo KMeans.
        """
        X_scaled = self.scaler.fit_transform(X)
        return self.kmeans_model.fit(X_scaled)

    def predict(self, X):
        """
        Predice si los datos son anomalías utilizando ambos modelos en paralelo.
        """
        # Realiza predicciones en paralelo
        rf_future = self.executor.submit(self.rf_model.predict, X)
        kmeans_future = self.executor.submit(self._predict_kmeans, X)
        
        # Recupera los resultados
        rf_predictions = rf_future.result()
        kmeans_predictions = kmeans_future.result()
        return np.logical_and(rf_predictions, kmeans_predictions)  # Combina las predicciones

    def _predict_kmeans(self, X):
        """
        Predice utilizando KMeans para determinar distancias y umbralizar.
        """
        X_scaled = self.scaler.transform(X)
        distances = self.kmeans_model.transform(X_scaled)
        threshold = np.percentile(distances.min(axis=1), 95)
        return distances.min(axis=1) > threshold

    def optimize_hyperparameters(self, X, y):
        """
        Optimiza los hiperparámetros para RandomForest y KMeans en paralelo.
        """
        # Envía las tareas de optimización a los procesadores en paralelo
        rf_future = self.executor.submit(self._optimize_rf_estimators, X, y)
        kmeans_future = self.executor.submit(self._optimize_kmeans_clusters, X)

        # Recupera los mejores parámetros
        best_n_estimators = rf_future.result()
        best_n_clusters = kmeans_future.result()

        # Reconfigura los modelos con los mejores parámetros encontrados y vuelve a entrenar
        self.rf_model = RandomForestClassifier(n_estimators=best_n_estimators, n_jobs=-1)
        self.kmeans_model = KMeans(n_clusters=best_n_clusters, n_init=10)
        self.fit(X, y)

    def _optimize_rf_estimators(self, X, y):
        """
        Busca el mejor número de estimadores para RandomForest mediante validación cruzada.
        """
        scores = []
        for n in range(50, 200, 50):
            model = RandomForestClassifier(n_estimators=n, n_jobs=-1)
            score = np.mean(cross_val_score(model, X, y, cv=3))
            scores.append((n, score))
        return max(scores, key=lambda x: x[1])[0]

    def _optimize_kmeans_clusters(self, X):
        """
        Busca el mejor número de clusters para KMeans utilizando el método del codo.
        """
        X_scaled = self.scaler.fit_transform(X)
        scores = []
        for k in range(2, 10):
            model = KMeans(n_clusters=k, n_init=10)
            score = -model.fit(X_scaled).inertia_  # Inertia negativa para maximizar
            scores.append((k, score))
        return max(scores, key=lambda x: x[1])[0]

# Uso del detector
if __name__ == "__main__":
    X = np.random.rand(1000, 10)
    y = np.random.randint(2, size=1000)

    detector = OptimizedDetector()
    detector.optimize_hyperparameters(X, y)
    detector.fit(X, y)
    predictions = detector.predict(X)
    print(f"Anomalías detectadas: {sum(predictions)}")
