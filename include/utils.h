#ifndef UTILS_H
#define UTILS_H

void allocate_matrix(double ***matrix, int n);
void free_matrix(double **matrix, int n);
void randomize_matrix(double **matrix, int n);
void zero_matrix(double **matrix, int n);
void print_matrix(double **matrix, int n);

#endif // UTILS_H 