# Evaliacion 1: ps,grep, pipes linux, bash, awk

### Objetivos
* Aprender a listar y filtrar proceos activos en un sistema.
* Entender como identificar procesos por PID, user, uso de recursos y otros criterios.
* Utilizar `ps` para monitorear la salud y el rendimiento de aplicaciones paralelas y distribuidas.
* Aplicar `grep` para analizar logs de aplicaciones y sistemas, facilitando la depuracion y el monitoreo.
* Utilizar pipes para crear cadenas de porcesamiento de datos eficientes y scripts de analisis.
* Aprender a escribir scripts de shell para automatizar tareas de administración y despliegue.
* Entender el control de flujo, manejo de variables, y funciones en Bash.
* Desarrollar habilidades para la automatización de pruebas y despliegues en entornos de computación distribuida
* Aprender a utilizar awkpara el filtrado y transformación de datos complejos en scripts de shell.


## ps (process status) Command
Muestra informacion sobre procesos activos en un sistema.

##### usos: vistos desde la computacion paralela y concurrente

* Monitoreo de procesos: identificar y monitorear procesos 
* Gestion de recursos: observar uso de la CPU y memoria para asi optimizar aplicaciones en entornos paralelos y distribuidos.
* Depuracion y diagnostico: Identificar procesos bloqueados, zombies o que consumen recursos en exceso -> depurar y mantener el rendimiento del sistema.

* Automatizacion y scripting: automatizar la supervision y gestion de apps.
* Estudio de casos

## Monitoreo de procesos por uso excesivo de CPU

Tener en cuenta que se puede agregar en un comando directo en la linea de comando o en un _bash file_ 

```bash

```


## Identificar procesos zombis y reportar

```bash
#!/bin/bash
# Identificar procesos zombis y reportar.

ps -eo stat, pid, cmd | grep "^Z" | while read stat pid cmd; do
    echo "Proceso zombi detectado: PID=$pid CMD=$cmd"
done

```

