# MPI Distributed Matrix Multiplication

This project implements and evaluates the performance of matrix multiplication across multiple nodes using MPI.
## Project Overview

The project includes:
- **Serial Matrix Multiplication**: Baseline implementation for comparison
- **MPI Distributed Matrix Multiplication**: Parallel implementation using MPI
- **Performance Metrics**: Execution time and scalability measurements
- **Benchmarking Tools**: Automated testing and comparison utilities
- **Documentation**: Comprehensive analysis and results

## Project Structure

```
.
├── src/
│   ├── serial_matrix_mult.c      # Serial implementation
│   ├── mpi_matrix_mult.c         # MPI distributed implementation
│   └── utils.c                   # Utility functions
├── include/
│   └── utils.h                   # Header file for utilities
├── scripts/
│   ├── run_benchmarks.sh         # Benchmarking script
│   └── plot_results.py           # Performance visualization
├── results/                      # Benchmark results and plots
├── Makefile                      # Build configuration
├── requirements.txt              # Python dependencies for plotting
└── README.md                     # This file
```

## Prerequisites

### MPI Installation

#### On macOS:
```bash
brew install open-mpi
```

#### On Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install openmpi-bin libopenmpi-dev
```

#### On CentOS/RHEL:
```bash
sudo yum install openmpi openmpi-devel
```

### Python Dependencies (for plotting)
```bash
pip install -r requirements.txt
```

## Building the Project

```bash
make clean
make all
```

## Usage

### Serial Matrix Multiplication
```bash
./serial_matrix_mult <matrix_size>
```

### MPI Distributed Matrix Multiplication
```bash
mpirun -np <number_of_processes> ./mpi_matrix_mult <matrix_size>
```

### Running Benchmarks
```bash
./scripts/run_benchmarks.sh
```

### Generating Performance Plots
```bash
python scripts/plot_results.py
```

## Algorithm Details

### Serial Implementation
- Standard O(n³) matrix multiplication algorithm
- Used as baseline for performance comparison

### MPI Distributed Implementation
- **Data Partitioning**: Matrices are distributed across processes using block distribution
- **Communication Pattern**: 
  - Process 0 distributes matrix data to all processes
  - Each process computes its assigned portion
  - Results are gathered back to process 0
- **Load Balancing**: Ensures even distribution of computational load

## Performance Metrics

The system measures:
- **Execution Time**: Wall-clock time for computation
- **Speedup**: Ratio of serial time to parallel time
- **Efficiency**: Speedup divided by number of processes
- **Scalability**: Performance across different process counts

## Expected Results

- **Speedup**: Should approach linear speedup for large matrices
- **Efficiency**: May decrease with more processes due to communication overhead
- **Scalability**: Performance gains diminish with very large process counts

## Troubleshooting

### Common Issues:
1. **MPI not found**: Ensure MPI is properly installed and in PATH
2. **Permission denied**: Check file permissions for execution
3. **Memory issues**: Reduce matrix size for limited memory systems

### Debug Mode:
```bash
make debug
mpirun -np 4 ./mpi_matrix_mult_debug 100
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License. 