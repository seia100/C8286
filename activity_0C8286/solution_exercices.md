A veces, probar con un clúster de un solo nodo no es suficiente. minikube lo resuelve. Sigaestas instrucciones para crear un verdadero clúster de Kubernetes de múltiples nodos enminikube:

## Probemos multiclusters
Documentacion de interes: [Creating a kubernets cluster with multiple nodes using minikube](https://pet2cattle.com/2021/01/multinode-minikube)

1. trabajar con varios nodos en minikube, podemos comandar
```
minikube start --nodes 3 -p demo
```

2. utilizar kubectl para ver o enimerar todos los nodos del cluster
```
kubectl get nodes
```
3.  SIP desafortunadamente esto es todo hasta aqui no hay mas dentro de los ejercicios a desarrollar.
```
minikube stop -p demo
```

4.  Eliminamos todos los nodos del sistema
```
minikube delete --all
```
y ps biennn ahora zomozz :3

continuamos con la actividad de Kind


