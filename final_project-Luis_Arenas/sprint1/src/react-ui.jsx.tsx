import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { Alert, AlertTitle } from '@/components/ui/alert';
import { Table } from '@/components/ui/table';

const Dashboard = () => {
  // Estados para almacenar los datos del dashboard
  const [packetData, setPacketData] = useState([]); // Datos para el gráfico de paquetes
  const [alerts, setAlerts] = useState([]); // Alertas generadas
  const [recentPackets, setRecentPackets] = useState([]); // Paquetes recientes

  useEffect(() => {
    // Función para simular la obtención de datos en tiempo real
    const fetchData = () => {
      // *** SECCIÓN PARA INTEGRAR CON EL BACKEND ***
      // -----------------------------------------------
      // Aquí deberías reemplazar esta lógica de simulación 
      // por una llamada a tu API o servicio backend para obtener:
      //   - Nuevos paquetes de red
      //   - Alertas generadas por el sistema de detección de intrusiones
      // -----------------------------------------------

      // Simulación de un nuevo paquete
      const newPacket = {
        time: new Date().toISOString(),
        count: Math.floor(Math.random() * 100)
      };

      // Actualiza el estado 'packetData' con el nuevo paquete
      setPacketData(prevData => [...prevData.slice(-19), newPacket]);

      // Simulación de una alerta si el conteo de paquetes es alto
      if (newPacket.count > 80) {
        setAlerts(prevAlerts => [...prevAlerts, {
          type: 'Alto tráfico',
          message: `Se detectó un alto volumen de tráfico: ${newPacket.count} paquetes`
        }]);
      }

      // Actualiza el estado 'recentPackets' con datos simulados
      setRecentPackets(prevPackets => [{
        time: newPacket.time,
        src: '192.168.1.' + Math.floor(Math.random() * 255),
        dst: '10.0.0.' + Math.floor(Math.random() * 255),
        protocol: ['TCP', 'UDP', 'ICMP'][Math.floor(Math.random() * 3)]
      }, ...prevPackets.slice(0, 4)]);
    };

    // Ejecuta 'fetchData' cada segundo para simular la actualización en tiempo real
    const interval = setInterval(fetchData, 1000);

    // Limpia el intervalo cuando el componente se desmonta
    return () => clearInterval(interval);
  }, []); // El array vacío indica que el efecto se ejecuta solo una vez al montar el componente

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Dashboard de Detección de Intrusiones</h1>

      {/* Gráfico de paquetes capturados */}
      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-2">Gráfico de Paquetes Capturados</h2>
        <LineChart width={600} height={300} data={packetData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="count" stroke="#8884d8" />
        </LineChart>
      </div>

      {/* Sección de alertas */}
      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-2">Alertas Recientes</h2>
        {alerts.map((alert, index) => (
          <Alert key={index} className="mb-2">
            <AlertTitle>{alert.type}</AlertTitle>
            {alert.message}
          </Alert>
        ))}
      </div>

      {/* Tabla de paquetes recientes */}
      <div>
        <h2 className="text-xl font-semibold mb-2">Paquetes Recientes</h2>
        <Table>
          <thead>
            <tr>
              <th>Tiempo</th>
              <th>Origen</th>
              <th>Destino</th>
              <th>Protocolo</th>
            </tr>
          </thead>
          <tbody>
            {recentPackets.map((packet, index) => (
              <tr key={index}>
                <td>{packet.time}</td>
                <td>{packet.src}</td>
                <td>{packet.dst}</td>
                <td>{packet.protocol}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      </div>
    </div>
  );
};

export default Dashboard;