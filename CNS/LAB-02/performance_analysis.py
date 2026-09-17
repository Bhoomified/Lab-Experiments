import time
import csv
import matplotlib.pyplot as plt


# ============================================================
# 1. MONOALPHABETIC CIPHER
# ============================================================

def monoalphabetic_encrypt(text, key):

    result = ""

    for ch in text:
        if ch.isalpha():
            ch = ch.upper()
            result += key[ord(ch) - ord('A')]
        else:
            result += ch

    return result


# ============================================================
# 2. HILL CIPHER
# ============================================================

def hill_encrypt(text, key):

    text = ''.join(
        ch.upper()
        for ch in text
        if ch.isalpha()
    )

    # Make length even
    if len(text) % 2 != 0:
        text += 'X'

    result = ""

    for i in range(0, len(text), 2):

        p1 = ord(text[i]) - ord('A')
        p2 = ord(text[i + 1]) - ord('A')

        c1 = (
            key[0][0] * p1 +
            key[0][1] * p2
        ) % 26

        c2 = (
            key[1][0] * p1 +
            key[1][1] * p2
        ) % 26

        result += chr(c1 + ord('A'))
        result += chr(c2 + ord('A'))

    return result


# ============================================================
# 3. PLAYFAIR CIPHER
# ============================================================

def create_playfair_matrix(key):

    used = set()
    matrix = []

    key = key.upper()

    # I and J treated as same
    used.add('J')

    # Add key characters
    for ch in key:

        if ch.isalpha():

            if ch == 'J':
                ch = 'I'

            if ch not in used:

                used.add(ch)

                if len(matrix) == 0 or len(matrix[-1]) == 5:
                    matrix.append([])

                matrix[-1].append(ch)

    # Add remaining alphabet
    for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":

        if ch == 'J':
            continue

        if ch not in used:

            used.add(ch)

            if len(matrix) == 0 or len(matrix[-1]) == 5:
                matrix.append([])

            matrix[-1].append(ch)

    return matrix


def find_position(matrix, ch):

    if ch == 'J':
        ch = 'I'

    for row in range(5):
        for col in range(5):

            if matrix[row][col] == ch:
                return row, col

    return None


def playfair_encrypt(text, matrix):

    # Clean text
    text = ''.join(
        ch.upper()
        for ch in text
        if ch.isalpha()
    )

    # Replace J with I
    text = text.replace('J', 'I')

    # Create digrams
    prepared = ""

    i = 0

    while i < len(text):

        if i == len(text) - 1:

            prepared += text[i]
            prepared += 'X'

            i += 1

        elif text[i] == text[i + 1]:

            prepared += text[i]
            prepared += 'X'

            i += 1

        else:

            prepared += text[i]
            prepared += text[i + 1]

            i += 2

    result = ""

    # Encrypt pairs
    for i in range(0, len(prepared), 2):

        a = prepared[i]
        b = prepared[i + 1]

        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        # Same row → move right
        if row1 == row2:

            col1 = (col1 + 1) % 5
            col2 = (col2 + 1) % 5

        # Same column → move down
        elif col1 == col2:

            row1 = (row1 + 1) % 5
            row2 = (row2 + 1) % 5

        # Rectangle → swap columns
        else:

            col1, col2 = col2, col1

        result += matrix[row1][col1]
        result += matrix[row2][col2]

    return result


# ============================================================
# 4. COLUMNAR TRANSPOSITION
# ============================================================

def transposition_encrypt(text, key):

    text = ''.join(
        ch.upper()
        for ch in text
        if ch.isalpha()
    )

    key = key.upper()

    columns = len(key)

    # Padding
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

    # Determine alphabetical column order
    order = sorted(
        range(columns),
        key=lambda i: (key[i], i)
    )

    result = ""

    # Read columns
    for col in order:

        for row in range(rows):

            result += matrix[row][col]

    return result


# ============================================================
# PERFORMANCE TEST
# ============================================================

print("==============================================")
print("       CRYPTOGRAPHY PERFORMANCE ANALYSIS")
print("==============================================")

# Input sizes
input_sizes = [
    100,
    500,
    1000,
    5000,
    10000,
    50000,
    100000
]

# Generate test text
base_text = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"

# Keys
mono_key = "QWERTYUIOPASDFGHJKLZXCVBNM"

hill_key = [
    [3, 3],
    [2, 5]
]

playfair_key = "MONARCHY"

transposition_key = "ZEBRA"

# Create Playfair matrix
playfair_matrix = create_playfair_matrix(playfair_key)


# Store results
mono_times = []
hill_times = []
playfair_times = []
transposition_times = []


# Number of repetitions
REPEAT = 5


# ============================================================
# RUN TESTS
# ============================================================

for n in input_sizes:

    text = (base_text * ((n // len(base_text)) + 1))[:n]

    print(f"\nTesting input size: {n}")

    # ------------------------------------------
    # Monoalphabetic
    # ------------------------------------------

    start = time.perf_counter()

    for _ in range(REPEAT):
        monoalphabetic_encrypt(text, mono_key)

    end = time.perf_counter()

    mono_time = (end - start) / REPEAT

    mono_times.append(mono_time)


    # ------------------------------------------
    # Hill Cipher
    # ------------------------------------------

    start = time.perf_counter()

    for _ in range(REPEAT):
        hill_encrypt(text, hill_key)

    end = time.perf_counter()

    hill_time = (end - start) / REPEAT

    hill_times.append(hill_time)


    # ------------------------------------------
    # Playfair
    # ------------------------------------------

    start = time.perf_counter()

    for _ in range(REPEAT):
        playfair_encrypt(text, playfair_matrix)

    end = time.perf_counter()

    playfair_time = (end - start) / REPEAT

    playfair_times.append(playfair_time)


    # ------------------------------------------
    # Transposition
    # ------------------------------------------

    start = time.perf_counter()

    for _ in range(REPEAT):
        transposition_encrypt(text, transposition_key)

    end = time.perf_counter()

    transposition_time = (end - start) / REPEAT

    transposition_times.append(transposition_time)


    print(
        f"Monoalphabetic : {mono_time:.8f} seconds"
    )

    print(
        f"Hill Cipher     : {hill_time:.8f} seconds"
    )

    print(
        f"Playfair        : {playfair_time:.8f} seconds"
    )

    print(
        f"Transposition   : {transposition_time:.8f} seconds"
    )


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n\n==============================================")
print("                 RESULTS")
print("==============================================")

print(
    f"{'Input':<12}"
    f"{'Mono':<15}"
    f"{'Hill':<15}"
    f"{'Playfair':<15}"
    f"{'Transposition':<15}"
)

for i in range(len(input_sizes)):

    print(
        f"{input_sizes[i]:<12}"
        f"{mono_times[i]:<15.8f}"
        f"{hill_times[i]:<15.8f}"
        f"{playfair_times[i]:<15.8f}"
        f"{transposition_times[i]:<15.8f}"
    )


# ============================================================
# SAVE RESULTS TO CSV
# ============================================================

with open(
    "performance_results.csv",
    "w",
    newline=""
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "Input Size",
        "Monoalphabetic",
        "Hill Cipher",
        "Playfair",
        "Transposition"
    ])

    for i in range(len(input_sizes)):

        writer.writerow([
            input_sizes[i],
            mono_times[i],
            hill_times[i],
            playfair_times[i],
            transposition_times[i]
        ])


print("\nResults saved to:")
print("performance_results.csv")


# ============================================================
# GRAPH
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    input_sizes,
    mono_times,
    marker='o',
    label='Monoalphabetic'
)

plt.plot(
    input_sizes,
    hill_times,
    marker='o',
    label='Hill Cipher'
)

plt.plot(
    input_sizes,
    playfair_times,
    marker='o',
    label='Playfair'
)

plt.plot(
    input_sizes,
    transposition_times,
    marker='o',
    label='Transposition'
)

plt.xlabel("Input Size (characters)")
plt.ylabel("Average Execution Time (seconds)")

plt.title(
    "Performance Analysis of Cryptographic Algorithms"
)

plt.legend()

plt.grid(True)

plt.tight_layout()

# Save graph
plt.savefig(
    "performance_comparison.png",
    dpi=300
)

print("\nGraph saved as:")
print("performance_comparison.png")

# SHOW GRAPH
plt.show()