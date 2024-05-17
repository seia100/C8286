# Introducción a docker
## Creación de imágenes docker

$${\color{green}\text{Docker commit}}$$

1. Ejecuta un contenedor desde ubuntu:20.04 y conectar a mi linea de comando
```bahs
docker run -i -t ubuntu:20.04 /bin/bash
```

2. Instalar  el kit de herramientas de GIT

```bash
apt update
apt install -y git
```

3. comprobar si el kit de herramientas esta instalado ejecutando lo siguiente:

```bash
which git
#/usr/bin/git
```
4. salir del contenedor
```bash
exit # para salir del contenedor
```

5. verificar cambios de mi contendor. Es importante el ID container 
```bash
docker ps -a
```
![ubuntu](
```diff
- text in red
+ text in green
! text in orange
# text in gray
@@ text in purple (and bold)@@
```

$${\color{red}\text{Hola mundo}}$$


$${\color{lightblue}Light \space Blue}$$
