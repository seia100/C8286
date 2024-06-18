# Ej11: Utiliza herramientas de profiling y benchmarking para identificar cuellos de botella en el rendimiento de aplicaciones paralelas.


## Metodos de medicion
### profiling

Ejemplos de uso de gprof:

```bash
gcc -pg -o my_program my_program.c
./my_program 
gprof my_program gmon.out > analysis.txt

```
## Task1: Implementa un programa paralelo (por ejemplo multiplicación de matrices) en C o C++.
```c
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
```
## task 2: Interpretación del Profiling

### Reporte Paralelo en una matriz 1000 ** 2
Flat Profile

| % Tiempo | Tiempo acumulado (ms) | Tiempo propio (ms) | Llamadas        | ms/llamada | ms/total llamada  | Nombre                      |
|----------|-----------------------|--------------------|-----------------|------------|-------------------|-----------------------------|
| 50.85    | 6850                  | 6850               | 6002000023      | 0.00       | 0.00              | _fini                       |
| 49.15    | 13470                 | 6620               |                 |            |                   | main                        |
| 0.00     | 13470                 | 0                  | 1               | 0.00       | 2280.00           | matrix_multiplication       |

#### Call Graph

- `main` llama a `matrix_multiplication` y `_fini`.
- `_fini` consume la mayor parte del tiempo después de ser llamado por `main`.
 
### Reporte Secuencial en una matriz 1000 ** 2

Flat Profile

| % Tiempo | Tiempo acumulado (ms) | Tiempo propio (ms) | Llamadas        | ms/llamada | ms/total llamada  | Nombre                      |
|----------|-----------------------|--------------------|-----------------|------------|-------------------|-----------------------------|
| 45.73    | 5840                  | 5840               | 1               | 5840.00    | 12770.00          | matrix_multiply             |
| 19.07    | 8280                  | 2440               | 2000000000      | 0.00       | 0.00              | std::vector<int>::operator[]|
| 18.56    | 10640                 | 2370               | 2000000000      | 0.00       | 0.00              | std::vector<std::vector<int>>::operator[] |
| 10.30    | 11960                 | 1310               | 1001000000      | 0.00       | 0.00              | std::vector<int>::operator[]|
| 6.34     | 12770                 | 810                | 1001000000      | 0.00       | 0.00              | std::vector<std::vector<int>>::operator[] |

#### Call Graph

- `main` llama a `matrix_multiply`, que a su vez llama a `std::vector` operadores.

### Conclusiones

- **Paralelo:**
  - La función `_fini` consume una gran parte del tiempo (6850 ms), indicando un posible overhead en la finalización del programa.
  - La función `matrix_multiplication` no consume tiempo significativo, lo cual es indicativo de una distribución efectiva del tiempo de ejecución entre los hilos.

- **Secuencial:**
  - `matrix_multiply` consume la mayor parte del tiempo (5840 ms).
  - Las operaciones de acceso a elementos de `std::vector` representan una parte significativa del tiempo de ejecución (2440 + 2370 + 1310 + 810 ms).

### Ejecución del Programa

```bash
gcc -fopenmp -o matrix_multiplication matrix_multiplication.c
./matrix_multiplication
```

## Benchmarking
permite comparar el rendimiento d ediferentes programas o en sistemas en codiciones similares

El tiempo de ejecucion 




## task 4 Optimiza el código basado en los resultados del profiling y benchmarking.

### Conversión de Matrices Bidimensionales a Unidimensionales

#### Introducción

La conversión de matrices bidimensionales a unidimensionales es una técnica común en programación para optimizar el acceso a la memoria y mejorar la eficiencia del caché. En esta técnica, una matriz bidimensional se representa como una matriz unidimensional utilizando una fórmula matemática que mapea cada par de índices bidimensionales a un índice unidimensional.

#### Representación de una Matriz Bidimensional

Considere una matriz bidimensional \(A\) de tamaño \(N \times N\). El elemento en la fila \(i\) y columna \(j\) se denota como \(A[i][j]\).

##### Conversión a una Matriz Unidimensional

Para convertir esta matriz bidimensional a una matriz unidimensional, se puede utilizar una matriz unidimensional \(A\) de tamaño \(N \times N\). La posición del elemento \(A[i][j]\) en la matriz bidimensional se mapea a la posición \(A[i \times N + j]\) en la matriz unidimensional.

#### Fórmula Matemática

Dado un índice bidimensional \((i, j)\), la posición equivalente en la matriz unidimensional se calcula como:

\[ \text{index} = i \times N + j \]

##### Ejemplo

Supongamos una matriz bidimensional de tamaño \(3 \times 3\):

\[
A = \begin{bmatrix}
a_{00} & a_{01} & a_{02} \\
a_{10} & a_{11} & a_{12} \\
a_{20} & a_{21} & a_{22} \\
\end{bmatrix}
\]

Convertimos esta matriz a una matriz unidimensional de tamaño \(9\):

\[
A = \begin{bmatrix}
a_{00}, a_{01}, a_{02}, a_{10}, a_{11}, a_{12}, a_{20}, a_{21}, a_{22}
\end{bmatrix}
\]

Para acceder al elemento \(a_{ij}\) en la matriz unidimensional, usamos la fórmula:

\[
\text{index} = i \times N + j
\]

Por ejemplo, para acceder al elemento \(a_{12}\):

\[
\text{index} = 1 \times 3 + 2 = 5
\]

Entonces, \(a_{12}\) se encuentra en la posición 5 de la matriz unidimensional.

#### Implementación en C

La implementación en C de esta conversión se puede hacer de la siguiente manera:

##### Inicialización de Matrices

```c
void initialize_matrices(double *A, double *B, double *C, int N) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            A[i * N + j] = rand() % 100;
            B[i * N + j] = rand() % 100;
            C[i * N + j] = 0;
        }
    }
}
```
#####   Multiplicación de Matrices
```c
void matrix_multiplication(double *A, double *B, double *C, int N) {
    #pragma omp parallel for collapse(2)
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            double sum = 0;
            for (int k = 0; k < N; k++) {
                sum += A[i * N + k] * B[k * N + j];
            }
            C[i * N + j] = sum;
        }
    }
}
```

#### Ventajas de la Conversión

    Mejor Localización de la Memoria: Almacenar la matriz en una sola dimensión permite un acceso más contiguo a la memoria, mejorando la eficiencia del caché de la CPU.
    Simplificación del Código: El uso de una matriz unidimensional puede simplificar la gestión de la memoria y reducir el overhead asociado a la creación y liberación de múltiples bloques de memoria.
    Eficiencia en la Paralelización: La matriz unidimensional puede ser más fácilmente paralelizable, ya que los accesos a los elementos están más alineados en la memoria.

Esta conversión es particularmente útil en aplicaciones de gran tamaño de datos donde la eficiencia del acceso a la memoria es crítica para el rendimiento.

