/* 

11 . Utiliza herramientas de profiling y benchmarking para identificar 
cuellos de botella en el rendimiento de aplicaciones paralelas.

Tareas:

    Implementa un programa paralelo (por ejemplo multiplicación de matrices) en C o C++.
    Utiliza herramientas de profiling (e.g., gprof, perf) para identificar las partes del código que consumen más tiempo.
    Realiza benchmarking con diferentes tamaños de matrices y comparar los resultados.
    Optimiza el código basado en los resultados del profiling y benchmarking.
    Realiza los pasos anteriores usando python.


*/
#include <iostream>   // Incluye la biblioteca para la entrada y salida estándar
#include <vector>     // Incluye la biblioteca para el uso de la clase std::vector
#include <chrono>     // Incluye la biblioteca para el manejo de tiempo y cronometraje

using namespace std;  // Usa el espacio de nombres estándar para evitar tener que usar std::

void matrix_multiply(const vector<vector<int>>& A, const vector<vector<int>>& B, vector<vector<int>>& C, int N) {
    // Función que realiza la multiplicación de matrices A y B, almacenando el resultado en C
    for (int i = 0; i < N; ++i) {  // Recorre cada fila de la matriz A
        for (int j = 0; j < N; ++j) {  // Recorre cada columna de la matriz B
            C[i][j] = 0;  // Inicializa el valor de C[i][j] a 0
            for (int k = 0; k < N; ++k) {  // Recorre los elementos para realizar la multiplicación de matrices
                C[i][j] += A[i][k] * B[k][j];  // Acumula el producto de los elementos correspondientes
            }
        }
    }
}

int main() {
    int N = 1000;  // Define el tamaño de las matrices como 1000x1000
    vector<vector<int>> A(N, vector<int>(N, 1));  // Inicializa la matriz A con todos sus elementos en 1
    vector<vector<int>> B(N, vector<int>(N, 1));  // Inicializa la matriz B con todos sus elementos en 1
    vector<vector<int>> C(N, vector<int>(N, 0));  // Inicializa la matriz C con todos sus elementos en 0

    auto start = chrono::high_resolution_clock::now();  // Captura el tiempo actual antes de la multiplicación
    matrix_multiply(A, B, C, N);  // Llama a la función para multiplicar las matrices A y B, almacenando el resultado en C
    auto end = chrono::high_resolution_clock::now();  // Captura el tiempo actual después de la multiplicación

    chrono::duration<double> diff = end - start;  // Calcula la duración de la multiplicación
    cout << "Tiempo de ejecución: " << diff.count() << " s" << endl;  // Imprime el tiempo de ejecución en segundos

    return 0;  // Finaliza la función main y retorna 0, indicando que el programa terminó correctamente
}


/*

    Compila con 
        g++ -o matrix_mult matrix_mult.cpp -pg
    Ejecuta el programa: 
        ./matrix_mult . 
    Genera el reporte de profiling: 
        gprof ./matrix_mult gmon.out > report.txt

*/