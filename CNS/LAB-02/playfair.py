SIZE = 5


def normalize(ch):
    ch = ch.upper()

    if ch == 'J':
        ch = 'I'

    return ch


def create_matrix(key):
    matrix = []

    used = set()

    # I and J are treated as the same
    used.add('J')

    # Add key characters
    for ch in key.upper():

        if not ch.isalpha():
            continue

        ch = normalize(ch)

        if ch not in used:
            used.add(ch)

            if len(matrix) == 0 or len(matrix[-1]) == SIZE:
                matrix.append([])

            matrix[-1].append(ch)

    # Add remaining alphabet
    for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":

        if ch == 'J':
            continue

        if ch not in used:
            used.add(ch)

            if len(matrix) == 0 or len(matrix[-1]) == SIZE:
                matrix.append([])

            matrix[-1].append(ch)

    return matrix


def display_matrix(matrix):
    print("\nPlayfair Matrix:\n")

    for row in matrix:
        print(" ".join(row))


def find_position(matrix, ch):

    ch = normalize(ch)

    for row in range(SIZE):
        for col in range(SIZE):

            if matrix[row][col] == ch:
                return row, col

    return None


def prepare_text(text):

    # Remove spaces and non-alphabetic characters
    text = ""

    for ch in input_text:
        if ch.isalpha():
            text += normalize(ch)

    result = ""

    i = 0

    while i < len(text):

        # Last character
        if i == len(text) - 1:

            result += text[i]
            result += 'X'

            i += 1

        # Repeated letters
        elif text[i] == text[i + 1]:

            result += text[i]
            result += 'X'

            i += 1

        # Normal pair
        else:

            result += text[i]
            result += text[i + 1]

            i += 2

    return result


def encrypt_pair(a, b, matrix):

    row1, col1 = find_position(matrix, a)
    row2, col2 = find_position(matrix, b)

    # Same row → move right
    if row1 == row2:

        col1 = (col1 + 1) % SIZE
        col2 = (col2 + 1) % SIZE

    # Same column → move down
    elif col1 == col2:

        row1 = (row1 + 1) % SIZE
        row2 = (row2 + 1) % SIZE

    # Rectangle → swap columns
    else:

        col1, col2 = col2, col1

    return matrix[row1][col1] + matrix[row2][col2]


def decrypt_pair(a, b, matrix):

    row1, col1 = find_position(matrix, a)
    row2, col2 = find_position(matrix, b)

    # Same row → move left
    if row1 == row2:

        col1 = (col1 - 1) % SIZE
        col2 = (col2 - 1) % SIZE

    # Same column → move up
    elif col1 == col2:

        row1 = (row1 - 1) % SIZE
        row2 = (row2 - 1) % SIZE

    # Rectangle → swap columns
    else:

        col1, col2 = col2, col1

    return matrix[row1][col1] + matrix[row2][col2]


def encrypt(text, matrix):

    prepared = prepare_text(text)

    print("\nDigrams:", end=" ")

    for i in range(0, len(prepared), 2):
        print(prepared[i:i + 2], end=" ")

    result = ""

    for i in range(0, len(prepared), 2):

        result += encrypt_pair(
            prepared[i],
            prepared[i + 1],
            matrix
        )

    return result


def decrypt(text, matrix):

    text = ""

    for ch in input_text:
        if ch.isalpha():
            text += normalize(ch)

    if len(text) % 2 != 0:
        print("\nInvalid ciphertext!")
        print("Ciphertext must contain an even number of letters.")
        return None

    result = ""

    for i in range(0, len(text), 2):

        result += decrypt_pair(
            text[i],
            text[i + 1],
            matrix
        )

    return result


print("===== PLAYFAIR CIPHER =====")

key = input("\nEnter key: ")

matrix = create_matrix(key)

display_matrix(matrix)

print("\n1. Encryption")
print("2. Decryption")

choice = int(input("\nEnter your choice: "))

input_text = input("Enter text: ")

if choice == 1:

    cipher = encrypt(input_text, matrix)

    print("\n\nCipher text:", cipher)

elif choice == 2:

    plain = decrypt(input_text, matrix)

    if plain is not None:
        print("\nPlain text:", plain)

else:

    print("\nInvalid choice!")