::: {align="center"}
# ⚡ Neural Network Layers in CUDA

### Experiment 5 · CUDA Programming Laboratory

**A two-layer neural-network forward pass implemented with custom CUDA
kernels**

`<br>`{=html}

![CUDA](https://img.shields.io/badge/CUDA-13.4-76B900?logo=nvidia)
![C++](https://img.shields.io/badge/C%2B%2B-MSVC-00599C?logo=cplusplus)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D4?logo=windows)
![GPU](https://img.shields.io/badge/GPU-RTX%204500%20Ada-76B900?logo=nvidia)
:::

------------------------------------------------------------------------

## 📌 Project Overview

This experiment implements and evaluates three fundamental
neural-network operations using **custom CUDA kernels**:

-   **Matrix multiplication with bias** --- computes weighted sums and
    adds the bias vector.
-   **ReLU activation** --- replaces negative values with zero.
-   **Sigmoid activation** --- maps values into the range 0 to 1.

The same two-layer forward pass is executed on both the **CPU and GPU**.
Their outputs are compared for numerical correctness, and their
execution times are measured to calculate speedup.

> **Scope:** This is forward propagation (inference) only. It does not
> train the network and does not implement loss calculation, an
> optimizer, or backpropagation.

## 🎯 Aim

To implement basic neural-network layers using CUDA, compare CPU and GPU
execution, validate numerical correctness, measure execution time, and
calculate GPU speedup.

## 🧠 How It Works

The network performs the following operations in sequence:

``` text
             INPUT
          X: 256 × 128
                │
                ▼
      Matrix Multiplication
           X × W1 + b1
                │
                ▼
              ReLU
                │
                ▼
         HIDDEN LAYER
          256 × 64
                │
                ▼
      Matrix Multiplication
           A1 × W2 + b2
                │
                ▼
             Sigmoid
                │
                ▼
             OUTPUT
           256 × 10
```

### Forward-pass equations

**Layer 1**

`Z1 = X × W1 + b1`

`A1 = ReLU(Z1)`

**Layer 2**

`Z2 = A1 × W2 + b2`

`Y = Sigmoid(Z2)`

### CUDA kernel execution

Each CUDA thread computes one output element for matrix multiplication,
or processes one element for an activation function. The GPU kernels are
launched in sequence so that each operation receives the previous
operation's output.

## ⚙️ Network Configuration

  Parameter                           Value
  --------------------------- -------------
  Batch size                            256
  Input size                            128
  Hidden layer size                      64
  Output size                            10
  Repetitions for timing                 20
  Input tensor                    256 × 128
  First weight matrix (W1)         128 × 64
  First bias (b1)               64 elements
  Second weight matrix (W2)         64 × 10
  Second bias (b2)              10 elements
  Final output                     256 × 10

Inputs and weights are generated using deterministic sine and cosine
functions. This ensures that the CPU and GPU use identical data for
comparison.

## 🛠️ Technologies & Environment

  -----------------------------------------------------------------------
  Component                           Environment used
  ----------------------------------- -----------------------------------
  Programming language                C++ with CUDA

  CUDA Toolkit                        13.4

  CUDA compiler                       NVIDIA `nvcc`

  C++ compiler                        Microsoft MSVC 19.52 (x64)

  Operating system                    Windows

  GPU                                 NVIDIA RTX 4500 Ada Generation

  Build environment                   Visual Studio Build Tools, x64
                                      Developer Command Prompt
  -----------------------------------------------------------------------

## 📂 Project Structure

``` text
Experiment5_CUDA/
│
├── neural_network.cu       # CUDA source code
├── neural_network.exe      # Compiled executable (generated)
├── screenshots/            # Execution and validation evidence
│   ├── 01_CUDA_Environment.png
│   ├── 02_Compilation_Success.png
│   ├── 03_Kernel_Validation.png
│   ├── 04_Forward_Pass_Results.png
│   ├── 05_CPU_GPU_Comparison.png
│   └── 06_Repeated_Run_Results.png
│
└── README.md
```

*The executable is generated during compilation. It does not need to be
committed if your repository policy excludes build artifacts.*

## 🚀 Build & Run

Run these commands from an **x64 Developer Command Prompt for Visual
Studio**, inside the project directory.

### 1. Verify the CUDA environment

``` cmd
nvidia-smi
nvcc --version
where cl
```

Make sure `where cl` shows the x64 compiler path (`Hostx64\x64\cl.exe`).

### 2. Compile

``` cmd
nvcc -O2 neural_network.cu -o neural_network.exe
```

### 3. Execute

``` cmd
neural_network.exe
```

## ✅ Validation

The program tests the three CUDA kernels independently using small
inputs with known expected outputs.

  -----------------------------------------------------------------------------
  Kernel                  Validation input        Expected result
  ----------------------- ----------------------- -----------------------------
  Matrix multiplication + A 2×3, B 3×2, bias      `[[23, 27], [50, 63]]`
  bias                    `[1, -1]`               

  ReLU                    `[-2, 0, 3, -4, 5]`     `[0, 0, 3, 0, 5]`

  Sigmoid                 `[-2, 0, 2]`            Approximately
                                                  `[0.119203, 0.5, 0.880797]`
  -----------------------------------------------------------------------------

**Observed validation:** all three kernel tests passed in both recorded
runs. The maximum absolute CPU/GPU output difference was `0.000000`, and
the program reported `MATCH (within tolerance)`.

## 📊 Experimental Results

The following measurements are from the actual executions recorded
during this experiment. Timing values can vary between runs due to
system load and GPU execution conditions.

### Run 1

  Measurement                            Observed result
  ------------------------------------ -----------------
  Average CPU compute time                   0.722240 ms
  Average GPU kernel-only time               0.019654 ms
  Average GPU end-to-end time                0.066055 ms
  Kernel-only speedup                         36.746987×
  End-to-end speedup                          10.933919×
  Maximum absolute output difference            0.000000
  CPU/GPU output validation                        MATCH

### Run 2

  Measurement                            Observed result
  ------------------------------------ -----------------
  Average CPU compute time                   0.720380 ms
  Average GPU kernel-only time               0.042842 ms
  Average GPU end-to-end time                0.179115 ms
  Kernel-only speedup                         16.814964×
  End-to-end speedup                           4.021885×
  Maximum absolute output difference            0.000000
  CPU/GPU output validation                        MATCH

### Timing comparison

  Metric                        Run 1         Run 2
  --------------------- ------------- -------------
  CPU compute             0.722240 ms   0.720380 ms
  GPU kernel-only         0.019654 ms   0.042842 ms
  GPU end-to-end          0.066055 ms   0.179115 ms
  Kernel-only speedup      36.746987×    16.814964×
  End-to-end speedup       10.933919×     4.021885×

**Run 3:** Pending. Add its measured values after the third execution;
do not substitute the manual's reference timings.

### Understanding the two GPU timings

-   **Kernel-only time:** measures repeated GPU kernel execution when
    inputs and weights are already in device memory. CUDA events are
    used for this measurement.
-   **End-to-end time:** includes host-to-device data transfers, kernel
    execution, synchronization, and the device-to-host output transfer.

End-to-end time is therefore expected to be greater than kernel-only
time. Transfer and launch overhead can reduce the end-to-end speedup.

### Speedup calculations

`Kernel-only speedup = CPU average time ÷ GPU kernel-only time`

`End-to-end speedup = CPU average time ÷ GPU end-to-end time`

A speedup greater than 1 indicates that the GPU measurement is faster
than the CPU measurement for that scope.

## 🔍 Output Consistency

The program uses fixed input and weight-generation formulas, so the
first ten output values are expected to remain the same across runs:

``` text
0.498196  0.503101  0.508006  0.512911  0.517814
0.497729  0.502638  0.507548  0.512457  0.517364
```

The CPU and GPU outputs are considered a match when the maximum absolute
difference is below `1e-4`.

## 📸 Execution Evidence

The `screenshots/` directory contains the environment, compilation,
kernel validation, forward-pass measurements, CPU/GPU comparison, and
repeated-run evidence.

## 📝 Key Takeaways

-   Implemented matrix multiplication with bias, ReLU, and sigmoid as
    CUDA kernels.
-   Combined the kernels into a two-layer neural-network forward pass.
-   Executed an equivalent forward pass on the CPU for comparison.
-   Used GPU memory allocation and host/device data transfers.
-   Measured kernel-only and end-to-end execution times.
-   Validated numerical agreement between CPU and GPU outputs.

## 🏁 Conclusion

Custom CUDA kernels for matrix multiplication with bias, ReLU, and
sigmoid were implemented and tested, then combined into a two-layer
neural-network forward pass. CPU and GPU outputs were compared for
numerical correctness, and execution times were measured to calculate
kernel-only and end-to-end speedups. In the two recorded executions, all
kernel tests passed and the CPU and GPU outputs matched within the
specified tolerance.

------------------------------------------------------------------------

::: {align="center"}
**Experiment 5 · Neural Network Layers in CUDA**

*CUDA Programming Laboratory*
:::
