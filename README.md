# 5th Semester Lab Experiments

This repository contains my 5th semester laboratory experiments, implementations, outputs, screenshots, and learning notes across all practical lab courses.

---

## 📌 Overview

| Property | Details |
| :--- | :--- |
| **Semester** | 5th Semester (B.Tech / B.E. Computer Science & Engineering) |
| **Purpose** | A comprehensive record of laboratory practicals, source implementations, performance analysis, benchmark observations, and learning documentation. |
| **Status** | 🔄 Active / In Progress |

---

## 📚 Courses & Curricula

### ☁️ Cloud Computing
Experiments exploring cloud computing architectures, bare-metal and hosted virtualization, hypervisors (Type-1 & Type-2), virtual machine lifecycle management, cloud storage configuration, and containerized workload performance.

- **Primary Stack / Tools:** Linux, KVM/QEMU, VirtualBox, Docker, OpenStack / AWS / GCP CLI, CloudSim.
- **Directory:** [`Cloud-Computing/`](./Cloud-Computing/)

### ⚡ Parallel Computing & GPU
Experiments focused on high-performance parallel programming, multi-core CPU threading, GPU hardware architecture, CUDA kernel development, synchronization primitives, memory hierarchy optimization, and parallel speedup analysis.

- **Primary Stack / Tools:** C/C++, OpenMP, MPI, NVIDIA CUDA Toolkit, `nvcc`, Nsight Systems/Compute, GNU Gprof.
- **Directory:** [`Parallel-Computing-GPU/`](./Parallel-Computing-GPU/)

---

## 📂 Repository Structure

```text
Lab-Experiments/
│
├── Cloud-Computing/
│   ├── README.md
│   ├── Experiment-01/
│   ├── Experiment-02/
│   ├── Experiment-03/
│   └── ...
│
├── Parallel-Computing-GPU/
│   ├── README.md
│   ├── Experiment-01/
│   ├── Experiment-02/
│   ├── Experiment-03/
│   └── ...
│
└── README.md
```

---

## 🧪 Laboratory Progress & Status

### ☁️ Cloud Computing Practicals

| Experiment | Topic / Title | Status |
| :---: | :--- | :---: |
| **01** | Virtualization & Hypervisor Setup (Type-1 / Type-2) | 🔄 In Progress |
| **02** | Virtual Machine Provisioning, Networking & Resource Slicing | ⏳ Pending |
| **03** | Cloud Storage & Object Store Configuration | ⏳ Pending |
| **04** | Containerization & Workload Orchestration | ⏳ Pending |

### ⚡ Parallel Computing & GPU Practicals

| Experiment | Topic / Title | Status |
| :---: | :--- | :---: |
| **01** | Multi-threaded Parallel Execution with OpenMP | 🔄 In Progress |
| **02** | Distributed Memory Architecture & Communication via MPI | ⏳ Pending |
| **03** | NVIDIA CUDA Kernel Programming & Thread Hierarchy | ⏳ Pending |
| **04** | Shared vs. Global GPU Memory Performance Profiling | ⏳ Pending |

---

## 📑 Experiment Standard Structure

Each experiment directory follows a consistent documentation layout:

- **`Aim`** — Core objective and expected learning outcome.
- **`Requirements`** — Hardware, operating system, compilers, drivers, and software libraries needed.
- **`Theory`** — Conceptual foundations, mathematical formulations, and architectural diagrams.
- **`Procedure & Configuration`** — Step-by-step setup, configuration steps, and environment tuning.
- **`Implementation`** — Commented source code, build scripts, and execution commands.
- **`Screenshots & Outputs`** — Terminal logs, verification screenshots, and captured output files.
- **`Observations & Performance Analysis`** — Speedup curves, memory bandwidth utilization, or virtualization overhead.
- **`Conclusion`** — Key takeaways, limitations encountered, and potential optimizations.

---

## 🛠️ Environment & Prerequisites

Ensure the following toolchains are installed to replicate these experiments:

- **Operating System:** Ubuntu 22.04 LTS / Linux or WSL2 (with GPU passthrough enabled)
- **Compiler Support:** `gcc`/`g++` (v11+), `nvcc` (CUDA 12.x+)
- **Virtualization Support:** Intel VT-x / AMD-V enabled in BIOS/UEFI

---

## 👤 Author & Academic Integrity

- **Author:** 5th Semester CSE Student  
- **Note:** All lab code and documentation are intended for educational and reference purposes in accordance with academic integrity guidelines.