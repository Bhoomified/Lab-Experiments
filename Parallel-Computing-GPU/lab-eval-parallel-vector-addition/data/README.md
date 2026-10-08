# Data

No external input file is needed. Vectors A and B are generated inside
`src/vector_add.c` with a deterministic formula, so every run is reproducible:

    A[i] = (i % 1000) * 0.5
    B[i] = (i % 777)  * 1.5

Vector sizes tested: 1M, 10M, 50M and 100M elements (double precision, 8 bytes each).
At N = 100M the four arrays (A, B, sequential C, parallel C) use about 3.2 GB of
RAM, so reduce the largest size to 50M if your laptop has 8 GB of RAM or less.
