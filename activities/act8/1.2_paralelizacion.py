import numpy as np
from joblib import Parallel, delayed

def multiply_sub_matrices(A, B):
    return np.dot(A, B)

def parallel_matrix_multiplication():
    A = np.random.rand(1000, 1000)
    B = np.random.rand(1000, 1000)
    # la matriz se divide en 4 partes 
    A_subs = np.array_split(A, 4, axis=0) # a lo largo de las filas 
    B_subs = np.array_split(B, 4, axis=1) # a lo largo de las columnas

    results = Parallel(n_jobs=4)(delayed(multiply_sub_matrices)(A_sub, B_sub) for A_sub in A_subs for B_sub in B_subs)
    
    C = np.zeros((1000, 1000))

    segment_size = 250
    for i, res in enumerate(results):
        # C[i*250:(i+1)*250, :] = res # se rellena la matriz

        #mis cambios
        row_idx = (i // 4) * segment_size  # Calcula el índice de fila correcto
        col_idx = (i % 4) * segment_size  # Calcula el índice de columna correcto
        C[row_idx:row_idx+segment_size, col_idx:col_idx+segment_size] = res
    return C

print(parallel_matrix_multiplication())
