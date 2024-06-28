# Componentes del sistema dIDS
## Tipos de intrusiones a detectar
Los tipode itrusiones a detectar vana  ser los siguientes:
* Ataques de fuerza bruta
* Escaneo de puertos
* Inyección SQL

## Componentes principales
Dentro del sistema de componentes principales hemos condirado algugos de los cuales se han considerado importantes ya que basicamente son la estructura o la fuente de para el desarrollo completo del sistema en sí

* Configuracion del entorno de desarrollo con DOcker y Kubernetes.
* Implementar el capturador de paquetes.
* Crear un microservicoi básico para la captura y almacenamiento de datos.
* Implementar la interfaz de usuario básica.

Dentro de la carpeta de componentes es que he hecho diferentes pruebas del sistema. L acual sirvió para sacar la vejor version del sistema. Considerando que la más óptima es la que está de manera directa sin agrupar dentro de la carpta de src

Dada la nanturaleza del proyecto se ha empleado tecnicas que no requiere una configuracion mut sofisticada

## Dependencias
* For react install
  *  rechart
  *  importar el modulo components # por el momento es un tema de ver si es que es necesario un script en carpeta.

## Recomendaciones adicionales:

  * Implementar un sistema de logging para registrar eventos importantes durante la ejecución del sistema, facilitando la depuración de errores y el análisis del comportamiento del sistema.

  * Implementar un sistema de autenticación y autorización para la interfaz de usuario, restringiendo el acceso a la información sensible.

  * Utilizar un gestor de secretos para almacenar las credenciales de acceso a la base de datos MongoDB, evitando hardcodearlas en el código.

  * 
