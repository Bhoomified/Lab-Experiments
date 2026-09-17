def get_order(key):
    # Sort according to alphabet.
    # enumerate() also handles repeated letters
    # from left to right.
    return sorted(range(len(key)), key=lambda i: (key[i], i))


def encrypt(text, key):

    # Remove spaces and keep alphabets
    text = ''.join(
        ch.upper()
        for ch in text
        if ch.isalpha()
    )

    key = key.upper()

    columns = len(key)

    # Add X padding
    while len(text) % columns != 0:
        text += 'X'

    rows = len(text) // columns

    # Create matrix
    matrix = []

    index = 0

    for i in range(rows):
        row = []

        for j in range(columns):
            row.append(text[index])
            index += 1

        matrix.append(row)

    print("\nMatrix:")

    for row in matrix:
        print(" ".join(row))

    # Determine column order
    order = get_order(key)

    print("\nColumn order:", end=" ")

    for col in order:
        print(col + 1, end=" ")

    print()

    # Read columns
    result = ""

    for col in order:
        for row in range(rows):
            result += matrix[row][col]

    return result


def decrypt(ciphertext, key):

    ciphertext = ''.join(
        ch.upper()
        for ch in ciphertext
        if ch.isalpha()
    )

    key = key.upper()

    columns = len(key)

    if len(ciphertext) % columns != 0:
        print("\nInvalid ciphertext length.")
        print("Ciphertext length must be divisible by key length.")
        return None

    rows = len(ciphertext) // columns

    # Empty matrix
    matrix = [
        [''] * columns
        for _ in range(rows)
    ]

    order = get_order(key)

    index = 0

    # Put ciphertext column-wise
    for col in order:

        for row in range(rows):

            matrix[row][col] = ciphertext[index]

            index += 1

    print("\nMatrix:")

    for row in matrix:
        print(" ".join(row))

    # Read row-wise
    result = ""

    for row in range(rows):

        for col in range(columns):

            result += matrix[row][col]

    return result


print("===== COLUMNAR TRANSPOSITION CIPHER =====")

key = input("\nEnter key: ")

print("\n1. Encryption")
print("2. Decryption")

choice = int(input("\nEnter your choice: "))

text = input("Enter text: ")


if choice == 1:

    cipher = encrypt(text, key)

    print("\nEncrypted text:", cipher)


elif choice == 2:

    plain = decrypt(text, key)

    if plain is not None:
        print("\nDecrypted text:", plain)


else:

    print("\nInvalid choice!")