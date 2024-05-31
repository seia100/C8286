# Resumen de Memoria Compartida Distribuida

## Conceptos Clave

1. **Coherencia de Caché**:
   - **Protocolo MESI**: Explica cómo se mantiene la coherencia en sistemas de memoria compartida.
   - **Estados MESI**: Modificado, Exclusivo, Compartido, Inválido.
   - **Transiciones de Estado**:
     - Cuando un procesador lee una línea de caché por primera vez.
     - Cuando un segundo procesador lee la misma línea de caché.
     - Cuando un procesador modifica la línea de caché.
     - Cuando un segundo procesador intenta leer la línea de caché modificada.

2. **Implementación Práctica**:
   - Uso de **POSIX threads (pthread)** y **mutexes** para proteger una variable compartida.
   - Ejemplo de un programa que incrementa de manera segura una variable global compartida mediante múltiples hilos.

3. **Optimización de Algoritmos para Memoria Compartida**:
   - **Localización de Datos**: Agrupar en memoria los datos frecuentemente accedidos para aprovechar la caché.
   - **Reducción de Contención**: Utilizar estructuras de datos concurrentes y particionar tareas para minimizar el acceso simultáneo.
   - **Minimización de la Latencia de Caché**: Acceder a los datos siguiendo patrones que maximicen la eficiencia de la caché y evitar el "cache thrashing".

## Ejercicios Propuestos

1. Describir detalladamente el funcionamiento del protocolo MESI con ejemplos de transiciones de estados.
2. Programar en C usando pthreads y mutexes para demostrar la protección de una variable compartida.
3. Discutir estrategias para optimizar algoritmos en sistemas de memoria compartida, incluyendo técnicas para mejorar el rendimiento y reducir la latencia.
