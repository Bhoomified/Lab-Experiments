import csv
import os
import statistics
import time

import matplotlib.pyplot as plt

from Crypto.Cipher import AES, DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


# ============================================================
# CONFIGURATION
# ============================================================

AES_KEY = b"1234567890123456"   # AES-128 -> 16 bytes
DES_KEY = b"12345678"           # DES -> 8 bytes

DEFAULT_SIZES_KB = [1, 10, 100, 1024]

DEFAULT_WARMUP_RUNS = 3
DEFAULT_MEASURED_RUNS = 30

CSV_FILE = "performance_results.csv"
GRAPH_DIRECTORY = "graphs"


# ============================================================
# AES ENCRYPTION
# ============================================================

def aes_encrypt(data, key):
    """
    Encrypt data using AES-128 in CBC mode.

    Padding and IV generation are performed outside
    the measured encryption interval so that the benchmark
    focuses on the cipher processing itself.
    """

    iv = get_random_bytes(AES.block_size)

    padded_data = pad(
        data,
        AES.block_size
    )

    cipher = AES.new(
        key,
        AES.MODE_CBC,
        iv
    )

    start = time.perf_counter_ns()

    ciphertext = cipher.encrypt(
        padded_data
    )

    end = time.perf_counter_ns()

    encryption_time_ns = end - start

    return iv, ciphertext, encryption_time_ns


# ============================================================
# AES DECRYPTION
# ============================================================

def aes_decrypt(ciphertext, key, iv):
    """
    Decrypt AES-CBC ciphertext.

    Decryption timing measures the cipher operation.
    Padding removal is outside the measured interval.
    """

    cipher = AES.new(
        key,
        AES.MODE_CBC,
        iv
    )

    start = time.perf_counter_ns()

    padded_plaintext = cipher.decrypt(
        ciphertext
    )

    end = time.perf_counter_ns()

    decryption_time_ns = end - start

    plaintext = unpad(
        padded_plaintext,
        AES.block_size
    )

    return plaintext, decryption_time_ns


# ============================================================
# DES ENCRYPTION
# ============================================================

def des_encrypt(data, key):
    """
    Encrypt data using DES in CBC mode.
    """

    iv = get_random_bytes(DES.block_size)

    padded_data = pad(
        data,
        DES.block_size
    )

    cipher = DES.new(
        key,
        DES.MODE_CBC,
        iv
    )

    start = time.perf_counter_ns()

    ciphertext = cipher.encrypt(
        padded_data
    )

    end = time.perf_counter_ns()

    encryption_time_ns = end - start

    return iv, ciphertext, encryption_time_ns


# ============================================================
# DES DECRYPTION
# ============================================================

def des_decrypt(ciphertext, key, iv):
    """
    Decrypt DES-CBC ciphertext.
    """

    cipher = DES.new(
        key,
        DES.MODE_CBC,
        iv
    )

    start = time.perf_counter_ns()

    padded_plaintext = cipher.decrypt(
        ciphertext
    )

    end = time.perf_counter_ns()

    decryption_time_ns = end - start

    plaintext = unpad(
        padded_plaintext,
        DES.block_size
    )

    return plaintext, decryption_time_ns


# ============================================================
# BENCHMARK FUNCTION
# ============================================================

def benchmark_algorithm(
    algorithm_name,
    data,
    encrypt_function,
    decrypt_function,
    key,
    warmup_runs,
    measured_runs
):
    """
    Benchmark one algorithm for one input size.
    """

    encryption_times = []
    decryption_times = []

    # --------------------------------------------------------
    # Warm-up
    # --------------------------------------------------------

    for _ in range(warmup_runs):

        iv, ciphertext, _ = encrypt_function(
            data,
            key
        )

        decrypted, _ = decrypt_function(
            ciphertext,
            key,
            iv
        )

        if decrypted != data:
            raise RuntimeError(
                f"{algorithm_name} verification failed "
                "during warm-up."
            )

    # --------------------------------------------------------
    # Measured runs
    # --------------------------------------------------------

    for _ in range(measured_runs):

        iv, ciphertext, encryption_time = encrypt_function(
            data,
            key
        )

        decrypted, decryption_time = decrypt_function(
            ciphertext,
            key,
            iv
        )

        # Verify EVERY run
        if decrypted != data:
            raise RuntimeError(
                f"{algorithm_name} verification failed."
            )

        encryption_times.append(
            encryption_time
        )

        decryption_times.append(
            decryption_time
        )

    # --------------------------------------------------------
    # Median timing
    # --------------------------------------------------------

    median_encryption_ns = statistics.median(
        encryption_times
    )

    median_decryption_ns = statistics.median(
        decryption_times
    )

    encryption_seconds = (
        median_encryption_ns / 1_000_000_000
    )

    decryption_seconds = (
        median_decryption_ns / 1_000_000_000
    )

    total_seconds = (
        encryption_seconds +
        decryption_seconds
    )

    # --------------------------------------------------------
    # Throughput
    # --------------------------------------------------------

    size_mb = len(data) / (1024 * 1024)

    if encryption_seconds > 0:
        encryption_throughput = (
            size_mb / encryption_seconds
        )
    else:
        encryption_throughput = 0

    if decryption_seconds > 0:
        decryption_throughput = (
            size_mb / decryption_seconds
        )
    else:
        decryption_throughput = 0

    return {
        "algorithm": algorithm_name,
        "size_bytes": len(data),
        "size_kb": len(data) / 1024,
        "size_mb": size_mb,
        "encryption_time_s": encryption_seconds,
        "decryption_time_s": decryption_seconds,
        "total_time_s": total_seconds,
        "encryption_latency_ms": encryption_seconds * 1000,
        "decryption_latency_ms": decryption_seconds * 1000,
        "encryption_throughput_MBps": encryption_throughput,
        "decryption_throughput_MBps": decryption_throughput,
        "verification": "SUCCESS"
    }


# ============================================================
# INPUT SIZE
# ============================================================

def get_input_sizes():
    """
    Allow the user to enter custom input sizes in KB.
    """

    print("\nInput sizes are measured in KB.")

    print(
        "Default sizes:",
        ", ".join(
            f"{size} KB"
            for size in DEFAULT_SIZES_KB
        )
    )

    user_input = input(
        "\nEnter sizes separated by commas "
        "(press Enter for default): "
    ).strip()

    if not user_input:
        return DEFAULT_SIZES_KB

    try:

        sizes = [
            int(value.strip())
            for value in user_input.split(",")
        ]

        if any(size <= 0 for size in sizes):
            raise ValueError

        return sizes

    except ValueError:

        print(
            "Invalid input. Using default sizes."
        )

        return DEFAULT_SIZES_KB


# ============================================================
# NUMBER OF RUNS
# ============================================================

def get_number_of_runs():
    """
    Ask the user how many measurements to perform.
    """

    user_input = input(
        f"\nNumber of measured runs "
        f"(default {DEFAULT_MEASURED_RUNS}): "
    ).strip()

    if not user_input:
        return DEFAULT_MEASURED_RUNS

    try:

        runs = int(user_input)

        if runs <= 0:
            raise ValueError

        return runs

    except ValueError:

        print(
            "Invalid value. "
            "Using default number of runs."
        )

        return DEFAULT_MEASURED_RUNS


# ============================================================
# SAVE CSV
# ============================================================

def save_results(results):
    """
    Save benchmark results to CSV.
    """

    fieldnames = [
        "algorithm",
        "size_bytes",
        "size_kb",
        "size_mb",
        "encryption_time_s",
        "decryption_time_s",
        "total_time_s",
        "encryption_latency_ms",
        "decryption_latency_ms",
        "encryption_throughput_MBps",
        "decryption_throughput_MBps",
        "verification"
    ]

    with open(
        CSV_FILE,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(results)


# ============================================================
# PRINT RESULTS
# ============================================================

def print_results(results):
    """
    Display benchmark results in a formatted table.
    """

    print("\n")
    print("=" * 120)
    print("                 AES vs DES PERFORMANCE ANALYSIS")
    print("=" * 120)

    print(
        f"{'Size(KB)':<12}"
        f"{'Algorithm':<12}"
        f"{'Enc(ms)':<16}"
        f"{'Dec(ms)':<16}"
        f"{'Total(ms)':<16}"
        f"{'Enc(MB/s)':<16}"
        f"{'Dec(MB/s)':<16}"
        f"{'Verify':<12}"
    )

    print("-" * 120)

    for result in results:

        print(
            f"{result['size_kb']:<12.0f}"
            f"{result['algorithm']:<12}"
            f"{result['encryption_latency_ms']:<16.6f}"
            f"{result['decryption_latency_ms']:<16.6f}"
            f"{result['total_time_s'] * 1000:<16.6f}"
            f"{result['encryption_throughput_MBps']:<16.2f}"
            f"{result['decryption_throughput_MBps']:<16.2f}"
            f"{result['verification']:<12}"
        )

        if (
            (results.index(result) + 1) % 2 == 0
        ):
            print("-" * 120)


# ============================================================
# GRAPH HELPER
# ============================================================

def get_algorithm_results(
    results,
    algorithm
):
    """
    Extract results for a specific algorithm.
    """

    return [
        result
        for result in results
        if result["algorithm"] == algorithm
    ]


# ============================================================
# GENERATE GRAPHS
# ============================================================

def generate_graphs(results):
    """
    Generate four performance graphs.
    """

    os.makedirs(
        GRAPH_DIRECTORY,
        exist_ok=True
    )

    aes_results = get_algorithm_results(
        results,
        "AES"
    )

    des_results = get_algorithm_results(
        results,
        "DES"
    )

    sizes_aes = [
        result["size_kb"]
        for result in aes_results
    ]

    sizes_des = [
        result["size_kb"]
        for result in des_results
    ]

    # --------------------------------------------------------
    # Graph 1: Encryption Time
    # --------------------------------------------------------

    plt.figure(figsize=(10, 6))

    plt.plot(
        sizes_aes,
        [
            result["encryption_latency_ms"]
            for result in aes_results
        ],
        marker="o",
        label="AES"
    )

    plt.plot(
        sizes_des,
        [
            result["encryption_latency_ms"]
            for result in des_results
        ],
        marker="o",
        label="DES"
    )

    plt.xlabel("Input Size (KB)")
    plt.ylabel("Encryption Time (ms)")
    plt.title("AES vs DES - Encryption Time")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            GRAPH_DIRECTORY,
            "encryption_time.png"
        ),
        dpi=300
    )

    plt.close()

    # --------------------------------------------------------
    # Graph 2: Decryption Time
    # --------------------------------------------------------

    plt.figure(figsize=(10, 6))

    plt.plot(
        sizes_aes,
        [
            result["decryption_latency_ms"]
            for result in aes_results
        ],
        marker="o",
        label="AES"
    )

    plt.plot(
        sizes_des,
        [
            result["decryption_latency_ms"]
            for result in des_results
        ],
        marker="o",
        label="DES"
    )

    plt.xlabel("Input Size (KB)")
    plt.ylabel("Decryption Time (ms)")
    plt.title("AES vs DES - Decryption Time")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            GRAPH_DIRECTORY,
            "decryption_time.png"
        ),
        dpi=300
    )

    plt.close()

    # --------------------------------------------------------
    # Graph 3: Encryption Throughput
    # --------------------------------------------------------

    plt.figure(figsize=(10, 6))

    plt.plot(
        sizes_aes,
        [
            result["encryption_throughput_MBps"]
            for result in aes_results
        ],
        marker="o",
        label="AES"
    )

    plt.plot(
        sizes_des,
        [
            result["encryption_throughput_MBps"]
            for result in des_results
        ],
        marker="o",
        label="DES"
    )

    plt.xlabel("Input Size (KB)")
    plt.ylabel("Encryption Throughput (MB/s)")
    plt.title("AES vs DES - Encryption Throughput")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            GRAPH_DIRECTORY,
            "encryption_throughput.png"
        ),
        dpi=300
    )

    plt.close()

    # --------------------------------------------------------
    # Graph 4: Decryption Throughput
    # --------------------------------------------------------

    plt.figure(figsize=(10, 6))

    plt.plot(
        sizes_aes,
        [
            result["decryption_throughput_MBps"]
            for result in aes_results
        ],
        marker="o",
        label="AES"
    )

    plt.plot(
        sizes_des,
        [
            result["decryption_throughput_MBps"]
            for result in des_results
        ],
        marker="o",
        label="DES"
    )

    plt.xlabel("Input Size (KB)")
    plt.ylabel("Decryption Throughput (MB/s)")
    plt.title("AES vs DES - Decryption Throughput")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            GRAPH_DIRECTORY,
            "decryption_throughput.png"
        ),
        dpi=300
    )

    plt.close()


# ============================================================
# SUMMARY
# ============================================================

def print_summary(results):
    """
    Print a simple summary of the benchmark.
    """

    print("\n" + "=" * 70)
    print("                         SUMMARY")
    print("=" * 70)

    for algorithm in ["AES", "DES"]:

        algorithm_results = get_algorithm_results(
            results,
            algorithm
        )

        avg_encryption_time = statistics.mean(
            result["encryption_latency_ms"]
            for result in algorithm_results
        )

        avg_decryption_time = statistics.mean(
            result["decryption_latency_ms"]
            for result in algorithm_results
        )

        avg_encryption_throughput = statistics.mean(
            result["encryption_throughput_MBps"]
            for result in algorithm_results
        )

        avg_decryption_throughput = statistics.mean(
            result["decryption_throughput_MBps"]
            for result in algorithm_results
        )

        print(f"\n{algorithm}")

        print(
            f"Average Encryption Time     : "
            f"{avg_encryption_time:.6f} ms"
        )

        print(
            f"Average Decryption Time     : "
            f"{avg_decryption_time:.6f} ms"
        )

        print(
            f"Average Encryption Throughput: "
            f"{avg_encryption_throughput:.2f} MB/s"
        )

        print(
            f"Average Decryption Throughput: "
            f"{avg_decryption_throughput:.2f} MB/s"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("              CRYPTOGRAPHY PERFORMANCE LAB")
    print("                    AES vs DES")
    print("=" * 70)

    print("\nAlgorithms:")
    print("  AES-128")
    print("  DES-CBC")

    print(
        "\nBenchmark methodology:"
        "\n  - Same input data for AES and DES"
        "\n  - Warm-up runs"
        "\n  - Multiple measured runs"
        "\n  - Median execution time"
        "\n  - Verification on every run"
    )

    sizes_kb = get_input_sizes()

    measured_runs = get_number_of_runs()

    print(
        "\nWarm-up runs:",
        DEFAULT_WARMUP_RUNS
    )

    print(
        "Measured runs:",
        measured_runs
    )

    results = []

    # ========================================================
    # BENCHMARK EACH SIZE
    # ========================================================

    for size_kb in sizes_kb:

        size_bytes = size_kb * 1024

        print(
            f"\nRunning benchmark for "
            f"{size_kb} KB..."
        )

        # Generate ONE dataset for this size.
        # Both algorithms receive the same data.
        data = get_random_bytes(
            size_bytes
        )

        # ----------------------------------------------------
        # AES
        # ----------------------------------------------------

        aes_result = benchmark_algorithm(
            algorithm_name="AES",
            data=data,
            encrypt_function=aes_encrypt,
            decrypt_function=aes_decrypt,
            key=AES_KEY,
            warmup_runs=DEFAULT_WARMUP_RUNS,
            measured_runs=measured_runs
        )

        results.append(
            aes_result
        )

        # ----------------------------------------------------
        # DES
        # ----------------------------------------------------

        des_result = benchmark_algorithm(
            algorithm_name="DES",
            data=data,
            encrypt_function=des_encrypt,
            decrypt_function=des_decrypt,
            key=DES_KEY,
            warmup_runs=DEFAULT_WARMUP_RUNS,
            measured_runs=measured_runs
        )

        results.append(
            des_result
        )

    # ========================================================
    # OUTPUT
    # ========================================================

    print_results(results)

    save_results(results)

    generate_graphs(results)

    print_summary(results)

    print("\n" + "=" * 70)
    print("                  BENCHMARK COMPLETE")
    print("=" * 70)

    print(
        f"\nCSV file created:"
        f"\n  {CSV_FILE}"
    )

    print(
        "\nGraphs created in:"
        f"\n  {GRAPH_DIRECTORY}/"
    )


# ============================================================
# PROGRAM ENTRY
# ============================================================

if __name__ == "__main__":
    main()