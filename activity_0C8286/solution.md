
# Install linux mint
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
![docker version](https://github.com/seia100/C8286/blob/main/activity_0C8286/assets/sdock_version.png)
tiene que mostrarse de manera similar

```
sudo container run hello-world
```
![sdocker_hw](https://github.com/seia100/C8286/blob/main/activity_0C8286/assets/sdock_hw.png)

```
sudo docker container run rancher/cowsay Hello-seia
```
![cowsay](https://github.com/seia100/C8286/blob/main/activity_0C8286/assets/test_cowsay.png)

#### Ahora evitamos el sudo
```
> sudo groupadd docker

## para conocer tu user
> whoami 

## sudo usermod -aG docker $USER
> sudo usermod -aG docker seia

``` 
probamos ejecutar sin sudo

![doc_ver](https://github.com/seia100/C8286/blob/main/activity_0C8286/assets/doc_vers.png)

ahora procedemos a instalar docker desktop https://docs.docker.com/desktop/install/linux-install/

si la instalacion esta de manera correcta deberia de salir del siguiente modo para ocnfigurar de **kubernets**

![doc_desk](https://github.com/seia100/C8286/blob/main/activity_0C8286/assets/doc_desk.png)


### Minikube & kubectl 
- https://minikube.sigs.k8s.io/docs/start/
- https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/

1. acceder al cluster
```
kubectl config get-contexts
```
2. ver cuanto nodos tiene nuestro cluster
```
kubectl get nodes
```
posterior a ejecutar los comandos anteriores se debe mostrar del siguiente modo

![minikube_and_kubectl](https://github.com/seia100/C8286/blob/main/activity_0C8286/assets/kubectl_config_get.png)

Aquí tenemos un clúster de un solo nodo. El papel del nodo es el del plano de control, loque significa que es un nodo maestro. Un clúster de Kubernetes típico consta de unospocos nodos maestros y muchos nodos trabajadores.
##### Nginx
para poder ejecutar un cluster en el servidor web Nginx nos guiaremos de las siguientes fuentes para poder ejecutar de manera eficiente y evitar errores

[Launching your First Kubernetes Cluster with Nginx running ☸🚀](https://www.linkedin.com/pulse/day-31-launching-your-first-kubernetes-cluster-nginx-running-kumar) or 
[Setting up a Kubernetes Cluster with Nginx Pod using Kind](https://byteshiva.medium.com/setting-up-a-kubernetes-cluster-with-nginx-pod-using-kind-10dcc39b59ca)

creamos el file _.yaml_ para nginx
a. create nginx.yaml ` vi nginx.yaml` // usen nano es mas bonito jejjeje
```
nano nginx.yaml
```
posterior a ello procedemos a editar o escribir lo siguiente:
```                        
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels: 
    app: nginx
spec:
  containers:
    - name: nginx
      image: nginx:latest
      ports: 
        - containerPort: 80

```
![nginx_yaml](https://github.com/seia100/C8286/blob/main/activity_0C8286/assets/nignx_yaml.png)

3. Ahora, intentemos ejecutar algo en este clúster. Usaremos Nginx, un servidor webpopular para esto. Utiliza el archivo .yaml, que acompaña a la actividad que vamos a utilizarpara esta prueba:
```
kubectl apply -f nginx.yaml
```
![created_pod](https://github.com/seia100/C8286/blob/main/activity_0C8286/assets/apply_nginx.png)

4. Podemos verificar si el pod se está ejecutando con kubectl:
```
kubectl get pods 
```
Tenemos 1 pod con Nginx ejecutándose y que se ha reiniciado 0 veces
5. Para acceder al servidor Nginx, necesitamos exponer la aplicación que se ejecuta en elpod con el siguiente comando:
```
kubectl expose pod nginx --type=NodePort --port=80
```
Esta es la única forma en que podemos acceder a Nginx desde nuestra computadoraportátil, por ejemplo, a través de un navegador. Con el comando anterior, estamos creandoun servicio de Kubernetes, como se indica en el resultado generado para el comando:`service/nginx exposed`

6. Podemos usar kubectl para enumerar todos los servicios definidos en nuestro clúster:
```
kubectl get services
```
En el resultado anterior, podemos ver el segundo servicio llamado Nginx, que acabamos decrear. El servicio es del tipo NodePort; El puerto 80 del pod se había asignado al puerto30432 del nodo del clúster de nuestro clúster de Kubernetes en minikube

![apply3456](https://github.com/seia100/C8286/blob/main/activity_0C8286/assets/apply)


7.  Ahora, podemos usar minikube para crear un túnel hacia nuestro clúster y abrir unnavegador con la URL correcta para acceder al servidor web Nginx. Utilice este comando:
```
minikube service nginx
```
si te sale el siguiente "error": `❌  Exiting due to MK_UNIMPLEMENTED: minikube service is not currently implemented with the builtin network on QEMU` traquilo(a) vamos a solucionarlo
ok no seeee :v

