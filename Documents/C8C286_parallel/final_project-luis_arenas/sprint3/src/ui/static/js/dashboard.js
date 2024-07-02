// Este evento asegura que el código solo se ejecutará una vez que el DOM esté completamente cargado.
document.addEventListener('DOMContentLoaded', function() {
    // Función para actualizar las estadísticas de tráfico en la página.
    function updateStats() {
        // Realiza una solicitud GET a '/api/stats' para obtener estadísticas actualizadas.
        fetch('/api/stats')
            .then(response => response.json())  // Convierte la respuesta en JSON.
            .then(data => {
                // Actualiza el contenido de los elementos HTML con los nuevos valores.
                document.getElementById('total-packets').textContent = data.total_packets;
                document.getElementById('anomalies-detected').textContent = data.anomalies;
            });
    }

    // Función para crear un gráfico de tráfico en la página.
    function createTrafficChart() {
        // Realiza una solicitud GET a '/api/traffic_data' para obtener datos para el gráfico.
        fetch('/api/traffic_data')
            .then(response => response.json())  // Convierte la respuesta en JSON.
            .then(data => {
                // Prepara un contexto de canvas 2D donde se dibujará el gráfico.
                const ctx = document.getElementById('traffic-chart').getContext('2d');
                // Crea un nuevo gráfico de tipo línea en el contexto del canvas.
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: data.labels,  // Etiquetas del eje X (generalmente representan el tiempo).
                        datasets: [{
                            label: 'Network Traffic',  // Título de los datos del gráfico.
                            data: data.values,  // Valores de los datos para el gráfico.
                            borderColor: 'rgb(75, 192, 192)',  // Color de la línea del gráfico.
                            tension: 0.1  // Suavidad de la línea.
                        }]
                    },
                    options: {
                        responsive: true,  // Hace que el gráfico sea responsivo.
                        scales: {
                            y: {
                                beginAtZero: true  // Comienza el eje Y desde cero.
                            }
                        }
                    }
                });
            });
    }

    // Llama a las funciones de actualizar estadísticas y crear el gráfico cuando la página se carga.
    updateStats();
    createTrafficChart();

    // Establece un intervalo para actualizar las estadísticas cada 30 segundos.
    setInterval(updateStats, 30000);
});
