import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import tensorflow as tf
from typing import Tuple, List
import multiprocessing as mp

class MLAnalyzer:
    def __init__(self, n_estimators: int = 100):
        """
        Constructor de la clase MLAnalyzer.
        
        :param n_estimators: Número de árboles en el bosque del modelo Random Forest.
        """
        # Inicializa el modelo Random Forest con n_estimators árboles y habilita la ejecución en paralelo.
        self.rf_model = RandomForestClassifier(n_estimators=n_estimators, n_jobs=-1)
        # Crea y configura un modelo de red neuronal.
        self.nn_model = self._create_nn_model()

    @staticmethod
    def _create_nn_model() -> tf.keras.Model:
        """
        Crea y configura un modelo de red neuronal usando TensorFlow/Keras.
        
        :return: Modelo de red neuronal configurado.
        """
        # Define una secuencia de capas para la red neuronal:
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(4,)),  # Capa con 64 neuronas y activación ReLU.
            tf.keras.layers.Dense(32, activation='relu'),  # Capa con 32 neuronas y activación ReLU.
            tf.keras.layers.Dense(1, activation='sigmoid')  # Capa de salida con activación sigmoide para clasificación binaria.
        ])
        # Compila el modelo con el optimizador Adam y la pérdida de entropía cruzada binaria.
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def train_models(self, X: np.ndarray, y: np.ndarray) -> None:
        """
        Entrena ambos modelos (Random Forest y red neuronal) en paralelo usando multiprocessing.
        
        :param X: Matriz de características de entrada.
        :param y: Vector de etiquetas objetivo.
        """
        # Divide los datos en conjuntos de entrenamiento y prueba.
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Utiliza multiprocessing para entrenar ambos modelos en paralelo.
        with mp.Pool() as pool:
            # Aplica el entrenamiento de Random Forest y red neuronal de manera asíncrona.
            rf_future = pool.apply_async(self._train_random_forest, (X_train, y_train, X_test, y_test))
            nn_future = pool.apply_async(self._train_neural_network, (X_train, y_train, X_test, y_test))
            
            # Espera a que ambos entrenamientos concluyan y obtiene los resultados.
            rf_result = rf_future.get()
            nn_result = nn_future.get()
        
        # Imprime los resultados del desempeño de cada modelo.
        print("Random Forest Performance:")
        print(rf_result)
        print("Neural Network Performance:")
        print(nn_result)

    def _train_random_forest(self, X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray) -> str:
        """
        Entrena el modelo de Random Forest y evalúa su desempeño.
        
        :param X_train: Características de entrenamiento.
        :param y_train: Etiquetas de entrenamiento.
        :param X_test: Características de prueba.
        :param y_test: Etiquetas de prueba.
        :return: Reporte de clasificación del modelo.
        """
        # Entrena el modelo Random Forest.
        self.rf_model.fit(X_train, y_train)
        # Predice las etiquetas para el conjunto de prueba.
        rf_predictions = self.rf_model.predict(X_test)
        # Devuelve el informe de clasificación.
        return classification_report(y_test, rf_predictions)

    def _train_neural_network(self, X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray) -> str:
        """
        Entrena el modelo de red neuronal y evalúa su desempeño.
        
        :param X_train: Características de entrenamiento.
        :param y_train: Etiquetas de entrenamiento.
        :param X_test: Características de prueba.
        :param y_test: Etiquetas de prueba.
        :return: Reporte de clasificación del modelo.
        """
        # Entrena el modelo con los datos de entrenamiento, usando validación cruzada y silenciando la salida (verbose=0).
        self.nn_model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.1, verbose=0)
        # Predice las etiquetas para el conjunto de prueba y binariza la salida.
        nn_predictions = (self.nn_model.predict(X_test) > 0.5).astype(int).flatten()
        # Devuelve el informe de clasificación.
        return classification_report(y_test, nn_predictions)

    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Realiza predicciones usando ambos modelos en paralelo.
        
        :param X: Matriz de características de entrada para la predicción.
        :return: Tupla con las predicciones del modelo Random Forest y de la red neuronal.
        """
        # Utiliza multiprocessing para realizar predicciones con ambos modelos en paralelo.
        with mp.Pool() as pool:
            # Aplica la predicción de manera asíncrona para cada modelo.
            rf_future = pool.apply_async(self.rf_model.predict, (X,))
            nn_future = pool.apply_async(self.nn_model.predict, (X,))
            
            # Espera a que ambas predicciones concluyan y obtiene los resultados.
            rf_pred = rf_future.get()
            nn_pred = (nn_future.get() > 0.5).astype(int).flatten()
        
        # Devuelve las predicciones de ambos modelos.
        return rf_pred, nn_pred

# Ejemplo de uso
if __name__ == "__main__":
    analyzer = MLAnalyzer()
    X = np.random.rand(1000, 4)  # Genera datos aleatorios.
    y = np.random.randint(2, size=1000)  # Genera etiquetas aleatorias binarias.
    analyzer.train_models(X, y)  # Entrena los modelos con los datos generados.
    
    X_new = np.random.rand(10, 4)  # Genera nuevos datos para predicción.
    rf_predictions, nn_predictions = analyzer.predict(X_new)  # Realiza predicciones con los nuevos datos.
    print("Random Forest predictions:", rf_predictions)
    print("Neural Network predictions:", nn_predictions)
