# Performance Analysis of Virtual Machines and Containers

## Abstract

This project presents a practical performance analysis of a virtual machine (VM) environment and a Docker container environment under controlled workloads. The experiments were conducted on a MacBook M3 host using UTM to run Ubuntu 24.04.

The comparison covers CPU baseline performance, memory performance, disk I/O performance, and application-level performance using a FastAPI application. The VM and Docker workloads were executed inside the same Ubuntu environment, with Docker constrained to the same 2-CPU and 3-GB-memory resource limits used for the controlled comparison.

All measured benchmark outputs were preserved as raw text files. The results were then processed into CSV files and comparative graphs to support analysis and reproducibility.

---

## 1. Objectives

The objectives of this experiment are:

- To compare VM and container performance under controlled workloads.
- To measure CPU performance using Sysbench.
- To measure memory performance using repeated Sysbench runs.
- To evaluate sequential and random disk I/O using fio.
- To evaluate application-level performance using a FastAPI application.
- To preserve raw benchmark outputs for reproducibility.
- To process benchmark outputs into structured CSV files.
- To generate graphs for visual comparison of measured results.
- To document the experimental environment, methodology, results, and limitations.

---

## 2. Research Questions

The experiment investigates the following questions:

1. How does memory performance differ between the VM and Docker container environments?
2. How does disk I/O performance vary between sequential and random workloads?
3. How does the FastAPI application perform in the VM and Docker environments?
4. What performance differences are observed when the container is given controlled CPU and memory limits comparable to the VM configuration?

---

## 3. Experimental Environment

### 3.1 Host Machine

| Component | Configuration |
|---|---|
| Host machine | MacBook M3 |
| Virtualization software | UTM |
| Guest operating system | Ubuntu 24.04 |
| VM CPU allocation | 2 vCPU |
| VM memory allocation | 3 GB RAM |
| Virtual disk | Approximately 54 GB |

### 3.2 Docker Environment

Docker was installed and executed inside the Ubuntu 24.04 VM.

The container was run with the following resource limits:

| Resource | Docker Limit |
|---|---:|
| CPUs | 2 |
| Memory | 3 GB |

This allowed the Docker workloads to be tested under controlled CPU and memory limits inside the same Ubuntu VM.

---

## 4. Architecture

The experimental setup can be summarized as follows:

```text
                         MacBook M3
                             |
                             v
                           UTM
                             |
                             v
                    Ubuntu 24.04 VM
                    2 vCPU / 3 GB RAM
                             |
                 +-----------+-----------+
                 |                       |
                 v                       v
        Native VM Environment      Docker Container
                 |                       |
                 +-----------+-----------+
                             |
                             v
                    Common Workloads
                             |
          +------------------+------------------+
          |                  |                  |
          v                  v                  v
       Memory            Disk I/O           FastAPI
      Sysbench             fio              Apache ab
          |                  |                  |
          +------------------+------------------+
                             |
                             v
                       Raw Results
                             |
                             v
                     Processed CSV Files
                             |
                             v
                    Comparison Graphs
```

A detailed architecture diagram is available at:

```text
docs/architecture.png
```

---

## 5. Methodology

The experiments were conducted inside the Ubuntu 24.04 VM.

The VM environment was benchmarked directly. Docker workloads were executed inside the same Ubuntu VM using controlled CPU and memory limits.

The implemented workload categories were:

- CPU baseline
- Memory
- Disk I/O
- FastAPI application

Raw benchmark output was stored under:

```text
results/raw/
```

The raw results were processed using:

```text
scripts/analyze_results.py
```

The processed CSV files were generated under:

```text
results/processed/
```

Comparison graphs were generated using:

```text
scripts/generate_plots.py
```

and stored under:

```text
results/figures/
```

The methodology and experimental procedure are additionally documented in:

```text
docs/methodology.md
```

---

# 6. CPU Experiment

## 6.1 Tool

Sysbench 1.0.20 was used for the CPU benchmark.

The recorded benchmark configuration included:

- Number of threads: 4
- Prime number limit: 20000
- Test duration: approximately 30 seconds

## 6.2 Result

| Metric | Measured Value |
|---|---:|
| Sysbench version | 1.0.20 |
| Threads | 4 |
| Prime number limit | 20000 |
| Total time | 30.0005 s |
| Total events | 146649 |
| CPU speed | 4888.02 events/sec |
| Minimum latency | 0.40 ms |
| Average latency | 0.82 ms |
| Maximum latency | 19.79 ms |
| 95th percentile latency | 2.43 ms |

The raw CPU output is preserved at:

```text
results/raw/baseline/cpu.txt
```

### Note

The CPU result in this project is a baseline measurement of the experimental environment. A separate processed VM-versus-container CPU comparison dataset was not collected.

---

# 7. Memory Experiment

## 7.1 Benchmark

Memory performance was measured using Sysbench.

The workload used:

```text
Memory block size: 1M
Total memory workload: 10G
Threads: 4
Runs per environment: 10
```

The primary processed metric was calculated as:

```text
Events per second = Total number of events / Total execution time
```

## 7.2 Results

### VM

| Run | Events/sec | Total Time (s) |
|---:|---:|---:|
| 1 | 44931.99 | 0.2279 |
| 2 | 49468.60 | 0.2070 |
| 3 | 45531.35 | 0.2249 |
| 4 | 47805.79 | 0.2142 |
| 5 | 48233.63 | 0.2123 |
| 6 | 45857.59 | 0.2233 |
| 7 | 48279.11 | 0.2121 |
| 8 | 45775.59 | 0.2237 |
| 9 | 49207.11 | 0.2081 |
| 10 | 45612.47 | 0.2245 |

### Docker Container

| Run | Events/sec | Total Time (s) |
|---:|---:|---:|
| 1 | 48484.85 | 0.2112 |
| 2 | 46230.25 | 0.2215 |
| 3 | 49468.60 | 0.2070 |
| 4 | 45490.89 | 0.2251 |
| 5 | 44872.92 | 0.2282 |
| 6 | 47872.84 | 0.2139 |
| 7 | 46439.91 | 0.2205 |
| 8 | 44444.44 | 0.2304 |
| 9 | 46609.01 | 0.2197 |
| 10 | 47123.79 | 0.2173 |

### Average

| Environment | Average Events/sec |
|---|---:|
| VM | 47070.32 |
| Docker Container | 46703.75 |

The measured averages were close for this memory workload.

The processed results are stored at:

```text
results/processed/memory_results.csv
```

The generated comparison graph is:

```text
results/figures/memory_comparison.png
```

The raw benchmark outputs are stored under:

```text
results/raw/memory/
```

---

# 8. Disk I/O Experiment

## 8.1 Tool

Disk I/O performance was measured using fio.

The experiment included four workloads:

1. Sequential read
2. Sequential write
3. Random read
4. Random write

The sequential workloads used a 1 MiB block size, while the random workloads used a 4 KiB block size.

The benchmark outputs include:

- Bandwidth
- IOPS
- Completion latency

## 8.2 Results

| Environment | Workload | Bandwidth (MiB/s) | IOPS | Latency (ms) |
|---|---|---:|---:|---:|
| VM | Random Read | 1777.0 | 1776 | 0.56201 |
| VM | Random Write | 3740.0 | 3740 | 0.25885 |
| VM | Sequential Read | 2831.0 | 2831 | 0.35252 |
| VM | Sequential Write | 3061.0 | 3061 | 0.31767 |
| Container | Random Read | 34.4 | 8813 | 0.11292 |
| Container | Random Write | 32.0 | 8183 | 0.12160 |
| Container | Sequential Read | 4122.0 | 4122 | 0.24196 |
| Container | Sequential Write | 3324.0 | 3324 | 0.29255 |

### Important observation

The random read and random write workloads used 4 KiB blocks. Therefore, bandwidth and IOPS must be interpreted together.

For example, a high IOPS value can coexist with a comparatively low MiB/s value when the individual I/O operations are small.

The measured results also show that the behavior differed substantially between workload types, particularly for the random workloads.

## 8.3 Generated Graphs

Disk bandwidth comparison:

```text
results/figures/disk_bandwidth_comparison.png
```

Disk IOPS comparison:

```text
results/figures/disk_iops_comparison.png
```

Processed disk results:

```text
results/processed/disk_results.csv
```

Raw fio results:

```text
results/raw/disk/
```

---

# 9. FastAPI Application Experiment

## 9.1 Application

A lightweight FastAPI application was implemented to evaluate application-level performance.

The application provides the following endpoints:

```text
/health
/compute
/memory
```

### `/health`

Returns a simple health status response.

### `/compute`

Performs a computational workload by calculating the sum of squared integers over a fixed range.

### `/memory`

Creates a list containing one million elements and returns the number of elements.

The application source code is located at:

```text
api/main.py
```

Dependencies are specified in:

```text
api/requirements.txt
```

The Docker image configuration is:

```text
api/Dockerfile
```

## 9.2 Benchmarking

Apache Benchmark (`ab`) was used to generate requests and measure application performance.

The recorded metrics include:

- Requests per second
- Time per request
- Failed requests

## 9.3 Results

| Environment | Endpoint | Requests/sec | Time/request | Failed Requests |
|---|---|---:|---:|---:|
| VM | `/health` | 2853.93 | 35.039 ms | 0 |
| VM | `/compute` | 20.09 | 497.878 ms | 0 |
| Docker | `/health` | 2230.52 | 44.833 ms | 0 |
| Docker | `/compute` | 18.68 | 535.200 ms | 0 |

No failed requests were recorded in the tested Apache Benchmark runs.

The processed API results are stored at:

```text
results/processed/api_results.csv
```

The generated graph is:

```text
results/figures/api_requests_per_second.png
```

Raw API outputs are stored under:

```text
results/raw/api/
```

---

# 10. Results Summary

The following table summarizes the main measured results.

| Experiment | Environment | Measured Result |
|---|---|---:|
| CPU baseline | VM | 4888.02 events/sec |
| Memory | VM | 47070.32 average events/sec |
| Memory | Docker | 46703.75 average events/sec |
| Sequential Read | VM | 2831 MiB/s |
| Sequential Read | Docker | 4122 MiB/s |
| Sequential Write | VM | 3061 MiB/s |
| Sequential Write | Docker | 3324 MiB/s |
| Random Read | VM | 1777 MiB/s |
| Random Read | Docker | 34.4 MiB/s |
| Random Write | VM | 3740 MiB/s |
| Random Write | Docker | 32.0 MiB/s |
| FastAPI `/health` | VM | 2853.93 requests/sec |
| FastAPI `/health` | Docker | 2230.52 requests/sec |
| FastAPI `/compute` | VM | 20.09 requests/sec |
| FastAPI `/compute` | Docker | 18.68 requests/sec |

---

# 11. Analysis and Discussion

## 11.1 Memory

The ten memory runs produced relatively close average event rates:

```text
VM:        47070.32 events/sec
Container: 46703.75 events/sec
```

The difference between the measured averages is small relative to the overall throughput of the workload. The individual runs also show normal variation between repeated executions.

## 11.2 Disk I/O

Disk performance varied considerably depending on the workload.

For sequential read, the measured bandwidth was:

```text
VM:        2831 MiB/s
Container: 4122 MiB/s
```

For sequential write:

```text
VM:        3061 MiB/s
Container: 3324 MiB/s
```

The random workloads produced a very different pattern. The measured random-read bandwidth was:

```text
VM:        1777 MiB/s
Container: 34.4 MiB/s
```

and random-write bandwidth was:

```text
VM:        3740 MiB/s
Container: 32.0 MiB/s
```

At the same time, the container recorded higher IOPS for the random workloads:

```text
Random Read:
VM:        1776 IOPS
Container: 8813 IOPS

Random Write:
VM:        3740 IOPS
Container: 8183 IOPS
```

This illustrates why IOPS and bandwidth should be interpreted together, especially when different block sizes are involved.

## 11.3 FastAPI

The application-level benchmark showed measurable differences between the two environments.

For the lightweight `/health` endpoint:

```text
VM:        2853.93 requests/sec
Container: 2230.52 requests/sec
```

For the computational `/compute` endpoint:

```text
VM:        20.09 requests/sec
Container: 18.68 requests/sec
```

Both environments recorded zero failed requests for the measured benchmark runs.

The application results therefore show that the observed difference was present not only at the low-level benchmark layer but also at the application level for this particular workload.

## 11.4 Overall Interpretation

The collected measurements do not show one uniform performance behavior across every workload.

Memory performance was relatively close between the environments, while disk behavior varied considerably by I/O pattern. The FastAPI workload also produced measurable differences in request throughput and response time.

These observations apply specifically to the experimental configuration used in this project. They should not be interpreted as universal performance characteristics of all virtual machines or Docker containers.

---

# 12. Limitations

The following limitations apply to this experiment:

- The experiment was performed on a single physical host.
- The VM used one fixed CPU and memory configuration.
- Docker was tested using one controlled CPU and memory configuration.
- Disk performance is influenced by the underlying virtualized storage system.
- The CPU measurement was collected as a baseline rather than as a complete VM-versus-container CPU comparison.
- The experiments were not repeated across multiple physical machines.
- Network benchmarking was not included in the implemented experiment.
- Startup-time benchmarking was not included.
- Scalability benchmarking was not included.
- Results can vary with hardware, operating-system versions, virtualization configuration, Docker versions, storage configuration, background processes, and system load.
- The results represent measurements from the selected workloads and parameters rather than all possible workloads.

---

# 13. Reproducibility

The project preserves both raw and processed results.

### Raw Results

```text
results/raw/
```

contains the original benchmark outputs.

### Processed Results

```text
results/processed/
```

contains:

```text
memory_results.csv
disk_results.csv
api_results.csv
```

### Figures

```text
results/figures/
```

contains:

```text
memory_comparison.png
disk_bandwidth_comparison.png
disk_iops_comparison.png
api_requests_per_second.png
```

### Processing Scripts

The benchmark outputs can be processed using:

```bash
python3 scripts/analyze_results.py
```

The graphs can be regenerated using:

```bash
python3 scripts/generate_plots.py
```

The exact benchmark commands and experimental procedure are documented in:

```text
docs/methodology.md
```

---

# 14. Project Structure

```text
vm-vs-container-performance/
│
├── README.md
├── .gitignore
│
├── api/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
│
├── docker/
│   └── Dockerfile
│
├── docs/
│   ├── architecture.png
│   ├── cpu-info.txt
│   ├── kernel-info.txt
│   ├── memory-info.txt
│   ├── methodology.md
│   └── storage-info.txt
│
├── results/
│   ├── raw/
│   │   ├── api/
│   │   ├── baseline/
│   │   ├── disk/
│   │   └── memory/
│   │
│   ├── processed/
│   │   ├── api_results.csv
│   │   ├── disk_results.csv
│   │   └── memory_results.csv
│   │
│   └── figures/
│       ├── api_requests_per_second.png
│       ├── disk_bandwidth_comparison.png
│       ├── disk_iops_comparison.png
│       └── memory_comparison.png
│
└── scripts/
    ├── analyze_results.py
    └── generate_plots.py
```

---

# 15. Conclusion

This project provides a practical comparison of VM and Docker execution under selected CPU, memory, disk I/O, and application workloads.

The measurements show that performance depends on the workload being executed. Memory throughput was relatively close between the VM and container environments, while disk behavior differed significantly between sequential and random access patterns. The FastAPI application also showed measurable differences in requests per second and request latency between the two environments.

The experiment demonstrates the importance of evaluating virtualization and containerization using workload-specific measurements rather than relying on a single benchmark.

Because the raw benchmark outputs, processed CSV files, analysis scripts, graphs, and experimental documentation are preserved, the experiment can be reviewed and reproduced using the same methodology and configuration.

---

# 16. Future Work

The experiment can be extended in several ways:

- Perform a dedicated CPU comparison using identical VM and container CPU workloads.
- Repeat experiments with different VM CPU and memory allocations.
- Evaluate additional Docker CPU and memory limits.
- Add network benchmarking using iperf3.
- Measure VM and container startup times.
- Evaluate scalability under increasing request loads.
- Increase the number of repetitions for statistical analysis.
- Calculate confidence intervals and additional statistical measures.
- Repeat the experiment on different host hardware.
- Compare additional container runtimes or virtualization technologies.

---

## Author

**Cloud Computing Laboratory**

**Experiment: Performance Analysis of Virtual Machines and Containers**
