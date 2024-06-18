/* guide:
* geeksforgeeks and LLM
https://www.geeksforgeeks.org/multiplication-of-matrix-using-threads/
with openMP:
https://people.math.sc.edu/Burkardt/C_src/mxm_openmp/mxm_openmp.html

*/

// OpenMP: paralelizar aplicaciones en C y C++

#include <stdio.h>
#include <stdlib.h>
#include <omp.h> // openmp

#define N 1000 // Define el tamaño de las matrices como 1000x1000

// Función para inicializar las matrices A, B y C
void initialize_matrices(double **A, double **B, double **C) {
    for (int i = 0; i < N; i++) { // Itera sobre las filas
        for (int j = 0; j < N; j++) { // Itera sobre las columnas
            A[i][j] = rand() % 100; // Asigna un valor aleatorio a cada elemento de A
            B[i][j] = rand() % 100; // Asigna un valor aleatorio a cada elemento de B
            C[i][j] = 0; // Inicializa C con ceros
        }
    }
}

// Función para realizar la multiplicación de matrices A y B, almacenando el resultado en C
void matrix_multiplication(double **A, double **B, double **C) {
    double start, end; // Variables para medir el tiempo

    start = omp_get_wtime(); // Obtiene el tiempo de inicio
    #pragma omp parallel for // Directiva de OpenMP para paralelizar el bucle siguiente
    for (int i = 0; i < N; i++) { // Itera sobre las filas de A y C
        for (int j = 0; j < N; j++) { // Itera sobre las columnas de B y C
            for (int k = 0; k < N; k++) { // Itera sobre las columnas de A y filas de B
                C[i][j] += A[i][k] * B[k][j]; // Realiza la multiplicación de matrices
            }
        }
    }
    end = omp_get_wtime(); // Obtiene el tiempo de finalización
    printf("Time taken for matrix multiplication inside function: %f seconds\n", end - start); // Imprime el tiempo tomado para la multiplicación de matrices
}

int main() {
    // Reservar memoria para las matrices
    // https://www.programiz.com/c-programming/c-dynamic-memory-allocation
    double **A = (double **)malloc(N * sizeof(double *)); // Reserva memoria para un array de punteros a double
    double **B = (double **)malloc(N * sizeof(double *)); // Reserva memoria para un array de punteros a double
    double **C = (double **)malloc(N * sizeof(double *)); // Reserva memoria para un array de punteros a double
    for (int i = 0; i < N; i++) {
        A[i] = (double *)malloc(N * sizeof(double)); // Reserva memoria para cada fila de A
        B[i] = (double *)malloc(N * sizeof(double)); // Reserva memoria para cada fila de B
        C[i] = (double *)malloc(N * sizeof(double)); // Reserva memoria para cada fila de C
    }

    // Inicializar las matrices
    initialize_matrices(A, B, C); // Llama a la función para inicializar las matrices A, B y C

    // Medir el tiempo de ejecución
    double start_time = omp_get_wtime(); // Obtiene el tiempo de inicio
    matrix_multiplication(A, B, C); // Llama a la función para multiplicar las matrices
    double end_time = omp_get_wtime(); // Obtiene el tiempo de finalización

    printf("Total time taken for matrix multiplication: %f seconds\n", end_time - start_time); // Imprime el tiempo total tomado para la multiplicación de matrices

    // Liberar memoria
    for (int i = 0; i < N; i++) {
        free(A[i]); // Libera la memoria reservada para cada fila de A
        free(B[i]); // Libera la memoria reservada para cada fila de B
        free(C[i]); // Libera la memoria reservada para cada fila de C
    }
    free(A); // Libera la memoria reservada para el array de punteros A
    free(B); // Libera la memoria reservada para el array de punteros B
    free(C); // Libera la memoria reservada para el array de punteros C

    return 0; // Retorna 0 indicando que el programa finalizó correctamente
}


/*
execute:
```bash
gcc -fopenmp -o matrix_multiplication matrix_multiplication.c
./matrix_multiplication
```

Genera el reporte de profiling: 
gprof ./matrix_mult gmon.out > report.txt
*/