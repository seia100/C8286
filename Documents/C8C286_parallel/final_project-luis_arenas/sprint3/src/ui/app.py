from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
import threading
import time
from src.detection.optimized_detector import OptimizedDetector
from src.analysis.distributed_analyzer import DistributedAnalyzer

app = Flask(__name__)
socketio = SocketIO(app)

detector = OptimizedDetector()
analyzer = DistributedAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/alerts')
def alerts():
    return render_template('alerts.html')

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    # Implementar lógica para obtener alertas de la base de datos
    alerts = [
        {"id": 1, "type": "Intrusion Attempt", "source_ip": "192.168.1.100", "timestamp": "2024-07-02 15:30:00"},
        {"id": 2, "type": "Malware Detected", "source_ip": "10.0.0.5", "timestamp": "2024-07-02 15:35:00"}
    ]
    return jsonify(alerts)

def background_analyzer():
    while True:
        # Simular análisis continuo
        time.sleep(5)
        anomalies = detector.predict(analyzer.preprocess_data(get_new_data()))
        if any(anomalies):
            socketio.emit('new_alert', {'message': 'Nueva anomalía detectada!'})

@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')

if __name__ == '__main__':
    threading.Thread(target=background_analyzer, daemon=True).start()
    socketio.run(app, debug=True)