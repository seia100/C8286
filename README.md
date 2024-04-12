# C8286
prácticas de código relacionados al curso parallel and  distributed  computing


Indice de la semana 4

# Docker:
esd dep codigo abierto para lanzar apps usando CONTENEDORES DE SOFTWARE
mas partes de codigo librerias y mas 
docker esta relacionado con la virtualizacion 

la idea de docker  en una imagen 

una maquina virtual es lo que hace es emilar y lo hace con una arquitectueta computadores y proporciona propoedad des fisicas

VM
- arquitectura de computadoras y funciones de computadora
- haciendo aislamiento de ina  imagen viartual separado
- Podemos el aislamiento completo de las imagenes

- la maquina virtual emulaa para poder ejecutar en toda cla computadora y eso lo que hacecon el hipervisor

* el aisalamiento en docker es a nivel de procesos del sistema operativo host

* dokcer engine en linux es para ESPACIOS DE NOMBRES
* a nivel de aislamiento es menos seguro
* el problema de ejecucion de sofrware y debemos tomar el control del sistema operativo y como instalar las cosas


al momento 

docker engine esta formado por
- demonio
- client
- api rest docker


instalar docker es instalar todos los componentes para comunicar todo el time como un servicio

una contendor tiene un estado y lo podemos moficar _Stateful_ 

palabras clave
- name spaces
- grupos de control: son los que nos ayudan en un contenedor no tenga el sindrome del vecino ruidoso. Que un contenedor no se coma todos los recursos disponibles del docker host. como controlar ram, etc.
- capacidad de las capas


espacio de nombres del ID del proceso 

stratificacion o _layering_ puede optimizar mas lo demas :)

si podemos contralar en la primera capa poemos hacer un mejor manejo de las primitivas que nos brinda  linux

run: es la funcionalidad de bajo nivel del tiempo de ejecucion/ encargado del tiempo de vida del contenedor

container: se basa en run y se enarga en la administracion de imagenes, tambien tiene capacidad de redes. son de codigo abierto ambos.

docker engine: proporciona funcionalidades.
_________________________
interfaz de REST
  es importante porque me permite automatizar todas las operaciones de contenedores. y es por eso es importante.
  la interfaz de la linea de comandos de docker e.
