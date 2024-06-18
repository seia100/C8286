una pregunta de examen 
  invoar procedimientos en un servidor remoto como si fuera un servidor local.

## RPC
  programar stubs -> no confundir entre stup con stub
    - representacion de codigo entre proceso de datos cliente servidor, pero del que maneja la distribucion de datos
    - manejar procedimientos remotos 
  lo que hace es abstraer
  se utiliza en sistemas distributed
  aplicado en base de datos distribuida
programacion orientada a objetos
### grpc 
variante de rpc
aplciaciones web escalables
  
## MPI
paso de mensajes entre nodos

## RMI
orientado con java
permite que los objetos ubicados en diferentes maquinas virtuales interactuen de manera transparent, lo puedes operar y ver lo que pasa dentro del sistema 
maneja invocacion de metodos
permite aplicaciones empresariales distributed

estados compartidos
hablamos also de objets

## Actor model
lo que tennemos es una abstraccion mayor
lo que hacen los actores lo que hacen es encapsular. la comunicacion es exclusiva al momento de intercambio de mensajes
explica lo que es [encapsulamiento]( https://datascientest.com/es/encapsulacion-definicion-e-importancia )
caundo necesito un alto grado de concurrencia para eventos en linea y en tiempo real.

# Algoritmos distribuidos 
1. Cordinacion 
2. Consenso

## algoritmos de consenso
pasos
raft: es mas facil implementar
  * permite mayor gestion de un lider
  * replicacion de log

permite que un conjinto de nodos 

## Algoritmos de eleccion de lider
Se necesita tener tareas centralizadas por un timepo
debe permitir el sistema de manera coordinada, incluso cuando algunos nodos fallan
* algoritmo Bully
* rings: anillo

## Algoritmos de relojes logicos
sincronizacion de eventos en sistemas distribuidos 
llamados relojes vectoriales

tengan un orden causal sin un orden causal y es necesario para la consistencia de una base de datos
y la ecuenciacion de eventos
* algoritmo de Lamport

## algoritmos de distribucion de recursos
deteccion de interbloqueos
intervenimos cuando un proceso quiere ser un destructor
aseguran para que los sistemas operen sin conflictos con una carga alta

_________________________---
SISTEMAS DISTRIBUIDOS
_________________________

comunication: 
  * Paso de mensajes: podemos usar MPI, sockets.
  * rpc: llamadas a procedimientos remotos: abstraer el proceso de comunicacion perminitiendo a un nodo como si fueran locales
    *   
  * sistemas de publicacion y suscripcion

Coordinacion:
* Implica gestionar dependencia
* orquestar diff componentes y nodos para un obj. comun
* asegura que pese a tener una operacion autonoma el sistema funcione sin problema
* protocolos de consenso
  *   paxos y raft
  *   bloqueos y semaforos
  *   contar con transacciones:
    * fallan o funcionan en consumo
 
Escalabilidad:
* Cuando un sistema ...
* particionamiento de datos: dividir datos en varios nodos
* balanceo de carga
* vertical y horizontal


Resiliencia:
* recuperarse de fallo sin interrupcion
* redundancia
* tolerancia a fallos
* failover: mecanismo de conmutacion -> cambia de manera automatica de un componente ante un fallo para asegurar un servicio continuo

las operaciones involucra el health del sistema
para ello es importante mencionar
OPERACIONES
* despliegue
* https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://www.ibm.com/mx-es/topics/middleware&ved=2ahUKEwiOxsaMu-WGAxW3CrkGHRr1BcUQFnoECBoQAw&usg=AOvVaw0ZMWWlI_PemVTTsLOnIFhd\
* 
