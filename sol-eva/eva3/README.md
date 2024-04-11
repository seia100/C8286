# Construyendo una simple app con contenedor de Docker
##### Objetivos
Parte 1: Crear un script Bash simple

Parte 2: Crear una aplicación web simple

Parte 3: Configurar la aplicación web para utilizar archivos de sitio web

Parte 4: Crear un script de Bash para compilar y ejecutar un contenedor Docker

Parte 5: Construir, ejecutar y verificar el contenedor Docker

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
from flask impor request

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
$ python3 sample_app.py
```

