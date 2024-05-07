#### Source
# [Learning the shell](https://linuxcommand.org/lc3_learning_the_shell.php)

```bash
du -s * | sort -nr > $HOME/user_space_report.txt
```
en este caso el comando del que se esta usando es para calcular el uso del espacio de cada archivo y directorio en un determinado directorio o en en el caso del actual.

1. `du -S *`:
  * `du` es un comando para estimar el uso del espacio en disco de archivos y directorios.
  * La opcion `-s` le indica a `du` que muestre solo un sumario del uso toral del disco para cada argument, en este caso para cada archivo y directorio en el direcotio actual (denotado por *)

2. `| sort -nr`
  * El simbolo `|` es una tuberia que toma la slaida del comando anterior  `(du -s *)` y lo pasa omo entrada al siguiente comando (`sort`).
  * `sort` ordena lineas de entrada
  * `-n` le indica a _sort_ que compare segun el valor numerico de las cadenas.
  * `-r` indica a _sort_ que ordene los resultados en orden descendente
3. `> $HOME/user_space_report.txt`
  * `>` Es un operador de redireccion que toma la salida del comando anteior y la escribe en un archivo, en este caso *user_space_report.txt*
  * `$HOME ` variable de entorno que ocntiene la rutal al directorio principal del usuario.
  * 

![du](https://github.com/seia100/C8286/blob/main/sol-eva/eva0/Screenshot%20from%202024-04-26%2021-44-47.png)

## Navigation

* `pwd` print working directory
* `cd` change directory
* `ls` lsit diles and directories

![pwd_ls](https://github.com/seia100/C8286/blob/main/sol-eva/eva0/pwd-ls.png)
![cd-ls-a](https://github.com/seia100/C8286/blob/main/sol-eva/eva0/usr-ls-a.png)

* notar que hago uso de `ls -a`. La opcion _a_ me permite visualizar los archivos que son "." o ".."


## Looking around 
* [ls](https://linuxcommand.org/lc3_man_pages/ls1.html): list files and directories
* [less](https://linuxcommand.org/lc3_man_pages/less1.html): view text files
* [file](https://linuxcommand.org/lc3_man_pages/file1.html): classify a file;s contents

![doc-ls](https://github.com/seia100/C8286/blob/main/sol-eva/eva0/ls-doc.png)



#### Important
*tener en consideracion los siguientes accesos o informacion del sistema mediante directorios de configuracion del sistema. 
[important directories](https://linuxcommand.org/lc3_lts0040.php)
________________________---

## Manipuling Files
* [cp](https://linuxcommand.org/lc3_man_pages/cp1.html): copy files and directories
* [mv](https://linuxcommand.org/lc3_man_pages/mv1.html): move or rename files and directories
* [rm](https://linuxcommand.org/lc3_man_pages/rm1.html): remove files and directories
* [mkdir](https://linuxcommand.org/lc3_man_pages/mkdir1.html)


#### how use `cp`
* `cp -i` solicita confirmacion. si el archivo existe te pide que confirmes para que sobreescribas
* `cp` Mientras copia el archivo a otra direccion y si no existe el nombre de `file2` lo crea

![cp-practice](https://github.com/seia100/C8286/blob/main/sol-eva/eva0/cp-practice.png)

### mv
comando para mover de un direcotrio/archivo a otro un directorio/archivo.

![move_directory](https://github.com/seia100/C8286/blob/main/sol-eva/eva0/mv_move.png)

En este caso ``..`` son para referirse al directorio anterior de modo que ya no se copia todo el _path_ del directorio anterior. En caso que se quiera renombrar un archivo no es necesario escribir el path solo el nombre es decir _mv [before_name_file] [new_name_file]_ 

### rm
The rm command removes (deletes) files and directories.
* Algunas opciones
 * `-i` para confirmar el archivo o file a eliminar.
 * `-r` eliminar un directorio de manera recursiva. Es decir todos los directorios que estan anidados en el directorio por eliminar.
 
![rm_reursive](https://github.com/seia100/C8286/blob/main/sol-eva/eva0/rm_recursive.png)

## Working with commands
* [type](https://linuxcommand.org/lc3_man_pages/typeh.html) Display information about command type
* [which](https://linuxcommand.org/lc3_man_pages/which1.html) Locate a command
* [help](https://linuxcommand.org/lc3_man_pages/helph.html) Display referencce page for shell builtin
* [man](https://linuxcommand.org/lc3_man_pages/man1.html) Display an on-line command reference

### type
muestra el tipo de comando que ejecutara el shell.

### which
En caso que haya mas de una version de- un programa ejecutable instalado en un sistema. Es decir, para determinar la ubicación exacta de un determinado ejecutable.

Por ejemplo en las siguientes lineas de codigo nos proporciona informacion de algunos comando de los directorios como tal.

`[type_which](https://github.com/seia100/C8286/blob/main/sol-eva/eva0/type-wich.png)


