# test_analysis.py
import unittest
import numpy as np
from src.analysis.clustering import ClusteringAnalyzer  # Importa la clase ClusteringAnalyzer
from src.analysis.ml_analyzer import MLAnalyzer  # Importa la clase MLAnalyzer

class TestAnalysis(unittest.TestCase):
    """
    Suite de pruebas para evaluar los analizadores de clustering y machine learning.
    """

    def setUp(self):
        """
        Método que se ejecuta antes de cada prueba para configurar los analizadores.
        """
        # Inicializa un analizador de clustering
        self.clustering_analyzer = ClusteringAnalyzer()
        # Inicializa un analizador de machine learning
        self.ml_analyzer = MLAnalyzer()

    def test_clustering_analyzer(self):
        """
        Prueba la detección de anomalías en datos de prueba usando ClusteringAnalyzer.
        """
        # Datos de muestra que incluyen una posible anomalía
        sample_data = [
            {'packet_size': 100, 'protocol': 6, 'src_port': 80, 'dst_port': 12345},
            {'packet_size': 200, 'protocol': 17, 'src_port': 53, 'dst_port': 54321},
            {'packet_size': 1000, 'protocol': 6, 'src_port': 22, 'dst_port': 65000},  # Anomalía
        ]
        # Detectar anomalías en los datos de muestra
        anomalies = self.clustering_analyzer.detect_anomalies(sample_data)
        # Verificar que se detecta exactamente una anomalía
        self.assertEqual(len(anomalies), 1)
        # Verificar que el índice de la anomalía detectada es 2
        self.assertEqual(anomalies[0], 2)

    def test_ml_analyzer(self):
        """
        Prueba el entrenamiento y la predicción utilizando MLAnalyzer.
        """
        # Genera datos aleatorios de características y etiquetas para el entrenamiento
        X = np.random.rand(100, 4)
        y = np.random.randint(2, size=100)
        # Entrena los modelos con los datos generados
        self.ml_analyzer.train_models(X, y)
        
        # Genera nuevos datos de prueba para la predicción
        X_new = np.random.rand(10, 4)
        # Realiza predicciones utilizando los modelos entrenados
        rf_predictions, nn_predictions = self.ml_analyzer.predict(X_new)
        
        # Verifica que las predicciones tienen el tamaño correcto
        self.assertEqual(len(rf_predictions), 10)
        self.assertEqual(len(nn_predictions), 10)
        # Verifica que todas las predicciones son binarias (0 o 1)
        self.assertTrue(all(pred in [0, 1] for pred in rf_predictions))
        self.assertTrue(all(pred in [0, 1] for pred in nn_predictions))

if __name__ == '__main__':
    unittest.main()  # Ejecuta todas las pruebas
