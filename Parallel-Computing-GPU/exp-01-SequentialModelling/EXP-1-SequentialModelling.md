# Experiment 1: Sequential Matrix Multiplication

**Course:** Parallel Computing and GPU
**Platform:** macOS Terminal (native, no WSL/VMware — see adaptation notes below)

---

## 1. Objective

Implement and benchmark a naive sequential (single-threaded) matrix multiplication of two 4000×4000 matrices, to serve as the baseline for comparing against the OpenMP, MPI, and CUDA versions in later experiments.

## 2. System Info

> Fill this in with your own machine's details — run `sysctl -n machdep.cpu.brand_string` and `sysctl -n hw.ncpu` in Terminal.

| | |
|---|---|
| CPU | *e.g. Apple M2, 8 cores* |
| OS | macOS *(version)* |
| Compiler | `gcc --version` output |

## 3. Adaptation Note

The reference manual assumes Windows + WSL2 Ubuntu. macOS's Terminal is already a native Unix shell, so this experiment runs directly — no WSL, no VM, no Docker needed for this part.

## 4. Source Code

`matrix_sequential.c`:

```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 4000

int main(void) {
    // Heap-allocate — 4000*4000*8 bytes = 128MB per matrix, too big for the stack
    double *A = malloc(sizeof(double) * (size_t)N * N);
    double *B = malloc(sizeof(double) * (size_t)N * N);
    double *C = malloc(sizeof(double) * (size_t)N * N);

    if (!A || !B || !C) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }

    // Initialize A and B to 1.0, per the reference problem definition
    for (long i = 0; i < (long)N * N; i++) {
        A[i] = 1.0;
        B[i] = 1.0;
    }

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            double sum = 0.0;
            for (int k = 0; k < N; k++) {
                sum += A[i * N + k] * B[k * N + j];
            }
            C[i * N + j] = sum;
        }
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    double elapsed = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;

    printf("Sequential Matrix Multiplication (%d x %d)\n", N, N);
    printf("Execution time: %f seconds\n", elapsed);
    printf("C[0][0] = %.2f\n", C[0]);

    free(A);
    free(B);
    free(C);
    return 0;
}
```

## 5. Compilation & Execution

```bash
mkdir -p matrix_seq && cd matrix_seq
# save matrix_sequential.c here
gcc -O2 matrix_sequential.c -o matrix_sequential
./matrix_sequential
```

## 6. Output

```
Sequential Matrix Multiplication (4000 x 4000)
Execution time: <your seconds> seconds
C[0][0] = 4000.00
```

`C[0][0] = 4000.00` confirms correctness (every element of A and B is 1.0, so each dot product sums 4000 ones).

## 7. Screenshots

![Compiler version](./exp-01-sequentialmodelling/screenshots/01-compiler-version.png)
*Terminal showing `gcc --version`*

![Compile command](./exp-01-sequentialmodelling/screenshots/02-compile.png)
*Compilation with no errors*

![Program output](./exp-01-sequentialmodelling/screenshots/03-output.png)
*Execution time and `C[0][0] = 4000.00`*

## 8. Observations

> Fill in after running: your recorded execution time, and how it compares once you have the OpenMP/MPI/CUDA numbers later (this becomes your speedup baseline).

---

## Repo folder structure for this experiment

Since this file lives at `parallel-computing-and-gpu/exp-01-sequentialmodelling.md`, put its code and screenshots in a matching subfolder right next to it — that's what the image paths above point to:

```
parallel-computing-and-gpu/
├── exp-01-sequentialmodelling.md
└── exp-01-sequentialmodelling/
    ├── matrix_sequential.c
    └── screenshots/
        ├── 01-compiler-version.png
        ├── 02-compile.png
        └── 03-files.png
```

