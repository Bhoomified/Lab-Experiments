# Experiment 5: Neural Network Layers in CUDA

## Overview

This experiment implements basic neural-network operations using custom CUDA kernels and compares their execution on the CPU and GPU.

The implementation consists of three operations:

- **Matrix Multiplication with Bias:** Computes weighted sums and adds bias.
- **ReLU:** Converts negative values to zero.
- **Sigmoid:** Maps values to a range between 0 and 1.

These operations are combined into a two-layer neural-network forward pass. The experiment evaluates numerical correctness and compares CPU and GPU execution times.

**Note:** This experiment performs forward propagation only. It does not involve model training or backpropagation.

## Network Architecture

The forward pass follows these steps:

```text
Input (256 × 128)
       |
Matrix Multiplication + Bias
       |
      ReLU
       |
Hidden Layer (256 × 64)
       |
Matrix Multiplication + Bias
       |
    Sigmoid
       |
Output (256 × 10)
```

### Network Configuration

| Parameter | Value |
|---|---:|
| Batch Size | 256 |
| Input Size | 128 |
| Hidden Layer Size | 64 |
| Output Size | 10 |
| Repetitions | 20 |

## Technologies Used

- C++ and CUDA
- NVIDIA CUDA Toolkit 13.4
- Microsoft Visual Studio Build Tools
- Windows
- NVIDIA RTX 4500 Ada Generation GPU

## Execution

Compile the program using the x64 Developer Command Prompt:

```cmd
nvcc -O2 neural_network.cu -o neural_network.exe
```

Run the executable:

```cmd
neural_network.exe
```

## Kernel Validation

Each CUDA kernel is tested independently using predefined inputs and expected outputs.

| Kernel | Expected Result |
|---|---|
| Matrix Multiplication + Bias | [[23, 27], [50, 63]] |
| ReLU | [0, 0, 3, 0, 5] |
| Sigmoid | [0.119203, 0.5, 0.880797] |

**Observed Result:** All three kernel tests passed.

## Experimental Results

The following values were recorded during execution on the NVIDIA RTX 4500 Ada Generation GPU.

### Performance Comparison

| Measurement | Run 1 | Run 2 |
|---|---:|---:|
| CPU Compute Time (ms) | 0.722240 | 0.720380 |
| GPU Kernel-only Time (ms) | 0.019654 | 0.042842 |
| GPU End-to-end Time (ms) | 0.066055 | 0.179115 |
| Kernel-only Speedup | 36.746987× | 16.814964× |
| End-to-end Speedup | 10.933919× | 4.021885× |

### Output Validation

| Validation | Result |
|---|---|
| Matrix Multiplication | PASSED |
| ReLU | PASSED |
| Sigmoid | PASSED |
| Maximum Absolute Difference | 0.000000 |
| CPU and GPU Outputs | MATCH |

The first ten GPU output values were:

```text
0.498196 0.503101 0.508006 0.512911 0.517814
0.497729 0.502638 0.507548 0.512457 0.517364
```

### Timing Methodology

- **CPU Time:** Average execution time of 20 CPU forward passes.
- **GPU Kernel-only Time:** Measures kernel execution using CUDA events, with input data already on the GPU.
- **GPU End-to-end Time:** Includes memory transfers, kernel execution, synchronization and output transfer.

Speedup is calculated as:

```text
Kernel-only Speedup = CPU Time / GPU Kernel-only Time

End-to-end Speedup = CPU Time / GPU End-to-end Time
```

Timing differences between runs are expected due to system and GPU execution conditions.

## Conclusion

The experiment successfully implemented matrix multiplication with bias, ReLU and sigmoid using CUDA kernels. The operations were combined into a two-layer neural-network forward pass and evaluated against a CPU implementation.

All kernel tests passed, and CPU and GPU outputs matched within the specified tolerance. Execution times were measured to evaluate kernel-only and end-to-end GPU speedup.
