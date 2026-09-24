# 🔐 LAB-03 — AES & DES Cryptography

> **Objective:** Implement AES and DES encryption/decryption using a cryptographic library, extend the implementation to binary files, and compare their performance.

---

## 1. What is Cryptography?

Cryptography protects data by transforming **plaintext** into unreadable **ciphertext** using a key.

```text
Plaintext
   ↓
Encryption + Key
   ↓
Ciphertext
   ↓
Decryption + Key
   ↓
Plaintext
```

AES and DES are **symmetric-key block ciphers**, meaning the same secret key is used for encryption and decryption.

---

## 2. AES vs DES

| Feature | AES | DES |
|---|---:|---:|
| Full form | Advanced Encryption Standard | Data Encryption Standard |
| Type | Symmetric block cipher | Symmetric block cipher |
| Block size | 128 bits | 64 bits |
| Key sizes | 128 / 192 / 256 bits | 56-bit effective key |
| Mode used | CBC | CBC |
| IV size in CBC | 16 bytes | 8 bytes |
| Use today | Modern standard | Legacy / educational |

### AES
AES encrypts data in **128-bit blocks** using 128-, 192-, or 256-bit keys.

### DES
DES encrypts data in **64-bit blocks**. Its effective key strength is only **56 bits**, so it is considered obsolete for modern security systems and is used here for educational comparison.

---

## 3. Cryptographic Library — PyCryptodome

### Library used
**PyCryptodome**

```python
from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
```

### Why PyCryptodome?

- Provides ready-to-use AES and **single DES** implementations.
- Supports CBC mode, padding, secure random byte generation, and binary data processing.
- Keeps the implementation focused on using and understanding the algorithms instead of implementing cryptographic primitives from scratch.

### How it works in this experiment

```text
Python Program
     ↓
PyCryptodome
     ↓
AES / DES cipher
     ↓
Encryption / Decryption
```

---

## 4. Encryption Mode — CBC

Both experiments use **Cipher Block Chaining (CBC)**.

A random **Initialization Vector (IV)** is generated for every encryption.

```text
Plaintext Block
      +
 IV / Previous Ciphertext
      ↓
   AES / DES
      ↓
Ciphertext Block
```

CBC requires padding when the final block is incomplete. The implementation uses **PKCS#7 padding**.

---

## 5. Normal Text Encryption Flow

Text is converted into bytes before encryption.

```text
User enters text
      ↓
UTF-8 bytes
      ↓
PKCS#7 padding
      ↓
AES / DES + CBC + IV
      ↓
Ciphertext
      ↓
Decryption
      ↓
Remove padding
      ↓
Original text
```

The program verifies:

```text
Original == Decrypted
```

---

## 6. Image / Audio / Video Encryption Flow

Media files are treated as **raw binary bytes**. The file type itself does not matter to AES or DES.

```text
Image / Audio / Video
        ↓
Open as binary ("rb")
        ↓
Read in chunks
        ↓
PKCS#7 padding for final block
        ↓
AES / DES + CBC + IV
        ↓
Encrypted binary file
        ↓
Decryption
        ↓
Original binary bytes
        ↓
Recovered Image / Audio / Video
```

Large files are processed in chunks instead of loading the entire file into memory.

The encrypted file stores required metadata such as the algorithm, key length, IV, and original filename — **not the secret key**.

---

## 7. Performance Analysis

The same input data was tested with AES-128 and DES for multiple file sizes. Each result was verified successfully.

### Performance Results

| Algorithm | Size | Encryption Time (ms) | Decryption Time (ms) | Total Time (ms) | Enc. Throughput (MB/s) | Dec. Throughput (MB/s) | Verification |
|---|---:|---:|---:|---:|---:|---:|---|
| AES | 1 KB | 0.006917 | 0.006772 | 0.013688 | 141.18 | 144.23 | SUCCESS |
| DES | 1 KB | 0.035917 | 0.026022 | 0.061938 | 27.19 | 37.53 | SUCCESS |
| AES | 10 KB | 0.071084 | 0.056042 | 0.127125 | 137.38 | 174.26 | SUCCESS |
| DES | 10 KB | 0.206146 | 0.157500 | 0.363646 | 47.37 | 62.00 | SUCCESS |
| AES | 100 KB | 0.505666 | 0.392667 | 0.898334 | 193.12 | 248.70 | SUCCESS |
| DES | 100 KB | 2.010751 | 1.531917 | 3.542667 | 48.57 | 63.75 | SUCCESS |
| AES | 1024 KB | 5.088021 | 3.911749 | 8.999771 | 196.54 | 255.64 | SUCCESS |
| DES | 1024 KB | 20.591042 | 15.689667 | 36.280709 | 48.56 | 63.74 | SUCCESS |

### Observations

- Encryption and decryption were successful for **all tested input sizes**.
- AES shows substantially higher throughput than DES across the tested sizes.
- As the input size increases, execution time increases while throughput becomes more stable.
- DES requires significantly more time to process the same data in this experiment.

---

## 8. Key Takeaways

- **AES and DES are symmetric block ciphers.**
- **PyCryptodome** provides the cryptographic primitives used in this lab.
- **CBC mode** uses a random IV and processes data block-by-block.
- Text, images, audio, and videos can all be encrypted because they are ultimately sequences of bytes.
- Binary files are processed in **chunks** for better memory efficiency.
- DES is included for educational comparison; **AES is the modern choice for real applications**.

---

### ✅ Result

AES and DES were successfully implemented using **PyCryptodome**, tested with dynamic text input, extended to binary file encryption, and evaluated using performance measurements across multiple input sizes.
