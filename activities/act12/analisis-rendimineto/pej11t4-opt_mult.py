import numpy as np
import multiprocessing as mp
import time
import cProfile
import pstats
import io

# Definir la función para multiplicar submatrices
def matrix_multiply_worker(A_sub, B, result, row_start, row_end):
    # Multiplicar la submatriz A_sub por B y guardar el resultado en result
    result[row_start:row_end] = np.dot(A_sub, B)

# Dividir el trabajo en procesos paralelos
def parallel_matrix_multiply(A, B, num_workers=4):
    # Obtener el número de filas de la matriz A
    num_rows = A.shape[0]
    # Calcular el tamaño de cada chunk (fragmento)
    chunk_size = num_rows // num_workers
    # Crear una matriz de ceros para almacenar el resultado
    result = np.zeros((num_rows, B.shape[1]))

    # Lista para almacenar los procesos
    processes = []
    for i in range(num_workers):
        # Calcular el índice de inicio del chunk
        row_start = i * chunk_size
        # Calcular el índice de finalización del chunk
        row_end = (i + 1) * chunk_size if i != num_workers - 1 else num_rows
        # Extraer la submatriz de A que se procesará
        A_sub = A[row_start:row_end, :]
        # Crear un nuevo proceso para multiplicar la submatriz
        p = mp.Process(target=matrix_multiply_worker, args=(A_sub, B, result, row_start, row_end))
        # Añadir el proceso a la lista de procesos
        processes.append(p)
        # Iniciar el proceso
        p.start()

    # Esperar a que todos los procesos terminen
    for p in processes:
        p.join()

    # Devolver la matriz de resultado
    return result

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
    result2 = parallel_matrix_multiply(A, B)  # Ejecutar la multiplicación de matrices en paralelo
    end_time = time.time()  # Registrar el tiempo final
    pr.disable()  # Detener el profiling
    parallel_time = end_time - start_time
    print(f"Parallel optimization: Tiempo de ejecución: {parallel_time} segundos")

    # Guardar resultados del profiling en un archivo
    with open("profile_1000_optpy.txt", "a") as f:
        ps = pstats.Stats(pr, stream=f).sort_stats(pstats.SortKey.CUMULATIVE)
        ps.print_stats()
        f.write("\n" + "-"*80 + "\n")

    # Medir el tiempo de ejecución para la versión tradicional
    start_time = time.time()
    result2t = np.dot(A, B)
    end_time = time.time()
    traditional_time = end_time - start_time
    print(f"Tradicional: Tiempo transcurrido: {traditional_time} segundos")
    
    # Comparar los tiempos
    # print(f"Ratio (parallel/traditional): {parallel_time / traditional_time}")
    print('-' * 60)
