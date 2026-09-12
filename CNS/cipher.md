# Cryptography Laboratory: Classical Substitution Ciphers

A practical record and analysis of classical symmetric encryption techniques implemented in C. This document tracks implementations, algorithmic mechanics, custom optimizations, and security observations.

---

## 1. Theoretical Overview

### Classical Cryptography & Substitution
Classical ciphers operate on characters or fixed blocks of letters using substitution or transposition. In a **substitution cipher**, units of plaintext are replaced with ciphertext according to a deterministic key and mathematical mapping.

* **Monoalphabetic Ciphers:** Each character in the alphabet maps to exactly one predetermined substitute throughout the entire message (e.g., Shift-by-$N$ / Caesar).
* **Polygraphic Ciphers:** Multiple characters are grouped and substituted simultaneously as blocks (digraphs, trigraphs), disrupting single-letter frequency distribution (e.g., Playfair).

---

## 2. Experiment 1: Simple Shift-by-$N$ Substitution Cipher

### 2.1 Mechanism
A modular arithmetic cipher where each character $p$ is shifted forward by an integer key $n$:

$$c = (p + n) \pmod{26}$$

Decryption applies the inverse transformation:

$$p = (c - n) \pmod{26}$$

### 2.2 Implementation Details & Edge Cases
* **Shift Normalization:** C's `%` operator calculates remainder, not mathematical modulo. We applied `(shift % 26 + 26) % 26` to safely bound negative shifts and shifts $n \ge 26$ to the range $[0, 25]$.
* **Case & Symbol Preservation:** Uppercase (`A–Z`) and lowercase (`a–z`) are converted to $[0, 25]$ indices and transformed independently. Non-alphabetic symbols (spaces, punctuation, digits) bypass the shift.
* **Persistent CLI Loop:** Wrapped the program in an interactive `while (1)` loop with an input buffer scrubber (`clear_input_buffer()`) to flush trailing newlines from `scanf()` and prevent stdin lockups.

---

## 3. Experiment 2: Shift-by-$N$ with Dictionary-Assisted Cryptanalysis

### 3.1 Objective & Thought Process
Monoalphabetic shift ciphers have a keyspace of only 26 possible values ($n \in [0, 25]$), making them trivially vulnerable to exhaustive key search (brute-force). 

Instead of forcing manual human review of all 25 output streams, we automated the cryptanalysis phase:
1. Try every candidate key $n = 1 \dots 25$.
2. Decrypt the candidate text using $-n$.
3. Check candidate words against a dictionary to evaluate readability.
4. Select the candidate key that yields valid, meaningful plaintext.

### 3.2 Engineering Solutions & Optimizations
* **macOS System Dictionary Integration:** Loaded the local `/usr/share/dict/words` file (~235,000 words) instead of issuing rate-limited, latency-heavy HTTP API requests.
* **High-Performance Hash Table:** Sized the hash table to $500,009$ buckets (prime number) using the `djb2` hash algorithm (`hash * 33 + c`) to achieve $O(1)$ word validation.
* **Early-Exit Mechanism:** Pre-calculated the total number of alphabetic words in the ciphertext. If a candidate key decrypts a text where `matched_words == total_words`, the program immediately halts execution without evaluating remaining keys.
* **Short-Word Guard:** Filtered out obscure two-letter dictionary words (e.g., `aa`, `ba`, `ka`) by enforcing an exact whitelist of standard English two-letter words (`in`, `at`, `to`, `is`, `it`, etc.) to eliminate false-positive early exits.

---

## 4. Experiment 3: The Playfair Cipher

### 4.1 Mechanism
A polygraphic substitution cipher encrypting digraphs (pairs of letters) using a $5 \times 5$ grid generated from a user-supplied keyword.
* Standard English has 26 letters; the matrix has 25 cells. The letters `I` and `J` are merged into one cell (`I/J`).
* The keyphrase is populated first (omitting duplicate letters), followed by the remainder of the alphabet.

### 4.2 Substitution Rules (Per Digraph)
1. **Same Row:** Replace each letter with the character immediately to its right (wrapping around to the left edge if at the boundary).
2. **Same Column:** Replace each letter with the character immediately below it (wrapping around to the top edge if at the bottom).
3. **Rectangle / Box:** Replace each letter with the character in its own row that shares the column of the other letter.
4. **Decryption:** Applies inverse coordinates (shifts left in rows, up in columns using `(pos + 4) % 5` to safely avoid negative C remainders).

### 4.3 Handled Edge Cases
* **Digraph Letter Duplication:** Identical adjacent letters in a pair (e.g., `EE`) cannot be looked up as a rectangle. A standard filler character (`X`) is inserted between them.
* **Dynamic Filler Collision:** If the repeated letter is itself `X` (e.g., `XX` in `"FOXXY"`) or the text ends on an odd `X`, using `X` causes an illegal collision. The program detects this and dynamically prompts the user for an alternative filler character (e.g., `Q` or `Z`).
* **Odd Plaintext Length:** An odd-length message is automatically padded at the end with the active filler character.
* **Odd Ciphertext Validation:** Reject ciphertext inputs with an odd number of characters during decryption, as Playfair ciphertexts must strictly be even-length digraph streams.

---

## 5. Security Summary & Key Takeaways

| Algorithm | Cipher Type | Keyspace Size | Primary Vulnerability | Cryptanalysis Method |
| :--- | :--- | :--- | :--- | :--- |
| **Shift-by-$N$** | Monoalphabetic Substitution | 25 | Extremely small keyspace; preserves letter frequencies | Brute-force key exhaustion & dictionary match |
| **Playfair Cipher** | Polygraphic Substitution | $\approx 25! \approx 1.55 \times 10^{25}$ | Preserves digraph frequency patterns | Digraph frequency analysis; identification of filler patterns |

### Key Learning Outcomes
1. **Modular Arithmetic in C:** Arithmetic operations on character sets require explicit offset normalization because the C `%` operator can yield negative remainders.
2. **Algorithmic Cryptanalysis:** Automation transforms brute-force cracking from visual inspection into an $O(1)$ dictionary lookup problem using hash tables.
3. **State Management in Digraph Preprocessing:** Polygraphic ciphers require strict string preprocessing (padding, collision mitigation, character merging) before cryptographic operations can execute safely.