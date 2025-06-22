#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "../include/utils.h"

void allocate_matrix(double ***matrix, int n) {
    *matrix = (double **)malloc(n * sizeof(double *));
    for (int i = 0; i < n; i++) {
        (*matrix)[i] = (double *)malloc(n * sizeof(double));
    }
}

void free_matrix(double **matrix, int n) {
    for (int i = 0; i < n; i++) {
        free(matrix[i]);
    }
    free(matrix);
}

void randomize_matrix(double **matrix, int n) {
    srand(time(NULL));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            matrix[i][j] = (double)(rand() % 100);
        }
    }
}

void zero_matrix(double **matrix, int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            matrix[i][j] = 0.0;
        }
    }
}

void print_matrix(double **matrix, int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            printf("%6.2f ", matrix[i][j]);
        }
        printf("\n");
    }
} 