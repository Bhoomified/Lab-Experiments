#!/bin/bash
# Runs the vector-addition benchmark for every (size, threads) combination
# and writes all results to results/results.csv
set -e
mkdir -p results
gcc-16 -O2 -fopenmp src/vector_add.c -o vector_add -lm

SIZES="1000000 10000000 50000000 100000000"
THREADS="1 2 4 8"

echo "N,threads,seq_time_s,par_time_s,speedup,efficiency" > results/results.csv
for N in $SIZES; do
  for T in $THREADS; do
    echo "Running N=$N threads=$T"
    ./vector_add $N $T 5 >> results/results.csv
  done
done
echo "Done. Results in results/results.csv"
