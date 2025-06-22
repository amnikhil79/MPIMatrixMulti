#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include "../include/utils.h"

void mpi_multiply_matrices(double *local_A, double *B, double *local_C, 
                          int local_rows, int n) {
    for (int i = 0; i < local_rows; i++) {
        for (int j = 0; j < n; j++) {
            local_C[i * n + j] = 0.0;
            for (int k = 0; k < n; k++) {
                local_C[i * n + j] += local_A[i * n + k] * B[k * n + j];
            }
        }
    }
}

int main(int argc, char *argv[]) {
    int rank, size;
    int n;
    double **A = NULL, **B = NULL, **C = NULL;
    double *flat_A = NULL, *flat_B = NULL, *flat_C = NULL;
    double *local_A = NULL, *local_C = NULL;
    int local_rows;
    double start_time, end_time;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (argc != 2) {
        if (rank == 0) {
            printf("Usage: mpirun -np <num_processes> %s <matrix_size>\n", argv[0]);
        }
        MPI_Finalize();
        return 1;
    }

    n = atoi(argv[1]);
    if (n <= 0) {
        if (rank == 0) {
            printf("Matrix size must be positive.\n");
        }
        MPI_Finalize();
        return 1;
    }

    if (n % size != 0) {
        if (rank == 0) {
            printf("Matrix size (%d) must be divisible by number of processes (%d).\n", n, size);
        }
        MPI_Finalize();
        return 1;
    }

    local_rows = n / size;

    // Allocate memory for local data
    local_A = (double *)malloc(local_rows * n * sizeof(double));
    local_C = (double *)malloc(local_rows * n * sizeof(double));
    flat_B = (double *)malloc(n * n * sizeof(double));

    if (rank == 0) {
        // Master process: allocate and initialize matrices
        allocate_matrix(&A, n);
        allocate_matrix(&B, n);
        allocate_matrix(&C, n);

        randomize_matrix(A, n);
        randomize_matrix(B, n);
        zero_matrix(C, n);

        // Flatten matrices for MPI communication
        flat_A = (double *)malloc(n * n * sizeof(double));
        flat_C = (double *)malloc(n * n * sizeof(double));

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                flat_A[i * n + j] = A[i][j];
                flat_B[i * n + j] = B[i][j];
            }
        }

        if (n <= 8) {
            printf("Matrix A:\n");
            print_matrix(A, n);
            printf("Matrix B:\n");
            print_matrix(B, n);
        }
    }

    // Broadcast matrix B to all processes
    MPI_Bcast(flat_B, n * n, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    // Scatter rows of matrix A to all processes
    MPI_Scatter(flat_A, local_rows * n, MPI_DOUBLE, 
                local_A, local_rows * n, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    // Start timing
    MPI_Barrier(MPI_COMM_WORLD);
    start_time = MPI_Wtime();

    // Perform local matrix multiplication
    mpi_multiply_matrices(local_A, flat_B, local_C, local_rows, n);

    // End timing
    MPI_Barrier(MPI_COMM_WORLD);
    end_time = MPI_Wtime();

    // Gather results back to master process
    MPI_Gather(local_C, local_rows * n, MPI_DOUBLE,
               flat_C, local_rows * n, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        // Convert flat result back to 2D matrix
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                C[i][j] = flat_C[i * n + j];
            }
        }

        printf("MPI matrix multiplication (n=%d, processes=%d) took %.6f seconds.\n", 
               n, size, end_time - start_time);

        if (n <= 8) {
            printf("Result C = A * B:\n");
            print_matrix(C, n);
        }

        // Cleanup master process memory
        free_matrix(A, n);
        free_matrix(B, n);
        free_matrix(C, n);
        free(flat_A);
        free(flat_C);
    }

    // Cleanup local memory
    free(local_A);
    free(local_C);
    free(flat_B);

    MPI_Finalize();
    return 0;
} 