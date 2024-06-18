#include <stdio.h>
#include <stdlib.h>
#include <omp.h> // openmp

// Función para inicializar las matrices A, B y C
void initialize_matrices(double *A, double *B, double *C, int N) {
    for (int i = 0; i < N; i++) { // Itera sobre las filas
        for (int j = 0; j < N; j++) { // Itera sobre las columnas
            A[i * N + j] = rand() % 100; // Asigna un valor aleatorio a cada elemento de A
            B[i * N + j] = rand() % 100; // Asigna un valor aleatorio a cada elemento de B
            C[i * N + j] = 0; // Inicializa C con ceros
        }
    }
}

// Función para realizar la multiplicación de matrices A y B, almacenando el resultado en C
void matrix_multiplication(double *A, double *B, double *C, int N) {
    double start, end; // Variables para medir el tiempo

    start = omp_get_wtime(); // Obtiene el tiempo de inicio
    #pragma omp parallel for collapse(2) // Directiva de OpenMP para paralelizar el bucle siguiente
    for (int i = 0; i < N; i++) { // Itera sobre las filas de A y C
        for (int j = 0; j < N; j++) { // Itera sobre las columnas de B y C
            double sum = 0;
            for (int k = 0; k < N; k++) { // Itera sobre las columnas de A y filas de B
                sum += A[i * N + k] * B[k * N + j]; // Realiza la multiplicación de matrices
            }
            C[i * N + j] = sum;
        }
    }
    end = omp_get_wtime(); // Obtiene el tiempo de finalización
    printf("Time taken for matrix multiplication of size %d: %f seconds\n", N, end - start); // Imprime el tiempo tomado para la multiplicación de matrices
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <matrix size>\n", argv[0]);
        return 1;
    }

    int N = atoi(argv[1]);
    if (N <= 0) {
        fprintf(stderr, "Matrix size must be a positive integer\n");
        return 1;
    }

    // Reservar memoria para las matrices en una sola dimensión
    double *A = (double *)malloc(N * N * sizeof(double)); // Reserva memoria para una matriz unidimensional que representa una bidimensional
    double *B = (double *)malloc(N * N * sizeof(double)); // Reserva memoria para una matriz unidimensional que representa una bidimensional
    double *C = (double *)malloc(N * N * sizeof(double)); // Reserva memoria para una matriz unidimensional que representa una bidimensional

    // Inicializar las matrices
    initialize_matrices(A, B, C, N); // Llama a la función para inicializar las matrices A, B y C

    // Medir el tiempo de ejecución
    double start_time = omp_get_wtime(); // Obtiene el tiempo de inicio
    matrix_multiplication(A, B, C, N); // Llama a la función para multiplicar las matrices
    double end_time = omp_get_wtime(); // Obtiene el tiempo de finalización

    printf("Total time taken for matrix multiplication of size %d: %f seconds\n", N, end_time - start_time); // Imprime el tiempo total tomado para la multiplicación de matrices

    // Liberar memoria
    free(A); // Libera la memoria reservada para la matriz unidimensional A
    free(B); // Libera la memoria reservada para la matriz unidimensional B
    free(C); // Libera la memoria reservada para la matriz unidimensional C

    return 0; // Retorna 0 indicando que el programa finalizó correctamente
}
