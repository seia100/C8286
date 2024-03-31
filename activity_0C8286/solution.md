
# install linux mint
Dado que linux mint su arquitectura es ubuntu trabajaremos desde alli y si es posible actualizaremos el _readme_ usando kali linux

Tenemos diferentes herramientas para bootear nuestro usb e intalar de manera segura
- copiar la imagen .iso en nuestro usb: https://linuxmint-installation-guide.readthedocs.io/en/latest/burn.html or also use https://ubuntu.com/tutorials/create-a-usb-stick-on-windows#1-overview
  - Tener en cuenta que si quieres instalar _mint_ desde una distribucion de linux descargas el iso y sigue estos pasos:
  -   https://www.kali.org/docs/usb/live-usb-install-with-linux/
    ** Para cualquier distribucion de linux se puede usar los comandos anteriores     
Una vez instalado mint procedemos con la actividad

# Install docker | Minikube & kubectl
use the documentations
- https://docs.docker.com/desktop/install/ubuntu/
### Prueba docker Engine
```
sudo docker version
```
![docker version](https://github.com/seia100/C8286/assets/89529418/29832b6a-218b-4c44-b23e-269317dd8879)
tiene que mostrarse de manera similar


- https://minikube.sigs.k8s.io/docs/start/
- https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/
