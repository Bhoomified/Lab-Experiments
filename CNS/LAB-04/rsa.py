import math


# Check whether a number is prime
def is_prime(n):
    if n < 2:
        return False

    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False

    return True


# Calculate GCD
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


# Extended Euclidean Algorithm
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0

    g, x1, y1 = extended_gcd(b, a % b)

    x = y1
    y = x1 - (a // b) * y1

    return g, x, y


# Calculate modular inverse
def mod_inverse(e, phi):
    g, x, _ = extended_gcd(e, phi)

    if g != 1:
        return None

    return x % phi


# Generate RSA keys
def generate_keys(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose the smallest e such that gcd(e, phi) = 1
    e = 2

    while e < phi:
        if gcd(e, phi) == 1:
            break
        e += 1

    d = mod_inverse(e, phi)

    return e, d, n, phi


# Encrypt message
def encrypt(message, e, n):
    ciphertext = []

    for char in message:
        m = ord(char)

        if m >= n:
            raise ValueError(
                "Prime numbers are too small for this character."
            )

        c = pow(m, e, n)
        ciphertext.append(c)

    return ciphertext


# Decrypt message
def decrypt(ciphertext, d, n):
    message = ""

    for c in ciphertext:
        m = pow(c, d, n)
        message += chr(m)

    return message


# ---------------- MAIN PROGRAM ----------------

print("========== RSA ALGORITHM ==========")

# Input prime numbers
p = int(input("Enter prime number p: "))
q = int(input("Enter prime number q: "))

# Validate input
if not is_prime(p) or not is_prime(q):
    print("Error: Both p and q must be prime numbers.")
    exit()

if p == q:
    print("Error: p and q must be different.")
    exit()

# Generate keys
e, d, n, phi = generate_keys(p, q)

print("\nRSA Parameters")
print("----------------")
print("p =", p)
print("q =", q)
print("n =", n)
print("phi(n) =", phi)

print("\nKeys")
print("----------------")
print("Public Key  =", (e, n))
print("Private Key =", (d, n))

# Input message
message = input("\nEnter message: ")

# Encryption
ciphertext = encrypt(message, e, n)

print("\nEncrypted Message:")
print(ciphertext)

# Decryption
decrypted_message = decrypt(ciphertext, d, n)

print("\nDecrypted Message:")
print(decrypted_message)

print("\nRSA execution completed successfully!")