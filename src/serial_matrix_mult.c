#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "../include/utils.h"

void multiply_matrices(double **A, double **B, double **C, int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <matrix_size>\n", argv[0]);
        return 1;
    }
    int n = atoi(argv[1]);
    if (n <= 0) {
        printf("Matrix size must be positive.\n");
        return 1;
    }

    double **A, **B, **C;
    allocate_matrix(&A, n);
    allocate_matrix(&B, n);
    allocate_matrix(&C, n);

    randomize_matrix(A, n);
    randomize_matrix(B, n);
    zero_matrix(C, n);

    clock_t start = clock();
    multiply_matrices(A, B, C, n);
    clock_t end = clock();

    double elapsed = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Serial matrix multiplication (n=%d) took %.6f seconds.\n", n, elapsed);

    if (n <= 8) {
        printf("Matrix A:\n");
        print_matrix(A, n);
        printf("Matrix B:\n");
        print_matrix(B, n);
        printf("Result C = A * B:\n");
        print_matrix(C, n);
    }

    free_matrix(A, n);
    free_matrix(B, n);
    free_matrix(C, n);
    return 0;
} 