import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

class Dashboard extends StatefulWidget {
  @override
  _DashboardState createState() => _DashboardState();
}

class _DashboardState extends State<Dashboard> {
  List<FlSpot> packetData = [];
  List<Map<String, String>> alerts = [];
  List<Map<String, String>> recentPackets = [];

  @override
  void initState() {
    super.initState();
    // Simular la obtención de datos en tiempo real
    Timer.periodic(Duration(seconds: 1), (timer) {
      setState(() {
        // Actualizar datos de paquetes
        if (packetData.length >= 20) {
          packetData.removeAt(0);
        }
        double newValue = Random().nextDouble() * 100;
        packetData.add(FlSpot(packetData.length.toDouble(), newValue));

        // Generar alerta si es necesario
        if (newValue > 80) {
          alerts.insert(0, {
            'type': 'Alto tráfico',
            'message': 'Se detectó un alto volumen de tráfico: ${newValue.toStringAsFixed(2)} paquetes'
          });
          if (alerts.length > 5) alerts.removeLast();
        }

        // Actualizar paquetes recientes
        recentPackets.insert(0, {
          'time': DateTime.now().toIso8601String(),
          'src': '192.168.1.${Random().nextInt(255)}',
          'dst': '10.0.0.${Random().nextInt(255)}',
          'protocol': ['TCP', 'UDP', 'ICMP'][Random().nextInt(3)]
        });
        if (recentPackets.length > 5) recentPackets.removeLast();
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Dashboard de Detección de Intrusiones'),
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Gráfico de Paquetes Capturados', style: Theme.of(context).textTheme.headline6),
            SizedBox(height: 8),
            Container(
              height: 300,
              child: LineChart(
                LineChartData(
                  gridData: FlGridData(show: true),
                  titlesData: FlTitlesData(show: true),
                  borderData: FlBorderData(show: true),
                  minX: 0,
                  maxX: 19,
                  minY: 0,
                  maxY: 100,
                  lineBarsData: [
                    LineChartBarData(
                      spots: packetData,
                      isCurved: true,
                      color: Colors.blue,
                      barWidth: 2,
                      isStrokeCapRound: true,
                      dotData: FlDotData(show: false),
                      belowBarData: BarAreaData(show: false),
                    ),
                  ],
                ),
              ),
            ),
            SizedBox(height: 16),
            Text('Alertas Recientes', style: Theme.of(context).textTheme.headline6),
            SizedBox(height: 8),
            Column(
              children: alerts.map((alert) => Card(
                child: ListTile(
                  title: Text(alert['type']!),
                  subtitle: Text(alert['message']!),
                ),
              )).toList(),
            ),
            SizedBox(height: 16),
            Text('Paquetes Recientes', style: Theme.of(context).textTheme.headline6),
            SizedBox(height: 8),
            Table(
              border: TableBorder.all(),
              children: [
                TableRow(
                  children: ['Tiempo', 'Origen', 'Destino', 'Protocolo']
                    .map((header) => TableCell(
                      child: Padding(
                        padding: EdgeInsets.all(8.0),
                        child: Text(header, style: TextStyle(fontWeight: FontWeight.bold)),
                      ),
                    )).toList(),
                ),
                ...recentPackets.map((packet) => TableRow(
                  children: [packet['time']!, packet['src']!, packet['dst']!, packet['protocol']!]
                    .map((cell) => TableCell(
                      child: Padding(
                        padding: EdgeInsets.all(8.0),
                        child: Text(cell),
                      ),
                    )).toList(),
                )).toList(),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
