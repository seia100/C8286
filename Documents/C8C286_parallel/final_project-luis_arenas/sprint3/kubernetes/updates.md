# Explicación de los cambios y adiciones:

## Sondas de vida y preparación:

Se han añadido livenessProbe y readinessProbe. Estas son cruciales para que Kubernetes pueda monitorear la salud de los contenedores y manejar el tráfico adecuadamente.
La sonda de vida (livenessProbe) verifica si el contenedor está funcionando correctamente.
La sonda de preparación (readinessProbe) determina si el contenedor está listo para recibir tráfico.


## Configuración de las sondas:

Ambas sondas utilizan comprobaciones HTTP GET en rutas específicas (/health y /ready).
Se han configurado retrasos iniciales y períodos de sondeo para evitar falsos positivos durante el inicio del contenedor.


## Recursos:

La configuración de recursos se mantiene igual, asegurando que cada pod tenga los recursos necesarios para funcionar eficientemente.


## Variables de entorno:

Se mantiene la configuración para la URI de MongoDB, obtenida de un secreto de Kubernetes.

Estos archivos de configuración de Kubernetes proporcionan una configuración completa para desplegar el sistema IDS en un cluster de Kubernetes:

- deployment.yaml: Define cómo se debe desplegar la aplicación IDS, incluyendo la imagen del contenedor, recursos, y configuraciones.
- service.yaml: Expone la aplicación IDS dentro del cluster.
ingress.yaml: Configura el acceso externo a la aplicación IDS, incluyendo el enrutamiento y la terminación TLS.
- hpa.yaml: Configura el escalado automático basado en el uso de CPU y memoria.
- configmap.yaml: Almacena configuraciones no sensibles que pueden ser montadas en los pods.
- secrets.yaml: Almacena información sensible como credenciales de base de datos y claves API.

Estos archivos trabajan juntos para proporcionar un despliegue robusto, seguro y escalable del sistema IDS en Kubernetes. Asegúrese de reemplazar los valores de placeholder (como your-registry.com, ids.yourdomain.com, etc.) con los valores específicos de su entorno antes de aplicar estas configuraciones.