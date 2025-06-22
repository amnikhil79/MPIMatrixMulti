CC = gcc
MPICC = mpicc
CFLAGS = -O2 -Wall -Iinclude
LDFLAGS =

SRC_DIR = src
BIN_DIR = .

SERIAL_SRC = $(SRC_DIR)/serial_matrix_mult.c $(SRC_DIR)/utils.c
SERIAL_BIN = $(BIN_DIR)/serial_matrix_mult

MPI_SRC = $(SRC_DIR)/mpi_matrix_mult.c $(SRC_DIR)/utils.c
MPI_BIN = $(BIN_DIR)/mpi_matrix_mult

all: $(SERIAL_BIN) $(MPI_BIN)

$(SERIAL_BIN): $(SERIAL_SRC)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

$(MPI_BIN): $(MPI_SRC)
	$(MPICC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

clean:
	rm -f $(SERIAL_BIN) $(MPI_BIN) *.o

.PHONY: all clean 