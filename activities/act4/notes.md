Si deseo ajustar la gestion de trabajadores y se tiene que agregar un modulo adicional y se llama `threding`
y asi tener control sobre los trabajadores.

Problema: no se puede interactuar con cod externo
  `map results = executor.map(mapper, my_input)`

e sun porbea en textos grandes

el codigo de `map_reduce_with_progress` y para hacer una retroalimentacion se impementa una funcion externa para el seguimiento del progreso.
`executor.submit` en reemplazo de `executor.map` ya que es un control mas intenso.

La recomendacion es que podamos tener un control sobre tareas muy grandes y lo podemos tener en tareas grandes y tener un seguimineto del trabajo del que estamos haciendo.


Tood es *PROGRAMACIN FUNCIONAL*

## threaded_mapreduce.py

nuevamente usamo lo que es relacionado con `concurrent.futures`

un _future_ es un resultado potencial de un `away` es la ofrma mas basica de escribir una fucion.
que peude estar sujeto a la palabra clave (away) y podemos hacer que haga un seguimiento de progreso.

####recomiendo explicar el codigo a mas profundidad.

```python
words = 'Python es super Python rocks'.split(' ')

with Executor(max_workers=4) as executor: # tenemos 4 ejecutores
    maps = map_less_naive(executor, words, emitter) 
    print(maps[-1])
    not_done = 1
    while not_done > 0:
        not_done = 0
        for fut in maps:
            not_done += 1 if not fut.done() else 0 # comprueba si el feature esta realizado
        sleep(1)
        print(f'Aun no ha finalizado: {not_done}')

```
Necesitamos una forma para que el que llama pueda estar informado del progreso y para elllo es necesario un _callback_

```python
ef report_progress(futures, tag, callback):
    not_done = 1
    done = 0
    while not_done > 0:
        not_done = 0
        done = 0
        for fut in futures:
            if fut.done():
                done +=1
            else:
                not_done += 1
        sleep(0.5)
        if not_done > 0 and callback:
            callback(tag, done, not_done)
```

se llamara cuando ocurre un evento y vamos hacer un seguimiento de todos los maps y reduces
y se pimplemtna de en la sigiuente lineas de cod

las funciones que me ayudan hacer tal seguimiento son `map_reduce_less_naive` y `report_progress`

report progress
lo que requiere un funcion callback cada 0.5 segundos para ver el progreso.
` report_progress(futures, 'reduce', callback)` reporta todo del progreso de todas las tareas _reduce_ de igual amanera pasa para _map_.
un _callbak_ debe ser muy rapida, pero eso lo decido io :D

cython solo ejecuta un subproceso a la vez, debido al _gil_

#### GIL: impone una restriccion solo se peude ejecutar un subproceso a la vez. 

para entrar en el paralelismo multithreading
si quieres redimientos los subprocesoss ne python rara vez son mejores. python debe ser muy lento si quiero programacion de rendimiento en subprocesos

a menos que la implemntacion en cypthon mejora, pero tien un costo. 

el problema del cruce entre la cpu y el gil que es ejecutar muchos procesos a la vez y por eso hay ese cruce.

si quiero codigo de alto rendimiento a nivel subprocesos pyhton no sea lo mejor. Por lo que sale una solucion y tiene caracteristicas dianmicas `Cpython`
pero si quiero eficiencia se rpograma en `C ` o `rast ` y `cython` una extension de c en python. o [Numba](http://numba.pydata.org/){:target="_blank"}

Escribimos solo la parte paralela en otro lenguaje y luego subirlo a python con un nivel de granularidad
no se hace con multithreding sino con multiprocesamiento.

procesamoento para hacer paralelismo y si tener toda la potencia de la cpu.

#### marshal, dill, pickle
si queremos velocidad usar marshal caso contrario pickle

no es posible transmitir lanmdas con pickle lo que hacemos es implementar nuestro propio protocolo

#### lamndas
no se puede usar entre procesos con pickle por eso necesitamos reescribir un 

sokcets

con los subprocesos todos con los tipos de objetos se puede compartir y antes se debe comprobar si son seguros de transmitir.
si estamos trabajando ocn primitivas y eso eso esta bn para procsamiento para grano grueso: baja comunicacion.

pickle y multiprocessing se llevan bien

### falta explicacion

un pool se crea cada vez que se necesita una funcion map reduce y el precio que estamos pagando es cuando creamos un pool

-> **eager and lazy**
la semantica de Pool.map(fun, data) //Eager: 
map(fun, data) // Lazy : regresa y no se ejecuta

ahora si hacemos con list

list(map(fun, data)) //sera que es similar a esto lo de eager?

## mp_mpareduce2.py

Pool.map.async es importante sol informa al final de la funcion y no es sufi 

```
map_results = [ret.get() for ret in map_returns]
```

no hay caoss generales y ejemplos de casos mas grandes y no se puede consumir tiempo y recursos :D

tener en cuenta de cerrar el pool
``pool(close())``

practicar [vim adventures](https://vim-adventures.com/)

adicional a ello plugins 
