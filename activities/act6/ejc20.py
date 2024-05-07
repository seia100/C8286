# defaultdict proporciona un diccionario con un valor por defecto para claves que no existen.
# Es útil para manejar colecciones de elementos agrupados sin tener que verificar si una clave ya existe.
from collections import defaultdict

# multiprocessing permite crear procesos que pueden ejecutar tareas en paralelo.
import multiprocessing as mp

# sys es utilizado para interactuar directamente con el intérprete de Python.
import sys

# time proporciona funciones para trabajar con tiempo, como pausas y marcas de tiempo.
import time
# sleep es una función específica del módulo time usada para hacer pausas en la ejecución.
from time import sleep

# reduce es una función que reduce una colección a un solo valor, aplicando una función acumulativa.
from functools import reduce



# Función para reportar el progreso de las tareas
def report_progress(map_returns, tag, callback):
    done = 0
    num_jobs = len(map_returns)
    while num_jobs > done:
        done = 0
        for ret in map_returns:
            if ret.ready():
                done += 1
        sleep(0.5)  # Espera antes de verificar de nuevo
        if callback:
            callback(tag, done, num_jobs - done)

# Función para dividir los datos en trozos (chunks)
def chunk(my_iter, chunk_size):
    chunk_list = []
    for elem in my_iter:
        chunk_list.append(elem)
        if len(chunk_list) == chunk_size:
            yield chunk_list
            chunk_list = []
    if len(chunk_list) > 0:
        yield chunk_list

# Ejecuta una función sobre un conjunto de datos en un proceso separado
def chunk_runner(fun, data):
    ret = []
    for datum in data:
        ret.append(fun(datum))
    return ret

# Mapeo asíncrono de datos a procesos utilizando chunking
def chunked_async_map(pool, mapper, data, chunk_size):
    async_returns = []
    for data_part in chunk(data, chunk_size):
        async_returns.append(pool.apply_async(chunk_runner, (mapper, data_part)))
    return async_returns

# Función principal de map_reduce
def map_reduce(pool, my_input, mapper, reducer, chunk_size, callback=None): 
    map_returns = chunked_async_map(pool, mapper, my_input, chunk_size)
    report_progress(map_returns, 'map', callback)
    map_results = []
    for ret in map_returns:
        map_results.extend(ret.get())
    total_sum = reduce(reducer, map_results)  # Reduce los resultados para obtener la suma total
    return total_sum

# Función de mapeo que devuelve el cuadrado de un número
def square_mapper(n):
    """Returns the square of the number."""
    return n * n

# Función de reducción que suma dos elementos
def sum_reducer(x, y):
    """Accumulate sum of elements."""
    return x + y

# Función para reportar el progreso de la operación
def reporter(tag, done, not_done):
    print(f'Operacion {tag}: {done}/{done + not_done}')

# Función para ejecutar el map_reduce
def run_map_reduce(numbers, chunk_size):
    pool = mp.Pool()  # Crea un pool de procesos
    start_time = time.time()  # Tiempo de inicio
    total_sum = map_reduce(pool, numbers, square_mapper, sum_reducer, chunk_size, reporter)
    pool.close()  # Cierra el pool
    pool.join()  # Espera a que todos los procesos terminen
    end_time = time.time()  # Tiempo de fin
    duration = end_time - start_time
    return duration, total_sum

if __name__ == '__main__':
    numbers = list(range(1, 1001))  # Lista de números del 1 al 1000
    chunk_sizes = [1, 10, 100, 1000, 10000]
    results = []

    for size in chunk_sizes:
        duration, total_sum = run_map_reduce(numbers, size)
        results.append((size, total_sum, duration))

    print("\nTam fragmentacion | Suma de cuadrados | Duracion")
    print("-" * 50)
    for size, total_sum, duration in results:
        print(f"{size:<16} | {total_sum:<18} | {duration:.2f} segundos")
