import csv
import json
import subprocess
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from statistics import mean


API_URL = "http://127.0.0.1:8001/books"

WORKLOADS = {
    "W1": 1,
    "W2": 2,
    "W3": 4,
    "W4": 8,
    "W5": 16,
}

REQUESTS_PER_WORKLOAD = 200

CONTAINER_NAMES = [
    "microservice_library_management-book_service-1",
    "microservice_library_management-member_service-1",
    "microservice_library_management-loan_service-1",
]


def send_request():
    start = time.perf_counter()

    try:
        with urllib.request.urlopen(API_URL, timeout=10) as response:
            response.read()
            status = response.status

        elapsed = (time.perf_counter() - start) * 1000

        return {
            "success": 200 <= status < 300,
            "response_time": elapsed,
        }

    except Exception:
        elapsed = (time.perf_counter() - start) * 1000

        return {
            "success": False,
            "response_time": elapsed,
        }


def get_docker_stats():
    stats = {}

    try:
        command = [
            "docker",
            "stats",
            "--no-stream",
            "--format",
            "{{json .}}",
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10,
        )

        for line in result.stdout.splitlines():

            if not line.strip():
                continue

            try:
                data = json.loads(line)

                name = data.get("Name", "")

                if name not in CONTAINER_NAMES:
                    continue

                cpu_text = data.get("CPUPerc", "0%")
                memory_text = data.get("MemUsage", "0MiB / 0MiB")

                cpu = float(cpu_text.replace("%", "").strip())

                memory_used = memory_text.split("/")[0].strip()

                if "GiB" in memory_used:
                    memory = float(
                        memory_used.replace("GiB", "").strip()
                    ) * 1024
                elif "MiB" in memory_used:
                    memory = float(
                        memory_used.replace("MiB", "").strip()
                    )
                elif "KiB" in memory_used:
                    memory = float(
                        memory_used.replace("KiB", "").strip()
                    ) / 1024
                else:
                    memory = 0

                stats[name] = {
                    "cpu": cpu,
                    "memory": memory,
                }

            except Exception:
                continue

    except Exception:
        pass

    return stats


def collect_stats_during_workload(executor):
    stats_samples = []

    futures = [
        executor.submit(send_request)
        for _ in range(REQUESTS_PER_WORKLOAD)
    ]

    while True:

        completed = sum(
            1 for future in futures
            if future.done()
        )

        stats = get_docker_stats()

        if stats:
            stats_samples.append(stats)

        if completed >= REQUESTS_PER_WORKLOAD:
            break

        time.sleep(0.2)

    request_results = [
        future.result()
        for future in as_completed(futures)
    ]

    return request_results, stats_samples


def calculate_container_averages(stat_samples):

    container_cpu = {}
    container_memory = {}

    for container in CONTAINER_NAMES:

        cpu_values = []
        memory_values = []

        for sample in stat_samples:

            if container in sample:
                cpu_values.append(sample[container]["cpu"])
                memory_values.append(
                    sample[container]["memory"]
                )

        container_cpu[container] = (
            mean(cpu_values) if cpu_values else 0
        )

        container_memory[container] = (
            mean(memory_values)
            if memory_values
            else 0
        )

    return container_cpu, container_memory


def main():

    print("=" * 70)
    print("LIBRARY MANAGEMENT MICROSERVICE LOAD TEST")
    print("=" * 70)

    print(f"\nAPI: {API_URL}")
    print(
        f"Requests per workload: "
        f"{REQUESTS_PER_WORKLOAD}"
    )

    print("\nChecking API...")

    try:

        with urllib.request.urlopen(
            API_URL,
            timeout=10
        ) as response:

            if response.status == 200:
                print("API is reachable successfully.")
            else:
                print(
                    f"API returned status "
                    f"{response.status}"
                )

    except Exception as error:

        print("\nERROR: API is not reachable.")
        print(error)

        print(
            "\nMake sure Docker Compose is running:"
        )
        print("docker compose up -d")

        return

    print("\nStarting workload tests...\n")

    all_results = []

    for workload, concurrency in WORKLOADS.items():

        print("-" * 70)
        print(
            f"{workload} - "
            f"Concurrency: {concurrency}"
        )
        print("-" * 70)

        # Warm-up requests
        for _ in range(10):
            send_request()

        time.sleep(1)

        start_time = time.perf_counter()

        with ThreadPoolExecutor(
            max_workers=concurrency
        ) as executor:

            request_results, stat_samples = (
                collect_stats_during_workload(
                    executor
                )
            )

        total_time = (
            time.perf_counter() - start_time
        )

        successful = sum(
            1
            for result in request_results
            if result["success"]
        )

        failed = (
            len(request_results) - successful
        )

        response_times = [
            result["response_time"]
            for result in request_results
        ]

        average_response_time = mean(
            response_times
        )

        throughput = (
            successful / total_time
        )

        container_cpu, container_memory = (
            calculate_container_averages(
                stat_samples
            )
        )

        book_cpu = container_cpu.get(
            "microservice_library_management-book_service-1",
            0,
        )

        member_cpu = container_cpu.get(
            "microservice_library_management-member_service-1",
            0,
        )

        loan_cpu = container_cpu.get(
            "microservice_library_management-loan_service-1",
            0,
        )

        book_memory = container_memory.get(
            "microservice_library_management-book_service-1",
            0,
        )

        member_memory = container_memory.get(
            "microservice_library_management-member_service-1",
            0,
        )

        loan_memory = container_memory.get(
            "microservice_library_management-loan_service-1",
            0,
        )

        average_cpu = mean([
            book_cpu,
            member_cpu,
            loan_cpu,
        ])

        average_memory = mean([
            book_memory,
            member_memory,
            loan_memory,
        ])

        result = {
            "workload": workload,
            "concurrency": concurrency,
            "response_time_ms": round(
                average_response_time,
                2
            ),
            "throughput_requests_per_second": round(
                throughput,
                2
            ),
            "successful_requests": successful,
            "failed_requests": failed,
            "cpu_percent": round(
                average_cpu,
                2
            ),
            "memory_mb": round(
                average_memory,
                2
            ),
            "book_cpu_percent": round(
                book_cpu,
                2
            ),
            "member_cpu_percent": round(
                member_cpu,
                2
            ),
            "loan_cpu_percent": round(
                loan_cpu,
                2
            ),
            "book_memory_mb": round(
                book_memory,
                2
            ),
            "member_memory_mb": round(
                member_memory,
                2
            ),
            "loan_memory_mb": round(
                loan_memory,
                2
            ),
        }

        all_results.append(result)

        print(
            f"Average Response Time : "
            f"{average_response_time:.2f} ms"
        )

        print(
            f"Throughput            : "
            f"{throughput:.2f} requests/sec"
        )

        print(
            f"Successful Requests   : "
            f"{successful}"
        )

        print(
            f"Failed Requests       : "
            f"{failed}"
        )

        print(
            f"Average CPU           : "
            f"{average_cpu:.2f}%"
        )

        print(
            f"Average Memory        : "
            f"{average_memory:.2f} MB"
        )

        print("\nContainer CPU:")

        print(
            f"  Book Service   : "
            f"{book_cpu:.2f}%"
        )

        print(
            f"  Member Service : "
            f"{member_cpu:.2f}%"
        )

        print(
            f"  Loan Service   : "
            f"{loan_cpu:.2f}%"
        )

        print("\nContainer Memory:")

        print(
            f"  Book Service   : "
            f"{book_memory:.2f} MB"
        )

        print(
            f"  Member Service : "
            f"{member_memory:.2f} MB"
        )

        print(
            f"  Loan Service   : "
            f"{loan_memory:.2f} MB"
        )

        time.sleep(2)

    output_file = "performance_results.csv"

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=all_results[0].keys(),
        )

        writer.writeheader()
        writer.writerows(all_results)

    print("\n" + "=" * 70)
    print("LOAD TEST COMPLETED")
    print("=" * 70)

    print(
        f"\nResults saved to: "
        f"{output_file}"
    )

    print("\nObservation Table:")
    print()

    print(
        "Workload | Concurrency | Response(ms) | "
        "Throughput | Failed | CPU(%) | Memory(MB)"
    )

    print("-" * 90)

    for result in all_results:

        print(
            f"{result['workload']:8} | "
            f"{result['concurrency']:11} | "
            f"{result['response_time_ms']:13.2f} | "
            f"{result['throughput_requests_per_second']:10.2f} | "
            f"{result['failed_requests']:6} | "
            f"{result['cpu_percent']:6.2f} | "
            f"{result['memory_mb']:9.2f}"
        )


if __name__ == "__main__":
    main()