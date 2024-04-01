# Kind
es otra herramienta popular que sepuede utilizar para ejecutar un clúster de Kubernetes de múltiples nodos localmente en sumáquina.

## Install kind
* Documentation: https://kind.sigs.k8s.io/docs/user/quick-start/#installing-from-release-binaries

1. Si bien en la guia tenemos la guia del curso (acticidad0) tenemos pasaso para instalar. Sin embargo usaremos la documentacion anterior adjunta.
* dado que neusrta arch es x86_64 emplearemos los siguientes comands
```
[ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.22.0/kind-linux-amd64

chmod +x ./kind

sudo mv ./kind /usr/local/bin/kind
```
2. Una vez instalado Kind, revisamos la rversion.
```
kind version
```

3. Ahora, intente crear un clúster de Kubernetes simple que consta de un nodo maestro ydos nodos trabajadores.

```
kind create cluster
```
4. Para verificar que se ha creado un clúster, utilice este comando:
```
kind get cluster
```
5.  Podemos crear un clúster adicional con un nombre diferente usando el parámetro --name, así:
```
kind create cluster --name demo-seia
```

6.  mostramos o listamos los clusters creados
```
kind get clusters
```

### Ejecutamos nuestra primera aplicacion. Usaeremos Nginx para ello. 

1. Ahora podemos usar kubectl para acceder y trabajar con los clústeres que acabamos decrear. Mientras creaba un clúster, Kind también actualizó el archivo de configuración denuestro kubectl.

```
kubectl config get-contexts
```
2. Utilice el siguiente comando para convertir el clúster de demo en su clúster actual si elasterisco indica que hay otro clúster actual:
```
kubectl config use-context kind-demo-seia
```
en nuestro caso es seia, ya no ejecutamos esto ya que el es el cluster actual _demo-seia_
3.  enumerar nodos
```
kubectl get nodes
```

4. Ahora, intentemos ejecutar el primer contenedor en este clúster. Usaremos nuestroservidor web Nginx de confianza, como hicimos antes. Utilice el siguiente comando paraejecutarlo:
```
kubectl apply -f nginx.yaml
```
5. Para acceder al servidor Nginx, necesitamos realizar el reenvío de puertos usandokubectl. Utilice este comando para hacerlo:Revisa: kubectl describe pod nginx, https://www.kristhecodingunicorn.com/post/kubernetes-port-forwarding-cleanup-of-orphaned-ports/
```
kubectl port-forward nginx 8080:80 
```
Tener en cuenta que se puede usar otros puertos 
un vez que se haya completado la intencion o el proposito de la actividad _kind_ 
Eliminamos el pod del cluster
```
kind delete -f nginx.yaml
```

Antes de continuar, limpiemos y eliminemos los dos clústeres que acabamos de crear:
```
kind delete cluster --name kind
kind delete cluster --namem demo-seia
```
puede servir :) https://blog.serialexperiments.co.uk/posts/kubernetes-port-forward-already-in-use/
Con esto andamo feli :3 
*No olvidar de revisar las preguntas :3

FINISH
