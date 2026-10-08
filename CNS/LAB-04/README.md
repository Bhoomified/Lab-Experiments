# Cryptographic Algorithms – Performance Analysis

## Algorithms
- RSA
- PKI
- Diffie-Hellman

## Files

```text
rsa.py
pki.py
diffie_hellman.py
crypto_performance.py
```

## Run

```bash
python3 rsa.py
python3 pki.py
python3 diffie_hellman.py
python3 crypto_performance.py
```

## Performance Results

| Algorithm | Key Generation | Main Operation | Verification / Decrypt |
|---|---:|---:|---:|
| RSA | 90.646 ms | 0.254 ms | 1.895 ms |
| PKI | 43.964 ms | 0.893 ms | 0.050 ms |
| Diffie-Hellman | 21232.478 ms | 5.081 ms | N/A |

**Unit:** milliseconds (ms)  
**Iterations:** 10

## Conclusion

- **PKI** had the lowest key-generation time in this experiment.
- **RSA** had the fastest main operation.
- **Diffie-Hellman** had the highest key-generation time because the benchmark generates 2048-bit DH parameters.
- The algorithms perform different functions, so the timings should be compared by operation rather than as direct replacements.