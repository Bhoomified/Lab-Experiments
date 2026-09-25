# Experimental Methodology

## Objective

The objective of this experiment is to compare the performance of a Virtual Machine and a Docker container under controlled and equivalent workloads.

## Experimental Environment

### Host

- Host machine: Mac M3
- Virtualization software: UTM

### Virtual Machine

- Operating System: Ubuntu 24.04 LTS
- vCPU: 2
- RAM: 3 GB
- Virtual disk: approximately 54 GB

### Container

- Runtime: Docker
- Base image: Ubuntu 24.04 / Python 3.12-slim for the FastAPI application
- CPU limit: 2 CPUs
- Memory limit: 3 GB

## Experiments Performed

The following experiments were completed:

1. Baseline CPU measurement
2. Memory performance
3. Disk I/O performance
4. FastAPI application performance

Network, startup-time, and scalability experiments were not included in this implementation.

## Memory Methodology

The Sysbench memory workload used:

- Block size: 1 MiB
- Total memory workload: 10 GiB
- Threads: 4
- Repetitions: 10

The same workload was executed for the VM and Docker container.

## Disk I/O Methodology

The disk benchmark was performed using fio.

Four workloads were tested:

- Sequential write
- Sequential read
- Random read
- Random write

Sequential workloads used:

- Block size: 1 MiB
- File size: 2 GiB
- I/O depth: 16
- Direct I/O: enabled
- Runtime: 30 seconds

Random workloads used:

- Block size: 4 KiB
- File size: 2 GiB
- I/O depth: 16
- Direct I/O: enabled
- Runtime: 30 seconds

The same benchmark parameters were used for VM and Docker.

## FastAPI Methodology

A FastAPI application was implemented with three endpoints:

- `/health`
- `/compute`
- `/memory`

The application was first executed directly inside the Ubuntu VM and then inside a Docker container.

Apache Benchmark was used for application performance testing.

### Health workload

- Requests: 10,000
- Concurrency: 100

### Compute workload

- Requests: 1,000
- Concurrency: 10

## Raw Data

Complete benchmark outputs are preserved under:

`results/raw/`

Raw measurements are not modified.
