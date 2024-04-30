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

