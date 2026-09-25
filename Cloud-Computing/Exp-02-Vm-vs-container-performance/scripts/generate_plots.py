import os
import pandas as pd
import matplotlib.pyplot as plt

# =========================================================
# VM vs Container Performance
# Generate comparison graphs from processed CSV results
# =========================================================

PROCESSED_DIR = "results/processed"
FIGURES_DIR = "results/figures"

os.makedirs(FIGURES_DIR, exist_ok=True)


# =========================================================
# 1. MEMORY PERFORMANCE
# =========================================================

memory_file = os.path.join(
    PROCESSED_DIR,
    "memory_results.csv"
)

memory = pd.read_csv(memory_file)

memory_summary = (
    memory
    .groupby("environment")["events_per_second"]
    .mean()
)

plt.figure(figsize=(7, 5))

memory_summary.plot(
    kind="bar"
)

plt.title("Memory Performance: VM vs Container")
plt.xlabel("Environment")
plt.ylabel("Average Events per Second")
plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    os.path.join(
        FIGURES_DIR,
        "memory_comparison.png"
    ),
    dpi=300
)

plt.close()


# =========================================================
# 2. DISK BANDWIDTH
# =========================================================

disk_file = os.path.join(
    PROCESSED_DIR,
    "disk_results.csv"
)

disk = pd.read_csv(disk_file)

bandwidth = disk.pivot(
    index="workload",
    columns="environment",
    values="bandwidth_MiBps"
)

plt.figure(figsize=(9, 5))

bandwidth.plot(
    kind="bar",
    ax=plt.gca()
)

plt.title("Disk Bandwidth: VM vs Container")
plt.xlabel("Disk Workload")
plt.ylabel("Bandwidth (MiB/s)")
plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    os.path.join(
        FIGURES_DIR,
        "disk_bandwidth_comparison.png"
    ),
    dpi=300
)

plt.close()


# =========================================================
# 3. DISK IOPS
# =========================================================

iops = disk.pivot(
    index="workload",
    columns="environment",
    values="IOPS"
)

plt.figure(figsize=(9, 5))

iops.plot(
    kind="bar",
    ax=plt.gca()
)

plt.title("Disk IOPS: VM vs Container")
plt.xlabel("Disk Workload")
plt.ylabel("IOPS")
plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    os.path.join(
        FIGURES_DIR,
        "disk_iops_comparison.png"
    ),
    dpi=300
)

plt.close()


# =========================================================
# 4. FASTAPI PERFORMANCE
# =========================================================

api_file = os.path.join(
    PROCESSED_DIR,
    "api_results.csv"
)

api = pd.read_csv(api_file)

requests = api.pivot(
    index="endpoint",
    columns="environment",
    values="requests_per_second"
)

plt.figure(figsize=(8, 5))

requests.plot(
    kind="bar",
    ax=plt.gca()
)

plt.title("FastAPI Performance: VM vs Container")
plt.xlabel("Endpoint")
plt.ylabel("Requests per Second")
plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    os.path.join(
        FIGURES_DIR,
        "api_requests_per_second.png"
    ),
    dpi=300
)

plt.close()


# =========================================================
# COMPLETE
# =========================================================

print()
print("=" * 60)
print("GRAPH GENERATION COMPLETE")
print("=" * 60)
print()
print("Generated figures:")

print(
    "  results/figures/memory_comparison.png"
)

print(
    "  results/figures/disk_bandwidth_comparison.png"
)

print(
    "  results/figures/disk_iops_comparison.png"
)

print(
    "  results/figures/api_requests_per_second.png"
)

print()

