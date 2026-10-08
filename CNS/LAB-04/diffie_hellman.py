
# Diffie-Hellman Key Exchange
# Dynamic Python Implementation


# Check whether a number is prime
def is_prime(n):
    if n < 2:
        return False

    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False

    return True


print("========== DIFFIE-HELLMAN KEY EXCHANGE ==========")

# Input public values
p = int(input("Enter a prime number (p): "))
g = int(input("Enter a primitive root (g): "))

# Validate p
if not is_prime(p):
    print("Error: p must be a prime number.")
    exit()

if g <= 1 or g >= p:
    print("Error: g must be greater than 1 and less than p.")
    exit()

# Private keys
a = int(input("Enter Alice's private key: "))
b = int(input("Enter Bob's private key: "))

if a <= 0 or b <= 0:
    print("Error: Private keys must be positive.")
    exit()

# Alice calculates public key
A = pow(g, a, p)

# Bob calculates public key
B = pow(g, b, p)

print("\n========== KEY EXCHANGE ==========")

print("\nPublic Parameters:")
print("Prime number (p) =", p)
print("Primitive root (g) =", g)

print("\nPrivate Keys:")
print("Alice's private key =", a)
print("Bob's private key   =", b)

print("\nPublic Keys:")
print("Alice's public key =", A)
print("Bob's public key   =", B)

# Calculate shared secret
alice_shared_key = pow(B, a, p)
bob_shared_key = pow(A, b, p)

print("\nShared Secret:")
print("Alice's shared key =", alice_shared_key)
print("Bob's shared key   =", bob_shared_key)

# Verify
if alice_shared_key == bob_shared_key:
    print("\nSUCCESS!")
    print("Both Alice and Bob have the same shared secret.")
else:
    print("\nFAILED!")
    print("The shared secrets do not match.")

print("\nDiffie-Hellman execution completed successfully!")