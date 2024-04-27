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




