import numpy as np
from multiprocessing import Pool
import time
import cProfile
import pstats
import io

# Función que multiplica una fila de A por la matriz B
def multiply_row(row, B):
    return np.dot(row, B)

# Función que paraleliza la multiplicación de matrices
def parallel_multiply_matrices(A, B, num_processes=None):
    # Crear un pool de procesos con el número especificado de procesos
    with Pool(processes=num_processes) as pool:
        # Aplicar la función multiply_row a cada fila de A con la matriz B usando starmap
        result = pool.starmap(multiply_row, [(row, B) for row in A])
    # Convertir el resultado en un array de numpy y devolverlo
    return np.array(result)

# Lista de tamaños de matrices para el benchmarking
matrix_sizes = [100, 200, 500, 1000]

# Realizar benchmarking
for size in matrix_sizes:
    print(f"Benchmarking con matrices de tamaño {size}x{size}")
    
    # Generar matrices aleatorias A y B de tamaño 'size'
    A = np.random.randint(0, 100, size=(size, size)) 
    B = np.random.randint(0, 100, size=(size, size)) 

    # Crear un objeto de perfilador
    pr = cProfile.Profile()

    # Medir el tiempo de ejecución para la versión paralela con profiling
    pr.enable()  # Iniciar el profiling
    start_time = time.time()  # Registrar el tiempo inicial
    result = parallel_multiply_matrices(A, B, num_processes=4)  # Ejecutar la multiplicación de matrices en paralelo
    end_time = time.time()  # Registrar el tiempo final
    pr.disable()  # Detener el profiling
    parallel_time = end_time - start_time
    print(f"Parallel optimization: Tiempo de ejecución: {parallel_time} segundos")

    if (size == 1000):
        # Guardar resultados del profiling en un archivo
        with open("profile_1000_py.txt", "a") as f:
            ps = pstats.Stats(pr, stream=f).sort_stats(pstats.SortKey.CUMULATIVE)
            ps.print_stats()
            f.write("\n" + "-"*80 + "\n")

    # Medir el tiempo de ejecución para la versión tradicional
    start_time = time.time()
    result2 = np.dot(A, B)
    end_time = time.time()
    traditional_time = end_time - start_time
    print(f"Tradicional: Tiempo transcurrido: {traditional_time} segundos")
    
    print('-' * 60)
