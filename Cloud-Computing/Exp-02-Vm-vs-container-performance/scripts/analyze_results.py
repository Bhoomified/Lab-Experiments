import os
import re
import csv

# =========================================================
# VM vs Container Performance Analysis
# Processes raw benchmark outputs into CSV files
# =========================================================

RAW_DIR = "results/raw"
PROCESSED_DIR = "results/processed"

os.makedirs(PROCESSED_DIR, exist_ok=True)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def read_file(path):
    """Read a text file safely."""
    with open(path, "r", errors="ignore") as file:
        return file.read()


def extract_float(pattern, text):
    """Extract the first floating-point number matching a regex."""
    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)

    if match:
        try:
            return float(match.group(1))
        except (ValueError, TypeError):
            return None

    return None


def extract_int(pattern, text):
    """Extract the first integer matching a regex."""
    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)

    if match:
        try:
            return int(match.group(1))
        except (ValueError, TypeError):
            return None

    return None


# =========================================================
# MEMORY ANALYSIS
# =========================================================

def process_memory():

    rows = []

    for environment in ["vm", "container"]:

        directory = os.path.join(
            RAW_DIR,
            "memory",
            environment
        )

        if not os.path.isdir(directory):
            print(f"WARNING: Missing directory: {directory}")
            continue

        for filename in sorted(os.listdir(directory)):

            if not filename.endswith(".txt"):
                continue

            path = os.path.join(directory, filename)
            text = read_file(path)

            # Extract run number
            run_match = re.search(
                r"run(\d+)",
                filename,
                re.IGNORECASE
            )

            run_number = (
                int(run_match.group(1))
                if run_match
                else None
            )

            # Total execution time
            total_time = extract_float(
                r"total time:\s*([0-9.]+)\s*s",
                text
            )

            # Total events
            total_events = extract_float(
                r"total number of events:\s*([0-9.]+)",
                text
            )

            # Calculate events per second from
            # actual measured values.
            events_per_second = None

            if (
                total_time is not None
                and total_time > 0
                and total_events is not None
            ):
                events_per_second = (
                    total_events / total_time
                )

            rows.append({
                "environment": environment,
                "run": run_number,
                "events_per_second": events_per_second,
                "total_time_s": total_time,
                "total_events": total_events
            })

    output_file = os.path.join(
        PROCESSED_DIR,
        "memory_results.csv"
    )

    with open(
        output_file,
        "w",
        newline=""
    ) as file:

        fieldnames = [
            "environment",
            "run",
            "events_per_second",
            "total_time_s",
            "total_events"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(rows)

    print(
        f"Memory results: {len(rows)} rows -> "
        f"{output_file}"
    )


# =========================================================
# DISK ANALYSIS
# =========================================================

def process_disk():

    rows = []

    for environment in ["vm", "container"]:

        directory = os.path.join(
            RAW_DIR,
            "disk",
            environment
        )

        if not os.path.isdir(directory):
            print(f"WARNING: Missing directory: {directory}")
            continue

        for filename in sorted(os.listdir(directory)):

            if not filename.endswith(".txt"):
                continue

            path = os.path.join(directory, filename)
            text = read_file(path)

            workload = filename.replace(
                ".txt",
                ""
            )

            # -------------------------------------------------
            # Bandwidth
            # fio generally reports:
            # bw=XXXXMiB/s
            # -------------------------------------------------

            bandwidth = extract_float(
                r"bw=([0-9.]+)\s*MiB/s",
                text
            )

            # If bandwidth is reported in KiB/s,
            # convert to MiB/s.
            if bandwidth is None:

                bandwidth_kib = extract_float(
                    r"bw=([0-9.]+)\s*KiB/s",
                    text
                )

                if bandwidth_kib is not None:
                    bandwidth = (
                        bandwidth_kib / 1024
                    )

            # -------------------------------------------------
            # IOPS
            # -------------------------------------------------

            iops = extract_float(
                r"IOPS=([0-9.]+)",
                text
            )

            # -------------------------------------------------
            # Average latency
            #
            # fio may report:
            # clat (usec): ... avg=123.45
            #
            # Convert microseconds -> milliseconds.
            # -------------------------------------------------

            latency_ms = None

            latency_us = extract_float(
                r"clat.*?avg=([0-9.]+)",
                text
            )

            if latency_us is not None:
                latency_ms = latency_us / 1000

            rows.append({
                "environment": environment,
                "workload": workload,
                "bandwidth_MiBps": bandwidth,
                "IOPS": iops,
                "latency_ms": latency_ms
            })

    output_file = os.path.join(
        PROCESSED_DIR,
        "disk_results.csv"
    )

    with open(
        output_file,
        "w",
        newline=""
    ) as file:

        fieldnames = [
            "environment",
            "workload",
            "bandwidth_MiBps",
            "IOPS",
            "latency_ms"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(rows)

    print(
        f"Disk results: {len(rows)} rows -> "
        f"{output_file}"
    )


# =========================================================
# FASTAPI / APACHE BENCHMARK ANALYSIS
# =========================================================

def process_api():

    rows = []

    for environment in ["vm", "container"]:

        directory = os.path.join(
            RAW_DIR,
            "api",
            environment
        )

        if not os.path.isdir(directory):
            print(f"WARNING: Missing directory: {directory}")
            continue

        benchmark_files = [
            "ab-health.txt",
            "ab-compute.txt"
        ]

        for filename in benchmark_files:

            path = os.path.join(
                directory,
                filename
            )

            if not os.path.isfile(path):
                print(
                    f"WARNING: Missing API result: {path}"
                )
                continue

            text = read_file(path)

            endpoint = filename.replace(
                "ab-",
                ""
            ).replace(
                ".txt",
                ""
            )

            # -------------------------------------------------
            # Requests per second
            # -------------------------------------------------

            requests_per_second = extract_float(
                r"Requests per second:\s*([0-9.]+)",
                text
            )

            # -------------------------------------------------
            # Time per request
            #
            # ApacheBench output contains:
            #
            # Time per request:       XX [ms] (mean)
            #
            # -------------------------------------------------

            time_per_request = extract_float(
                r"Time per request:\s*([0-9.]+)\s*\[ms\]",
                text
            )

            # -------------------------------------------------
            # Failed requests
            # -------------------------------------------------

            failed_requests = extract_int(
                r"Failed requests:\s*(\d+)",
                text
            )

            rows.append({
                "environment": environment,
                "endpoint": endpoint,
                "requests_per_second": requests_per_second,
                "time_per_request_ms": time_per_request,
                "failed_requests": failed_requests
            })

    output_file = os.path.join(
        PROCESSED_DIR,
        "api_results.csv"
    )

    with open(
        output_file,
        "w",
        newline=""
    ) as file:

        fieldnames = [
            "environment",
            "endpoint",
            "requests_per_second",
            "time_per_request_ms",
            "failed_requests"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(rows)

    print(
        f"API results: {len(rows)} rows -> "
        f"{output_file}"
    )


# =========================================================
# MAIN
# =========================================================

def main():

    print()
    print("=" * 60)
    print("VM vs Container Performance - Result Processing")
    print("=" * 60)
    print()

    process_memory()
    process_disk()
    process_api()

    print()
    print("=" * 60)
    print("PROCESSING COMPLETE")
    print("=" * 60)
    print()
    print("Generated files:")
    print(
        "  results/processed/memory_results.csv"
    )
    print(
        "  results/processed/disk_results.csv"
    )
    print(
        "  results/processed/api_results.csv"
    )
    print()


if __name__ == "__main__":
    main()
