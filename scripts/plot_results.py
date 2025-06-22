#!/usr/bin/env python3
"""
MPI Matrix Multiplication Performance Visualization
This script generates comprehensive plots from benchmark results.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import sys

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_data():
    """Load benchmark results from CSV files."""
    try:
        serial_df = pd.read_csv('results/serial_results.csv')
        mpi_df = pd.read_csv('results/mpi_results.csv')
        summary_df = pd.read_csv('results/benchmark_summary.csv')
        return serial_df, mpi_df, summary_df
    except FileNotFoundError as e:
        print(f"Error: Could not find results file: {e}")
        print("Please run './scripts/run_benchmarks.sh' first to generate results.")
        sys.exit(1)

def plot_execution_times(serial_df, mpi_df):
    """Plot execution times comparison."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Serial execution times
    serial_avg = serial_df.groupby('matrix_size')['execution_time'].mean().reset_index()
    ax1.plot(serial_avg['matrix_size'], serial_avg['execution_time'], 
             marker='o', linewidth=2, markersize=8, label='Serial')
    ax1.set_xlabel('Matrix Size')
    ax1.set_ylabel('Execution Time (seconds)')
    ax1.set_title('Serial Matrix Multiplication Performance')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # MPI execution times
    mpi_avg = mpi_df.groupby(['matrix_size', 'processes'])['execution_time'].mean().reset_index()
    for proc_count in sorted(mpi_avg['processes'].unique()):
        data = mpi_avg[mpi_avg['processes'] == proc_count]
        ax2.plot(data['matrix_size'], data['execution_time'], 
                marker='o', linewidth=2, markersize=8, label=f'{proc_count} processes')
    
    ax2.set_xlabel('Matrix Size')
    ax2.set_ylabel('Execution Time (seconds)')
    ax2.set_title('MPI Matrix Multiplication Performance')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('results/execution_times.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_speedup_efficiency(summary_df):
    """Plot speedup and efficiency metrics."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Speedup plot
    for size in sorted(summary_df['matrix_size'].unique()):
        data = summary_df[summary_df['matrix_size'] == size]
        ax1.plot(data['processes'], data['speedup'], 
                marker='o', linewidth=2, markersize=8, label=f'Size {size}')
    
    # Add ideal speedup line
    max_procs = summary_df['processes'].max()
    ideal_procs = range(1, max_procs + 1)
    ax1.plot(ideal_procs, ideal_procs, '--k', alpha=0.5, label='Ideal Speedup')
    
    ax1.set_xlabel('Number of Processes')
    ax1.set_ylabel('Speedup')
    ax1.set_title('Speedup vs Number of Processes')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Efficiency plot
    for size in sorted(summary_df['matrix_size'].unique()):
        data = summary_df[summary_df['matrix_size'] == size]
        ax2.plot(data['processes'], data['efficiency'], 
                marker='o', linewidth=2, markersize=8, label=f'Size {size}')
    
    # Add ideal efficiency line
    ax2.axhline(y=1.0, color='k', linestyle='--', alpha=0.5, label='Ideal Efficiency')
    
    ax2.set_xlabel('Number of Processes')
    ax2.set_ylabel('Efficiency')
    ax2.set_title('Efficiency vs Number of Processes')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_ylim(0, 1.1)
    
    plt.tight_layout()
    plt.savefig('results/speedup_efficiency.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_scalability_heatmap(summary_df):
    """Create a heatmap showing scalability across matrix sizes and process counts."""
    # Pivot the data for heatmap
    speedup_pivot = summary_df.pivot(index='matrix_size', columns='processes', values='speedup')
    efficiency_pivot = summary_df.pivot(index='matrix_size', columns='processes', values='efficiency')
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Speedup heatmap
    sns.heatmap(speedup_pivot, annot=True, fmt='.2f', cmap='YlOrRd', 
                ax=ax1, cbar_kws={'label': 'Speedup'})
    ax1.set_title('Speedup Heatmap')
    ax1.set_xlabel('Number of Processes')
    ax1.set_ylabel('Matrix Size')
    
    # Efficiency heatmap
    sns.heatmap(efficiency_pivot, annot=True, fmt='.2f', cmap='YlGnBu', 
                ax=ax2, cbar_kws={'label': 'Efficiency'})
    ax2.set_title('Efficiency Heatmap')
    ax2.set_xlabel('Number of Processes')
    ax2.set_ylabel('Matrix Size')
    
    plt.tight_layout()
    plt.savefig('results/scalability_heatmap.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_performance_comparison(summary_df):
    """Create a comprehensive performance comparison plot."""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create a bar plot comparing different configurations
    x_pos = np.arange(len(summary_df))
    colors = plt.cm.viridis(np.linspace(0, 1, len(summary_df['processes'].unique())))
    
    bars = ax.bar(x_pos, summary_df['speedup'], color=[colors[i % len(colors)] for i in range(len(summary_df))])
    
    # Customize the plot
    ax.set_xlabel('Configuration (Matrix Size, Processes)')
    ax.set_ylabel('Speedup')
    ax.set_title('Speedup Comparison Across All Configurations')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Create labels for x-axis
    labels = [f"({row['matrix_size']}, {row['processes']})" for _, row in summary_df.iterrows()]
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    
    # Add value labels on bars
    for bar, speedup in zip(bars, summary_df['speedup']):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{speedup:.2f}', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('results/performance_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

def generate_performance_report(serial_df, mpi_df, summary_df):
    """Generate a text-based performance report."""
    report_file = 'results/performance_report.txt'
    
    with open(report_file, 'w') as f:
        f.write("=== MPI MATRIX MULTIPLICATION PERFORMANCE REPORT ===\n\n")
        
        # Summary statistics
        f.write("SUMMARY STATISTICS:\n")
        f.write("-" * 50 + "\n")
        f.write(f"Matrix sizes tested: {sorted(summary_df['matrix_size'].unique())}\n")
        f.write(f"Process counts tested: {sorted(summary_df['processes'].unique())}\n")
        f.write(f"Total configurations: {len(summary_df)}\n\n")
        
        # Best performance metrics
        f.write("BEST PERFORMANCE METRICS:\n")
        f.write("-" * 50 + "\n")
        best_speedup = summary_df.loc[summary_df['speedup'].idxmax()]
        best_efficiency = summary_df.loc[summary_df['efficiency'].idxmax()]
        
        f.write(f"Best Speedup: {best_speedup['speedup']:.3f}x\n")
        f.write(f"  Configuration: Matrix size {best_speedup['matrix_size']}, {best_speedup['processes']} processes\n\n")
        
        f.write(f"Best Efficiency: {best_efficiency['efficiency']:.3f}\n")
        f.write(f"  Configuration: Matrix size {best_efficiency['matrix_size']}, {best_efficiency['processes']} processes\n\n")
        
        # Performance analysis by matrix size
        f.write("PERFORMANCE BY MATRIX SIZE:\n")
        f.write("-" * 50 + "\n")
        for size in sorted(summary_df['matrix_size'].unique()):
            size_data = summary_df[summary_df['matrix_size'] == size]
            f.write(f"\nMatrix Size {size}:\n")
            for _, row in size_data.iterrows():
                f.write(f"  {row['processes']} processes: {row['speedup']:.3f}x speedup, {row['efficiency']:.3f} efficiency\n")
        
        # Scalability analysis
        f.write("\nSCALABILITY ANALYSIS:\n")
        f.write("-" * 50 + "\n")
        for size in sorted(summary_df['matrix_size'].unique()):
            size_data = summary_df[summary_df['matrix_size'] == size].sort_values('processes')
            if len(size_data) > 1:
                scaling_efficiency = size_data['efficiency'].iloc[-1] / size_data['efficiency'].iloc[0]
                f.write(f"Matrix size {size}: {scaling_efficiency:.3f} scaling efficiency\n")
        
        f.write(f"\nReport generated and saved to: {report_file}\n")
    
    print(f"Performance report saved to: {report_file}")

def main():
    """Main function to generate all plots and reports."""
    print("Loading benchmark results...")
    serial_df, mpi_df, summary_df = load_data()
    
    print("Generating execution time plots...")
    plot_execution_times(serial_df, mpi_df)
    
    print("Generating speedup and efficiency plots...")
    plot_speedup_efficiency(summary_df)
    
    print("Generating scalability heatmap...")
    plot_scalability_heatmap(summary_df)
    
    print("Generating performance comparison...")
    plot_performance_comparison(summary_df)
    
    print("Generating performance report...")
    generate_performance_report(serial_df, mpi_df, summary_df)
    
    print("\nAll visualizations and reports have been generated!")
    print("Check the 'results/' directory for:")
    print("  - execution_times.png")
    print("  - speedup_efficiency.png") 
    print("  - scalability_heatmap.png")
    print("  - performance_comparison.png")
    print("  - performance_report.txt")

if __name__ == "__main__":
    main() 