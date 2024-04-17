# Construyendo una simple app con contenedor de Docker
##### Objetivos
Parte 1: Crear un script Bash simple

Parte 2: Crear una aplicación web simple

Parte 3: Configurar la aplicación web para utilizar archivos de sitio web

Parte 4: Crear un script de Bash para compilar y ejecutar un contenedor Docker

Parte 5: Construir, ejecutar y verificar el contenedor Docker

*tener en cuenta que los archivos python o ejecutables estaran presentes en la carpeta `assets` de la actividad.

### Resultado final:
// Enter the final result.

## Part1: Crear un scrip simple
En caso que no hayas creado tu entorno y demas quiero es importante que crees la carpeta requerida puedes usar `mkdir` para crear el nuevo o nuevos directorios. Abrimos el directorio creado y creamos un archivo `user-input.sh`
```
touch user-input.sh
```
Podemos usar nano o visual studio u otro entorno de desarrollo para modificar el archivo recien crado. Hay que acostumbrarse a usar nano o vim 
```
nano user-input.sh
```

Agregamos la 'she-bang' `#! /bin/bash`

Abregamos simples comandos:
``` bash
echo -n "Introduzca su nombre: "
read userName
echo "Tu nombre es $userName."
```
Guardamos el archivo, si es en `nano` usa CTRL + X. Luego la `Y` para confirmar cambios
Ejecutamos el archivo en desde la linea de comando.
```
bash user-input.sh
```
Cambiar el modo del script a un archivo ejecutable para todos los usuarios.
```
ls -l user-input.sh
## output: (va a depender de tu  consulta, puede variar.
## -rw-rw-r— 1 devasc devasc 84 Jun 7 16:43 user-input.sh

## damos permisos de ejecucion
chmod a+x user-input.sh

## revisamos que se haya modificado los permisos (fijate la x) 
ls -l user-input.sh
## output -rwxrwxr-x 1 devasc devasc 84 Jun 7 16:43 user-input.sh
```
Cambiar el nombre del archivo para eliminar la extensión .sh
```
mv user-input.sh user-input
```
Ejecutar el script desde la línea de comandos.
```
./user-input

```

## Part2 : Crear una aplicación web simple
Instalar Flask y abrir un puerto


// tener en cuenta que en este caso es necesario trabajar en entornos virtuales. Para crear un entorno virtual: ubicate en la carpeta de tu preferencia y ejecutas ``python3 -m venv $[nombre de tu preferencia al entorno]``
por ejemplo en mi caso

```
python3 -m venv acts
```
acts es el nombre de mi entorno y antes que te lances con todo es necesario que se active el entorno 
```
source acts/bin/activate
```

y algo que puedes caracterizar es por cuando sale el nombre a un costadito :D en caso que no funcine te recomiendo la documentacion de [python](https://docs.python.org/3/library/venv.html) o [venv](https://python.land/virtual-environments/virtualenv). De todas maneras si no te sirven estos enlaces no te limites :)

Una vez activado tu entorno virtual instalamos `flask`
```
pip3 install flask
```
Cremaos nuesta app sencilla y es por ello que creamos el archivo sample_app.py
``` python3
from flask import Flask
from flask import request

#Crear una instancia de la clase Flask.
sample = Flask(__name__)

# A continuación, configure Flask para que cuando un usuario
# visite la página predeterminada (directorio raíz),
# muestre un mensaje con la dirección IP del cliente.
@sample .route ("/")
def main():
  return 'Me estas llamando desde ' + request.remote_addr + '\n'

'''
Observe la instrucción @sample .route ("/") Flask. Los frameworks como Flask usan una técnica de
enrutamiento (routing) (. route) para referirse a una URL de aplicación (esto no debe confundirse con
el enrutamiento de red). Aquí el "/" (directorio raíz) está enlazado a la función main (). Por lo tanto,
cuando el usuario va a http://localhost:8080/ (directorio raíz) URL, la salida de la declaración de
retorno se mostrará en el navegador.
'''

# Configurar la aplicación para que se ejecute localmente.
if __name__=='__main__':
  sample.run(host='0.0.0.0', port=8080)
```

guardamos y ejecuatamos la app web de ejemplo
```bash 
python3 sample_app.py
```
el ouptput deberia de ser:
```shell 
* Serving Flask app "sample app" (lazy loading)
* Environment: production
ADVERTENCIA: Este es un servidor de desarrollo. No lo utilice en una
implementación de producción.
Utilice un servidor WSGI de producción en su lugar.
*Modo de depuración: apagado
* Ejecutando en http://0.0.0.0:8080/ (Presione CTRL+C para salir)
```
Comprobar que el servidor se está ejecutando.
Puede verificar que el servidor se está ejecutando de dos maneras.
1. Abra el navegador web Chromium e introduzca 0.0.0.0:8080 en el campo URL. Debería
obtener la siguiente salida:
Me estás llamando desde 127.0.0.1
Si recibe una respuesta de "HTTP 400 Bad Request", compruebe cuidadosamente su script
sample_app.py.
2. Abrir otra ventana de terminal y utilice la herramienta URL de línea de comandos (cURL)
para verificar la respuesta del servidor
```
curl http://0.0.0.0:8080
```
para detener el servidor o intancia ejecutada press `CTRL + C`

## Parte 3: Configurar la aplicación web para utilizar archivos de sitio web

* epxlorar los directorios que utilizara la aplicacion web
para ello tener en cuenta que debemos crear los directorios dentro de `app-web` tanto `static ` y el dorectorio `templates` en los que van a crearse los archivos `style.css` e `index.html` respectivamente.
  * Editamos ambos archivos. El siguiente codigo corresponde a `index.html`
  * ```html
    <html>
    <head>
      <title>Sample aplication</title>
    <link rel="stylesheet" href="/static/style.css"/>
    </head>
      <body>
        <h1>Calling me from: {{request.remore_addr}}</h1>
      </body>
    </html>
    ```
 *  Codigo para el archivo `style.css`
 *   ```css
     body {background: darksteelblue;}
     ```


* Actualizar el cod python para la apliacion web de muestra
  actualizamos el archivo `sample_app.py`de modo que nos reenderice el archivo `index.html`

  El archivo HTML se puede reenderizar automaticamente en Flask usando la funcion reder_template es por ello que vamos a editar `sample_app.py`
  ```python
  from flask import Flask, request, render_template

  sample = Flask (__name__)

  @sample .route("/")
  def main():
  return render_template ("index.html",request=request)

  if __name__ == "__main__":
    sample.run (host="0.0.0.0", port=8080)
  ```

🗒️ **NOTE:** No olvides de guardar cambios
ejecutamos el script no olvides de activar tu entorno virtual en python para que no haya errores :)

Si obtienes el siguiente resultado, **genial hemos progresado**
![execute-program](https://github.com/seia100/C8286/blob/main/sol-eva/eva3/run_server.png)

He hecho muchas consultas, considero que es la carga que le damos al servidor. Por lo que seria necesario un balanceador de carga o no se el por que cuando ejeccuto `curl 0.0.0.0:8080` no me sale nada relacionado al respecto. Por lo que asumo eso. Comprobe en el _browser_ y se queda cargando. Es por ello que llegue a tal conclusion :)

## Parte 4: Crear un script de Bash para compilar y ejecutar un contenedor Docker
1. Crear directorios temporales para almacenar los archivos del sitio web.
  ```bash
   #!/bin/bash
   
   # Creamos directorios de manera recursiva con el parametro -p
   mkdir -p tempdir/templates/static
  ```

   
  
2. Copiar los  directorios del sitio web y sample_app.py en el directorio temporal.
  ```
  cp sample_app.py tempdir/.
  cp -r templates/. tempdir/templates/.
  cp -r static/* tempdor/static/.
  ```
* Tener en cuenta que todo es en el mismo archivo.
* es un archivo sh repetimos los pasos anteirores para poder ejecutarlo.

Si te preguntas por mi codigo, tranqui ahora lo ubico

```bash
#! /bin/bash

# esto se tiene que ejecutar en el directorio app-web de 
# lo contrario no lo va a identificar los directorios a copiar :)

: '
echo -n "Enter your name: "
read userName
echo "Your name is aise"
'

# la siguiente linea la voy comentar porque algunos directorios ya fueron creados
## mkdir -p tempdir/templates/static

# es por ello que usaremos estructuras de control
if [ ! -d "tempdir/templates"]; then
    mkdir -p tempdir/templates
fi

if [ ! -d "tempdir/static"]; then 
    mkdir -p tempdir/static 

fi 

# copiamos los directorios del sitio web y sample_app.py 
# en el directorio temporal `tempdir`

#en este caso el argumento _n_ es para evitar sobreescribir files que ya fueron copiados
cp -n sample_app.py tempdir/ .
cp -rn templates/* tempdir/templates/.
cp -rn static/* tempdir/static/. 



```
Pueda que te salte algunos errores tener en cuenta y por que se ve asi. Resulta que hubo un typo y mi idea no era sobreescribir archivos y continuar con lo que copias. No se si me dejo entender. El punto es que lo ejecute el cod de la guia y como estaba mal se interrumpio "copiar"

El resultado te debe quedar de la siguiente manera:
![cp_mkdir](https://github.com/seia100/C8286/blob/main/sol-eva/eva3/mkdir_cp.png)

________________________________________________
* **IMPORTANT**
  *   Command Explanation
    * The cp command in Linux is used to copy files and directories. The following options can be particularly useful:
      * `-n, --no-clobber`: This option will prevent cp from overwriting existing files. If a file already exists in the destination directory, it won't be overwritten, and cp will simply skip the copy operation for that file.
      * ` -u, --update`: With this option, cp will only copy a file if it either doesn't exist at the destination or if the source file is newer than the destination file. This can be useful if you're repeatedly copying files and always want to ensure you have the most recent versions.

_________________________________________________


 
3. Crear un archivoo docker (Dockerfile)
   a. Necesita que python se ejecute en el contenedor, asi que agregue el comando Docker `FROM` para instalar Python en el contenedor.
    ```bash
    echo "FROM python" >> tempdir/Dockerfile
    ```
    
  b. su script `sample_app.py` necesita Flask, por lo que agregamos el comando Docker para instalar Flask en el contenedor.
    ```bash
    echo "RUN pip install flask" >> tempdir/Dockerfile
    ```
  c. El contendedor necesitara las carpetas del sitio web y el script `sample_app.py` oara ejecutar la aplicacion, asi que agregale los comandos de Docker **COPY** para agregarlos a un directorio en el contenedor DOcker. En este ejemplo creara `/home/myapp` como directorio principal dentro del contenedor Docker. Ademas de copiar el archivo *sample_app.py* al archivo Dockerfile, tammbien cipuara el archivo *index.html* del dorectorio de plantillas u el archivo *style del directorio *static*

  
  FALTA STEPS
6. Construir el contenedor Docker
7. Iniciar el contenedor y comprobar que se esta ejecutando.



