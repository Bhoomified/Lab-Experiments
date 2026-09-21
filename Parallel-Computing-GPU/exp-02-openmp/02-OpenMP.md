# Experiment 02 --- OpenMP Matrix Multiplication

## Parallel Computing & GPU Lab

### Experiment Overview

This experiment implements **4000 × 4000 matrix multiplication using
OpenMP shared-memory parallelism**.

The OpenMP implementation uses multiple CPU threads to divide the outer
loop of the matrix multiplication across threads. The mathematical
computation remains the same as the sequential implementation, and the
result is verified using `C[0][0] = 4000.00`.

The experiment is adapted from the laboratory reference manual for:

> **Matrix Multiplication using Sequential, OpenMP, MPI and CUDA**

------------------------------------------------------------------------

## 1. Objective

To implement and execute matrix multiplication using **OpenMP**, compare
its execution time with the sequential CPU implementation, verify the
correctness of the result, and calculate the speedup obtained through
thread-level parallelism.

### Problem Definition

-   Matrix `A`: 4000 × 4000, all elements initialized to `1.0`
-   Matrix `B`: 4000 × 4000, all elements initialized to `1.0`
-   Matrix `C`: `A × B`
-   Expected value of every element of `C`:

``` text
C[i][j] = 1×1 + 1×1 + ... + 1×1
         = 4000.00
```

Therefore:

``` text
C[0][0] = 4000.00
```

------------------------------------------------------------------------

## 2. System / Environment

### Host System

-   Operating System: macOS
-   Architecture: Apple Silicon / ARM64
-   Compiler: Apple Clang
-   OpenMP runtime: `libomp`
-   OpenMP threads used: **8**

### Compiler Verification

The installed compiler was verified using:

``` bash
gcc --version
```

The system reports Apple Clang, targeting ARM64 macOS.

> Note: On macOS, the OpenMP program was compiled using Clang together
> with Homebrew's `libomp`, rather than the Linux/WSL GCC setup
> described in the reference manual.

------------------------------------------------------------------------

## 3. OpenMP Setup

### 3.1 CPU Verification

The number of logical and physical CPU cores was checked using macOS
commands:

``` bash
sysctl -n hw.logicalcpu
sysctl -n hw.physicalcpu
```

This was used to determine the CPU resources available to the OpenMP
runtime.

### 3.2 OpenMP Runtime Installation

OpenMP support was installed using Homebrew:

``` bash
brew install libomp
```

The installation location was verified using:

``` bash
brew --prefix libomp
```

### 3.3 Thread Configuration

Eight OpenMP threads were requested:

``` bash
export OMP_NUM_THREADS=8
```

The setting was verified using:

``` bash
echo $OMP_NUM_THREADS
```

Expected output:

``` text
8
```

------------------------------------------------------------------------

## 4. Working Directory

The OpenMP experiment was maintained separately from the sequential
implementation.

Directory creation:

``` bash
mkdir -p ~/parallel_lab/openmp
cd ~/parallel_lab/openmp
```

The main source and executable are:

``` text
matrix_openmp.c
matrix_openmp
```

------------------------------------------------------------------------

## 5. OpenMP Source Code

### `matrix_openmp.c`

``` c
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define N 4000

int main()
{
    int i, j, k;
    double *A, *B, *C;
    double start, end;

    A = (double *)malloc(N * N * sizeof(double));
    B = (double *)malloc(N * N * sizeof(double));
    C = (double *)malloc(N * N * sizeof(double));

    if (A == NULL || B == NULL || C == NULL)
    {
        printf("Memory allocation failed\n");
        return 1;
    }

    for (i = 0; i < N; i++)
    {
        for (j = 0; j < N; j++)
        {
            A[i * N + j] = 1.0;
            B[i * N + j] = 1.0;
            C[i * N + j] = 0.0;
        }
    }

    start = omp_get_wtime();

    #pragma omp parallel for private(j, k)
    for (i = 0; i < N; i++)
    {
        for (j = 0; j < N; j++)
        {
            for (k = 0; k < N; k++)
            {
                C[i * N + j] +=
                    A[i * N + k] *
                    B[k * N + j];
            }
        }
    }

    end = omp_get_wtime();

    printf("OpenMP Matrix Multiplication Completed\n");
    printf("Matrix Size = %d x %d\n", N, N);
    printf("Number of Threads Used = %d\n", omp_get_max_threads());
    printf("Execution Time = %f seconds\n", end - start);
    printf("Verification C[0][0] = %.2f\n", C[0]);

    free(A);
    free(B);
    free(C);

    return 0;
}
```

------------------------------------------------------------------------

## 6. Important OpenMP Components

### OpenMP Header

``` c
#include <omp.h>
```

Provides the OpenMP functions and runtime interface.

### Parallel Loop

``` c
#pragma omp parallel for private(j, k)
```

This divides the iterations of the outer `i` loop among multiple OpenMP
threads.

### OpenMP Timing

``` c
start = omp_get_wtime();
```

and:

``` c
end = omp_get_wtime();
```

The difference gives the OpenMP computation time.

### Thread Count

``` c
omp_get_max_threads()
```

reports the maximum number of OpenMP threads available according to the
runtime configuration.

------------------------------------------------------------------------

## 7. Compilation

Because the experiment was performed on macOS using Apple Silicon,
OpenMP was compiled using Clang and Homebrew's `libomp`.

### Compilation Command

``` bash
clang -O2 -Xpreprocessor -fopenmp \
-I/opt/homebrew/opt/libomp/include \
-L/opt/homebrew/opt/libomp/lib \
-lomp \
matrix_openmp.c \
-o matrix_openmp
```

### Explanation

-   `clang` --- Apple Clang compiler
-   `-O2` --- enables compiler optimization
-   `-Xpreprocessor -fopenmp` --- enables OpenMP preprocessing
-   `-I.../include` --- locates OpenMP header files
-   `-L.../lib` --- locates the OpenMP library
-   `-lomp` --- links the OpenMP runtime
-   `matrix_openmp.c` --- source file
-   `-o matrix_openmp` --- generated executable

Compilation completed successfully.

------------------------------------------------------------------------

## 8. Executable Verification

The generated files were checked using:

``` bash
ls -lh
```

Expected project files:

``` text
matrix_openmp.c
matrix_openmp
```

The executable was successfully created and used for the experiment.

------------------------------------------------------------------------

## 9. OpenMP Execution

The program was executed using:

``` bash
./matrix_openmp
```

The OpenMP runtime was configured for eight threads.

### Actual Execution Output

``` text
OpenMP Matrix Multiplication Completed

Matrix Size = 4000 x 4000

Number of Threads Used = 8

Execution Time = 82.747345 seconds

Verification C[0][0] = 4000.00
```

------------------------------------------------------------------------

## 10. CPU Utilization Monitoring

CPU utilization was monitored using `htop` while the OpenMP matrix
multiplication was running.

Command:

``` bash
htop
```

This provided a visual indication of CPU activity during the
multi-threaded computation.

------------------------------------------------------------------------

## 11. Sequential Baseline

The OpenMP speedup was calculated using the actual sequential execution
time obtained on the same Mac system.

### Sequential Result

``` text
Matrix Size = 4000 x 4000
Execution Time = 246.610556 seconds
C[0][0] = 4000.00
```

### OpenMP Result

``` text
Matrix Size = 4000 x 4000
Number of Threads Used = 8
Execution Time = 82.747345 seconds
C[0][0] = 4000.00
```

------------------------------------------------------------------------

## 12. Speedup Calculation

The speedup formula is:

``` text
Speedup = Sequential Execution Time / OpenMP Execution Time
```

Using the actual measured values:

``` text
Speedup = 246.610556 / 82.747345
        ≈ 2.98×
```

### Result

**OpenMP Speedup = 2.98×**

This means that, for this particular 4000 × 4000 workload on the tested
Mac system, the measured OpenMP execution time was approximately
one-third of the measured sequential execution time.

------------------------------------------------------------------------

## 13. Performance Comparison

  Implementation     Execution Time Resources                Verification   Speedup
  ---------------- ---------------- ---------------------- -------------- ---------
  Sequential           246.610556 s Single CPU execution          4000.00     1.00×
  OpenMP                82.747345 s 8 CPU threads                 4000.00     2.98×

All implementations produced the expected verification value:

``` text
C[0][0] = 4000.00
```

------------------------------------------------------------------------

## 14. Why OpenMP Is Faster

The sequential implementation performs the matrix multiplication using
one CPU execution flow.

OpenMP introduces thread-level parallelism by distributing iterations of
the outer matrix row loop across multiple CPU threads.

Conceptually:

``` text
Sequential:

i = 0
i = 1
i = 2
...
i = 3999
        ↓
one execution flow
```

With OpenMP:

``` text
                 4000 rows
                     │
          ┌──────────┼──────────┐
          ↓          ↓          ↓
       Thread 1   Thread 2   ... Thread 8
          │          │             │
        rows       rows          rows
          └──────────┼─────────────┘
                     ↓
                  Matrix C
```

The matrices remain in shared memory while different threads process
different outer-loop iterations.

------------------------------------------------------------------------

## 15. Verification

The correctness of the multiplication was verified using:

``` text
C[0][0] = 4000.00
```

Since every element of both input matrices is `1.0`, each output element
is the sum of 4000 products of `1.0 × 1.0`.

Therefore:

``` text
C[0][0] = 4000.00
```

The expected result was obtained successfully.

------------------------------------------------------------------------

## 16. Screenshots

All screenshots for this experiment are stored inside:

``` text
exp-02-openmp/screenshots/
```

### Screenshot List

  --------------------------------------------------------------------------------
                           No. Filename                      Description
  ---------------------------- ----------------------------- ---------------------
                            01 `01_cpu_verification.png`     CPU resource
                                                             verification

                            02 `02_openmp_threads.png`       `OMP_NUM_THREADS=8`
                                                             configuration

                            03 `03_openmp_source_code.png`   OpenMP source code

                            04 `04_openmp_compilation.png`   Successful
                                                             compilation and
                                                             executable creation

                            05 `05_htop_cpu_usage.png`       CPU utilization
                                                             during OpenMP
                                                             execution

                            06 `06_openmp_result.png`        Final OpenMP
                                                             execution result

                            07 `07_openmp_files.png`         OpenMP source and
                                                             executable files
  --------------------------------------------------------------------------------

------------------------------------------------------------------------

## 17. Experiment Workflow

``` text
CPU Verification
       ↓
OpenMP Runtime Setup
       ↓
Set OMP_NUM_THREADS = 8
       ↓
Create OpenMP Source
       ↓
Compile with OpenMP Support
       ↓
Execute 4000 × 4000 Matrix Multiplication
       ↓
Monitor CPU Utilization
       ↓
Verify C[0][0] = 4000.00
       ↓
Record Execution Time
       ↓
Compare with Sequential Baseline
       ↓
Calculate Speedup
```

------------------------------------------------------------------------

## 18. Final Result

### OpenMP Matrix Multiplication

``` text
Matrix Size          : 4000 × 4000
Number of Threads    : 8
Execution Time       : 82.747345 seconds
Verification         : C[0][0] = 4000.00
Speedup              : 2.98×
```

### Conclusion

The 4000 × 4000 matrix multiplication was successfully implemented using
OpenMP shared-memory parallelism on an Apple Silicon Mac. Eight OpenMP
threads were used to parallelize the outer matrix-multiplication loop.
The program completed successfully with the expected verification value
of `4000.00`.

Compared with the measured sequential execution time of `246.610556`
seconds, the OpenMP implementation required `82.747345` seconds and
achieved a measured speedup of approximately `2.98×`.

------------------------------------------------------------------------

## 19. Reference

**Laboratory Manual:**\
*Matrix Multiplication using Sequential, OpenMP, MPI and CUDA*

The manual defines the 4000 × 4000 workload, OpenMP implementation,
thread configuration, execution workflow, verification method,
screenshot requirements, and speedup formula used in this experiment.
