#!/bin/bash

# MPI Matrix Multiplication Benchmarking Script
# This script runs comprehensive benchmarks and saves results to CSV files

# Create results directory if it doesn't exist
mkdir -p results

# Define test parameters
MATRIX_SIZES=(100 200 400 500)
PROCESS_COUNTS=(1 2 4)
ITERATIONS=2  # Number of iterations per test for averaging

# Output files
SERIAL_RESULTS="results/serial_results.csv"
MPI_RESULTS="results/mpi_results.csv"
SUMMARY_RESULTS="results/benchmark_summary.csv"

echo "Starting MPI Matrix Multiplication Benchmarks..."
echo "Matrix sizes: ${MATRIX_SIZES[@]}"
echo "Process counts: ${PROCESS_COUNTS[@]}"
echo "Iterations per test: $ITERATIONS"
echo ""

# Initialize CSV files with headers
echo "matrix_size,execution_time,iteration" > $SERIAL_RESULTS
echo "matrix_size,processes,execution_time,iteration" > $MPI_RESULTS
echo "matrix_size,processes,avg_time,speedup,efficiency" > $SUMMARY_RESULTS

# Function to extract execution time from output
extract_time() {
    echo "$1" | grep -o '[0-9]\+\.[0-9]\+' | tail -1
}

# Function to run serial benchmarks
run_serial_benchmarks() {
    echo "Running serial benchmarks..."
    for size in "${MATRIX_SIZES[@]}"; do
        echo "  Testing matrix size: $size"
        total_time=0
        
        for iter in $(seq 1 $ITERATIONS); do
            echo -n "    Iteration $iter... "
            output=$(./serial_matrix_mult $size 2>&1)
            time=$(extract_time "$output")
            echo "$size,$time,$iter" >> $SERIAL_RESULTS
            total_time=$(echo "$total_time + $time" | bc -l)
            echo "${time}s"
        done
        
        avg_time=$(echo "scale=6; $total_time / $ITERATIONS" | bc -l)
        echo "    Average: ${avg_time}s"
        echo ""
    done
}

# Function to run MPI benchmarks
run_mpi_benchmarks() {
    echo "Running MPI benchmarks..."
    for size in "${MATRIX_SIZES[@]}"; do
        # Check if matrix size is divisible by all process counts
        skip_size=false
        for procs in "${PROCESS_COUNTS[@]}"; do
            if [ $((size % procs)) -ne 0 ]; then
                echo "  Skipping matrix size $size (not divisible by $procs processes)"
                skip_size=true
                break
            fi
        done
        
        if [ "$skip_size" = true ]; then
            continue
        fi
        
        echo "  Testing matrix size: $size"
        
        for procs in "${PROCESS_COUNTS[@]}"; do
            echo "    Testing with $procs processes"
            total_time=0
            
            for iter in $(seq 1 $ITERATIONS); do
                echo -n "      Iteration $iter... "
                output=$(mpirun -np $procs ./mpi_matrix_mult $size 2>&1)
                time=$(extract_time "$output")
                echo "$size,$procs,$time,$iter" >> $MPI_RESULTS
                total_time=$(echo "$total_time + $time" | bc -l)
                echo "${time}s"
            done
            
            avg_time=$(echo "scale=6; $total_time / $ITERATIONS" | bc -l)
            echo "      Average: ${avg_time}s"
        done
        echo ""
    done
}

# Function to calculate speedup and efficiency
calculate_metrics() {
    echo "Calculating performance metrics..."
    
    # Calculate average serial times for each matrix size
    for size in "${MATRIX_SIZES[@]}"; do
        total_time=0
        count=0
        while IFS=',' read -r s t i; do
            if [[ $s == $size ]]; then
                total_time=$(echo "$total_time + $t" | bc -l)
                ((count++))
            fi
        done < <(tail -n +2 $SERIAL_RESULTS)
        
        if [[ $count -gt 0 ]]; then
            avg_serial_time=$(echo "scale=6; $total_time / $count" | bc -l)
            
            # Calculate metrics for each MPI configuration
            for procs in "${PROCESS_COUNTS[@]}"; do
                total_mpi_time=0
                mpi_count=0
                while IFS=',' read -r s p t i; do
                    if [[ $s == $size && $p == $procs ]]; then
                        total_mpi_time=$(echo "$total_mpi_time + $t" | bc -l)
                        ((mpi_count++))
                    fi
                done < <(tail -n +2 $MPI_RESULTS)
                
                if [[ $mpi_count -gt 0 ]]; then
                    avg_mpi_time=$(echo "scale=6; $total_mpi_time / $mpi_count" | bc -l)
                    speedup=$(echo "scale=3; $avg_serial_time / $avg_mpi_time" | bc -l)
                    efficiency=$(echo "scale=3; $speedup / $procs" | bc -l)
                    echo "$size,$procs,$avg_mpi_time,$speedup,$efficiency" >> $SUMMARY_RESULTS
                fi
            done
        fi
    done
}

# Function to display summary
display_summary() {
    echo ""
    echo "=== BENCHMARK SUMMARY ==="
    echo ""
    printf "%-12s %-10s %-12s %-10s %-12s\n" "Matrix Size" "Processes" "Time (s)" "Speedup" "Efficiency"
    printf "%-12s %-10s %-12s %-10s %-12s\n" "----------" "---------" "--------" "-------" "----------"
    
    tail -n +2 $SUMMARY_RESULTS | while IFS=',' read -r size procs time speedup efficiency; do
        printf "%-12s %-10s %-12s %-10s %-12s\n" "$size" "$procs" "$time" "$speedup" "$efficiency"
    done
    
    echo ""
    echo "Results saved to:"
    echo "  - Serial results: $SERIAL_RESULTS"
    echo "  - MPI results: $MPI_RESULTS"
    echo "  - Summary: $SUMMARY_RESULTS"
    echo ""
    echo "To generate plots, run: python scripts/plot_results.py"
}

# Main execution
main() {
    # Check if executables exist
    if [[ ! -f "./serial_matrix_mult" ]]; then
        echo "Error: serial_matrix_mult not found. Please run 'make' first."
        exit 1
    fi
    
    if [[ ! -f "./mpi_matrix_mult" ]]; then
        echo "Error: mpi_matrix_mult not found. Please run 'make' first."
        exit 1
    fi
    
    # Check if bc is available for calculations
    if ! command -v bc &> /dev/null; then
        echo "Error: 'bc' calculator not found. Please install it."
        exit 1
    fi
    
    start_time=$(date +%s)
    
    run_serial_benchmarks
    run_mpi_benchmarks
    calculate_metrics
    display_summary
    
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    echo "Total benchmark time: ${duration} seconds"
}

# Run the main function
main "$@" 