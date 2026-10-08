/*
 * Parallel Vector Addition using OpenMP
 * Computes C[i] = A[i] + B[i] for large vectors, sequentially and in parallel,
 * verifies the result, and prints timings as CSV.
 *
 * Build:  gcc -O2 -fopenmp src/vector_add.c -o vector_add
 * Run:    ./vector_add <N> <threads> [repeats]
 * Output: N,threads,seq_time_s,par_time_s,speedup,efficiency
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>

/* Sequential version: one thread walks the whole array */
static void vec_add_seq(const double *A, const double *B, double *C, long n) {
    for (long i = 0; i < n; i++)
        C[i] = A[i] + B[i];
}

/* Parallel version: OpenMP splits the loop iterations among threads.
 * schedule(static) gives each thread one contiguous chunk of ~n/p elements,
 * which is ideal here because every iteration costs the same. */
static void vec_add_par(const double *A, const double *B, double *C, long n) {
    #pragma omp parallel for schedule(static)
    for (long i = 0; i < n; i++)
        C[i] = A[i] + B[i];
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <N> <threads> [repeats]\n", argv[0]);
        return 1;
    }
    long n      = atol(argv[1]);
    int threads = atoi(argv[2]);
    int repeats = (argc > 3) ? atoi(argv[3]) : 5;

    double *A  = malloc(n * sizeof(double));
    double *B  = malloc(n * sizeof(double));
    double *Cs = malloc(n * sizeof(double));   /* sequential result */
    double *Cp = malloc(n * sizeof(double));   /* parallel result   */
    if (!A || !B || !Cs || !Cp) { fprintf(stderr, "malloc failed\n"); return 1; }

    omp_set_num_threads(threads);

    /* Initialise in parallel (first-touch: pages land near the thread that uses them) */
    #pragma omp parallel for schedule(static)
    for (long i = 0; i < n; i++) {
        A[i] = (double)(i % 1000) * 0.5;
        B[i] = (double)(i % 777) * 1.5;
        Cs[i] = 0.0; Cp[i] = 0.0;
    }

    /* Warm-up runs (not timed) */
    vec_add_seq(A, B, Cs, n);
    vec_add_par(A, B, Cp, n);

    /* Time each version: best of 'repeats' runs to reduce noise */
    double best_seq = 1e30, best_par = 1e30;
    for (int r = 0; r < repeats; r++) {
        double t0 = omp_get_wtime();
        vec_add_seq(A, B, Cs, n);
        double t1 = omp_get_wtime();
        vec_add_par(A, B, Cp, n);
        double t2 = omp_get_wtime();
        if (t1 - t0 < best_seq) best_seq = t1 - t0;
        if (t2 - t1 < best_par) best_par = t2 - t1;
    }

    /* Verify parallel result matches sequential result */
    for (long i = 0; i < n; i++) {
        if (fabs(Cs[i] - Cp[i]) > 1e-9) {
            fprintf(stderr, "Mismatch at %ld: %f vs %f\n", i, Cs[i], Cp[i]);
            return 2;
        }
    }

    double speedup    = best_seq / best_par;
    double efficiency = speedup / threads;
    printf("%ld,%d,%.6f,%.6f,%.3f,%.3f\n", n, threads, best_seq, best_par, speedup, efficiency);

    free(A); free(B); free(Cs); free(Cp);
    return 0;
}
