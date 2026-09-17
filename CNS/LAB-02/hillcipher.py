import math


MOD = 26


def mod_inverse(a):
    a %= MOD

    for x in range(1, MOD):
        if (a * x) % MOD == 1:
            return x

    return None


def get_matrix():
    print("\nEnter the 2x2 key matrix:")

    a = int(input("Enter key[0][0]: "))
    b = int(input("Enter key[0][1]: "))
    c = int(input("Enter key[1][0]: "))
    d = int(input("Enter key[1][1]: "))

    return [[a % MOD, b % MOD],
            [c % MOD, d % MOD]]


def determinant(key):
    return (
        key[0][0] * key[1][1]
        - key[0][1] * key[1][0]
    ) % MOD


def encrypt(text, key):
    # Keep only alphabets
    text = ''.join(ch.upper() for ch in text if ch.isalpha())

    # Add X if odd length
    if len(text) % 2 != 0:
        text += 'X'

    result = ""

    for i in range(0, len(text), 2):

        p1 = ord(text[i]) - ord('A')
        p2 = ord(text[i + 1]) - ord('A')

        c1 = (
            key[0][0] * p1 +
            key[0][1] * p2
        ) % MOD

        c2 = (
            key[1][0] * p1 +
            key[1][1] * p2
        ) % MOD

        result += chr(c1 + ord('A'))
        result += chr(c2 + ord('A'))

    return result


def decrypt(text, key):

    text = ''.join(ch.upper() for ch in text if ch.isalpha())

    if len(text) % 2 != 0:
        print("\nCiphertext must contain an even number of letters.")
        return None

    det = determinant(key)

    det_inverse = mod_inverse(det)

    if det_inverse is None:
        print("\nKey matrix cannot be inverted modulo 26.")
        return None

    # Inverse matrix:
    #
    #       d  -b
    # K^-1 =    × det^-1
    #      -c   a

    inverse = [
        [
            (key[1][1] * det_inverse) % MOD,
            (-key[0][1] * det_inverse) % MOD
        ],
        [
            (-key[1][0] * det_inverse) % MOD,
            (key[0][0] * det_inverse) % MOD
        ]
    ]

    result = ""

    for i in range(0, len(text), 2):

        c1 = ord(text[i]) - ord('A')
        c2 = ord(text[i + 1]) - ord('A')

        p1 = (
            inverse[0][0] * c1 +
            inverse[0][1] * c2
        ) % MOD

        p2 = (
            inverse[1][0] * c1 +
            inverse[1][1] * c2
        ) % MOD

        result += chr(p1 + ord('A'))
        result += chr(p2 + ord('A'))

    return result


print("===== HILL CIPHER =====")

key = get_matrix()

det = determinant(key)

if math.gcd(det, MOD) != 1:
    print("\nInvalid key matrix!")
    print("The determinant must be relatively prime to 26.")
    exit()

print("\nKey Matrix:")

for row in key:
    print(row)

print("\n1. Encrypt")
print("2. Decrypt")

choice = int(input("\nEnter your choice: "))

text = input("Enter text: ")

if choice == 1:

    encrypted = encrypt(text, key)

    print("\nEncrypted text:", encrypted)

elif choice == 2:

    decrypted = decrypt(text, key)

    if decrypted is not None:
        print("\nDecrypted text:", decrypted)

else:
    print("\nInvalid choice!")