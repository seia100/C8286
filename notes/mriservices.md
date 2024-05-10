# Microservicios

Vemos directamenete la **arquitectura, APIs(interfaces) y servicios independietes.
ademas se enlaza con conceptos CI/CD
  pipline ciandia de datos.
  hay una opcion de nube

La arquitectura de microservicios se basa en
* modularidad: un microservicio es un modulo que hace una funcion especifica en un entorno.
* Aislamiento: los servicios operan de manera independiente. Permite que diferentes equipos trabajan sin interferir al sistema
* independencia: En terminos de operacion y desarrollo -> Usar diferentes lenguajes y storage siempre y cuando se cumpla con actividades requeridas.
  * ediciones de diseno que podemos trabajar una base de datos o herramientos de enfoque algoritmico.
  *    
* descentralizacion: falta
* evolucion continua: falta

* 
## Ventaja
* despliegue continuo
* relacionados con CI/CD
  * reduce el riego
 
* Latencia y los sistemas distribuidos


Necesitamos un sistema de orquestacion, monitoreo y mas y seguridad
Cada vector de comunicacion es un tema de ver para el tema de seguridad

tambien es un reto cuando hablamos de que es mas costoso
por lo que es importante mencionar el tema de docker, kubernets, microservices

## docker file  que es y como implementear
Este es una pregunta de examen

Tener en cuenta la lectura de sistemas operativos.

cada servicio puede estar contenerizado y aislado de manera individual.

### kubernets
  gestionar contenedores
  gestionar servicios
  pods: unidad mas basica

kubernees usa el objeto de servicio para proporcionar una direccion ip y un DNS para un conjunto de pods, por lo que permite conexion de microservicios? true.

servicios:
Los servicios no permiten que los microservicios se descubra en un sistema y permitan operar de manera confiable? falso

balanceo de carga: kubernets ofrece capacidades que permite balanceo de carga y tambien de manera automatica entrante enntre los pods de un servicio? verdadero
* lo que mejoraria es la disponibilidad y la persistencia de las aplicaciones

Autoescalado:
kubernet puede ajustar automaticamente los pods en funcion de la carga de trabajo actual? true

= entonces eso no permite una gestion de adaptacion eficiente de los recursos (true) por lo que puede ayudar a gestionar mejores opciones de adaptebilidad.

Kubernets: permite ver la infraestructura de microservicios. este es un helm -> podemos lanzar y gestionar miroservicios en linux.

soporta:
Namespace: segmentacion de clusters en subgrupos. permite ailamiento y  solicitu d de permisos par que una aplicacion...

es importante ver el tema de elstic stack

kubernet y docker se combian y sirve para poder desarrollar y escalar.

es importante conocer el [catalogo de patrones de diseno](https://refactoring.guru/es/design-patterns/catalog)


Asocia con la batalla de helm el paquete de helm para kubernets
https://tolkiendili.com/wiki/Batalla_del_Abismo_de_Helm
https://helm.sh/

patrones de diseno 
patrones estructurales, creacionales, comportamiento

## patrones diseno de microservicios
* patrones de comunicacion
  * Sincrono: hablamos de REST (impone condiciones sobre cómo debe funcionar una API), gpc 
  * asincrono: hablamos de mensajeria con colas, rabbit MQ, kafka 
## Patrones de resiliencia. 
importante para tolerar fallor y pueda operar en fallos

  * circuit break
  * back off (examn final)
  * bulkhead
