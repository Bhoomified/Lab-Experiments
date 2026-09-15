# CC Experiment 01 --- Hypervisor Analysis

## Type-1 Proxmox VE vs Type-2 VMware Workstation



---

## 📌 Experiment Overview

This experiment studies the performance of virtual machines running on\
two different hypervisor architectures:

- **Type-1 Hypervisor:** Proxmox VE
- **Type-2 Hypervisor:** VMware Workstation

Ubuntu is used as the guest operating system in both environments. The\
virtual machines are configured with the same intended hardware\
resources, and CPU performance is evaluated using the **Sysbench CPU**\
**benchmark**.

The purpose is to understand the practical performance characteristics\
of Type-1 and Type-2 virtualization and compare their CPU benchmark\
results.

---

## 🎯 Objectives

The objectives of this experiment are:

1. To understand the difference between Type-1 and Type-2 hypervisors.
2. To create and configure an Ubuntu virtual machine using Proxmox VE.
3. To create and configure an Ubuntu virtual machine using VMware\
   Workstation.
4. To maintain an equivalent virtual hardware configuration for both\
   environments.
5. To perform CPU benchmarking using Sysbench.
6. To record execution time, total events, events per second, and\
   latency.
7. To compare the measured performance of both virtualization\
   approaches.
8. To observe virtual machine resource utilization.

---

# 🖥️ Hypervisor Architectures

## Type-1 Hypervisor --- Proxmox VE

Proxmox VE is used as the Type-1 hypervisor in this experiment.

A Type-1 hypervisor runs directly on the physical host hardware rather\
than depending on a conventional host operating system.

### Proxmox VM Configuration

Resource                 Configuration

---

Hypervisor               Proxmox VE\
Hypervisor Type          Type-1\
Guest Operating System   Ubuntu\
CPU Allocation           2 vCPU\
Memory Allocation        2 GB RAM\
Disk Allocation          20 GB

---

## Type-2 Hypervisor --- VMware Workstation

VMware Workstation is used as the Type-2 hypervisor.

A Type-2 hypervisor operates on top of a host operating system and\
provides virtualization services to guest virtual machines.

### VMware VM Configuration

Resource                 Configuration

---

Hypervisor               VMware Workstation\
Hypervisor Type          Type-2\
Guest Operating System   Ubuntu\
CPU Allocation           2 vCPU\
Memory Allocation        2 GB RAM\
Disk Allocation          20 GB\
Network Configuration    NAT

---

# ⚙️ Standard VM Configuration

To make the performance comparison meaningful, both virtual machines are\
intended to use the same basic resource allocation.

Resource        Value

---

Guest OS        Ubuntu\
CPU             2 vCPU\
RAM             2 GB\
Disk            20 GB\
Benchmark       Sysbench CPU\
CPU Benchmark   `sysbench cpu --cpu-max-prime=20000 run`

---

# 🧪 Benchmark Methodology

The CPU benchmark used in the experiment is:

```bash
sysbench cpu --cpu-max-prime=20000 run
```

The benchmark performs CPU-intensive prime-number calculations up to a\
limit of **20,000**.

The following measurements are recorded:

- Total execution time
- Total number of events
- Events per second
- Minimum latency
- Average latency
- Maximum latency
- 95th percentile latency

---

# 🟠 Part A --- Type-1 Hypervisor: Proxmox VE

## Proxmox VM

The Ubuntu virtual machine was created on the Proxmox VE environment\
using the standard experimental configuration.

### Configuration

Parameter          Value

---

Hypervisor         Proxmox VE\
Type               Type-1\
Operating System   Ubuntu\
CPU                2 vCPU\
Memory             2 GB\
Disk               20 GB

## Proxmox Benchmark Results

The Proxmox Sysbench benchmark values are currently unavailable.

They will be added when the benchmark is successfully obtained.

Metric                           Proxmox VE

---

Total Execution Time        **TO BE ADDED**\
Total Events                **TO BE ADDED**\
Events per Second           **TO BE ADDED**\
Minimum Latency             **TO BE ADDED**\
Average Latency             **TO BE ADDED**\
Maximum Latency             **TO BE ADDED**\
95th Percentile Latency     **TO BE ADDED**

### Proxmox Resource Monitoring

The experiment also requires observation of the VM resource utilization\
from the Proxmox VE interface.

Resource        Observation

---

CPU Usage       **TO BE ADDED**\
Memory Usage    **TO BE ADDED**\
Network Usage   **TO BE ADDED**\
Disk Usage      **TO BE ADDED**

> **Note:** No Proxmox performance or monitoring values have been\
> estimated. Missing values are explicitly marked as **TO BE ADDED**.

---

# 🔵 Part B --- Type-2 Hypervisor: VMware Workstation

## VMware VM

The Ubuntu virtual machine was configured under VMware Workstation using\
the intended equivalent resource allocation.

### Configuration

Parameter          Value

---

Hypervisor         VMware Workstation\
Type               Type-2\
Operating System   Ubuntu\
CPU                2 vCPU\
Memory             2 GB\
Disk               20 GB\
Network            NAT

---

## VMware Sysbench Configuration

The benchmark was executed using:

```bash
sysbench cpu --cpu-max-prime=20000 run
```

### Benchmark Parameters

Parameter                Value

---

Sysbench Version        1.0.20\
Benchmark                  CPU\
Prime Numbers Limit     20,000\
Number of Threads            1

---

## VMware Benchmark Results

The following results were obtained from the Ubuntu virtual machine\
running under VMware Workstation:

Performance Metric                  Result

---

Total Execution Time         **10.0006 s**\
Total Events                    **24,366**\
Events per Second             **2,436.05**\
Minimum Latency                **0.40 ms**\
Average Latency                **0.41 ms**\
Maximum Latency                **4.39 ms**\
95th Percentile Latency        **0.42 ms**\
Latency Sum                 **9992.75 ms**

### VMware Observation

The CPU benchmark completed in approximately **10 seconds**.

The VM processed **24,366 total events** and achieved a throughput of\
**2,436.05 events per second**.

The measured average latency was **0.41 ms**. The minimum latency was\
**0.40 ms**, while the maximum observed latency was **4.39 ms**. The\
95th percentile latency was **0.42 ms**.

---

# 📊 Performance Comparison

The final comparison uses the benchmark metrics specified for the\
experiment.

Parameter                Type-1: Proxmox VE   Type-2: VMware Workstation

---

Hypervisor Type                      Type-1                       Type-2\
Guest OS                             Ubuntu                       Ubuntu\
CPU                                  2 vCPU                       2 vCPU\
Memory                                 2 GB                         2 GB\
Disk                                  20 GB                        20 GB\
Total Execution Time        **TO BE ADDED**                **10.0006 s**\
Total Events                **TO BE ADDED**                   **24,366**\
Events per Second           **TO BE ADDED**                 **2,436.05**\
Average Latency             **TO BE ADDED**                  **0.41 ms**

> **Comparison status:** A final performance winner cannot be declared\
> until the corresponding Proxmox benchmark values are available.

---

# 📈 Analysis

## VMware Workstation

The VMware Workstation VM produced the following CPU benchmark\
measurements:

- **Execution Time:** 10.0006 seconds
- **Total Events:** 24,366
- **Events/Second:** 2,436.05
- **Average Latency:** 0.41 ms

These values provide the current Type-2 baseline for the experiment.

## Proxmox VE

The corresponding Proxmox benchmark measurements are currently\
unavailable.

Therefore, no numerical performance conclusion is made for Proxmox at\
this stage.

Once the Proxmox results are available, the following comparisons can be\
performed:

### Execution Time

The hypervisor with the lower execution time will have completed the\
same benchmark workload faster.

### Event Throughput

The hypervisor with the higher **events per second** value will\
demonstrate higher benchmark throughput for this workload.

### Average Latency

The hypervisor with the lower average latency will demonstrate lower\
average processing latency for the benchmark.

---

# 📝 Current Result

The Type-2 VMware Workstation experiment was successfully completed.

The recorded VMware CPU benchmark result is:

> **2,436.05 events per second**

with:

> **10.0006 seconds execution time**

and:

> **0.41 ms average latency**

The Type-1 Proxmox results are pending and are intentionally left as\
**TO BE ADDED**.

---

# 📷 Screenshot Evidence

All experiment screenshots are organized using the following structure:

```text
CC-Experiment-01-Hypervisor-Analysis/
│
├── screenshots/
│   │
│   ├── type1-proxmox/
│   │   ├── 01-proxmox-dashboard.png
│   │   ├── 02-proxmox-vm-configuration.png
│   │   ├── 03-proxmox-vm-running.png
│   │   ├── 04-proxmox-ubuntu-console.png
│   │   ├── 05-proxmox-system-configuration.png
│   │   ├── 06-proxmox-sysbench-result.png
│   │   └── 07-proxmox-resource-monitoring.png
│   │
│   ├── type2-vmware/
│   │   ├── 01-vmware-vm-configuration.png
│   │   ├── 02-vmware-vm-running.png
│   │   ├── 03-vmware-system-configuration.png
│   │   └── 04-vmware-sysbench-result.png
│   │
│   └── comparison/
│       └── 01-hypervisor-performance-comparison.png
│
├── results/
│   └── performance-analysis.md
│
└── README.md
```

---

# 📸 Screenshot Checklist

## Type-1 --- Proxmox VE

---

```
                No. Screenshot       File Name                               Status
```

---

```
                 01 Proxmox          `01-proxmox-dashboard.png`              To be verified
                    Dashboard                                                

                 02 VM Configuration `02-proxmox-vm-configuration.png`       To be verified

                 03 VM Running       `03-proxmox-vm-running.png`             To be verified

                 04 Ubuntu Console   `04-proxmox-ubuntu-console.png`         To be verified

                 05 System           `05-proxmox-system-configuration.png`   To be verified
                    Configuration                                            

                 06 Sysbench Result  `06-proxmox-sysbench-result.png`        **TO BE ADDED**

                 07 Resource         `07-proxmox-resource-monitoring.png`    **TO BE ADDED**
                    Monitoring                                               
```

---

## Type-2 --- VMware Workstation

---

```
                No. Screenshot       File Name                              Status
```

---

```
                 01 VM Configuration `01-vmware-vm-configuration.png`       To be verified

                 02 VM Running       `02-vmware-vm-running.png`             To be verified

                 03 System           `03-vmware-system-configuration.png`   To be verified
                    Configuration                                           

                 04 Sysbench Result  `04-vmware-sysbench-result.png`        **AVAILABLE**
```

---

## Comparison

---

```
                No. Screenshot       File Name                                    Status
```

---

```
                 01 Final            `01-hypervisor-performance-comparison.png`   **TO BE ADDED**
                    Performance                                                   
                    Comparison                                                    
```

---

---

# 🛠️ Technologies and Tools

Category              Technology / Tool

---

Type-1 Hypervisor     Proxmox VE\
Type-2 Hypervisor     VMware Workstation\
Guest OS              Ubuntu\
Benchmark             Sysbench\
Version Control       Git\
Repository Platform   GitHub

---

# 🔬 Experiment Workflow

```text
                    Hypervisor Analysis
                           │
             ┌─────────────┴─────────────┐
             │                           │
       Type-1 Hypervisor           Type-2 Hypervisor
        Proxmox VE                VMware Workstation
             │                           │
             ▼                           ▼
        Ubuntu VM                   Ubuntu VM
             │                           │
             ├── 2 vCPU                ├── 2 vCPU
             ├── 2 GB RAM              ├── 2 GB RAM
             └── 20 GB Disk            └── 20 GB Disk
             │                           │
             ▼                           ▼
          Sysbench                    Sysbench
             │                           │
             ▼                           ▼
       Performance                  Performance
         Results                      Results
             │                           │
             └─────────────┬─────────────┘
                           ▼
                   Final Comparison
```

---

# 🧾 Final Conclusion

This experiment demonstrates the process of evaluating virtual machine\
CPU performance using two different hypervisor architectures.

A Type-1 environment was configured using **Proxmox VE**, while a Type-2\
environment was configured using **VMware Workstation**. Ubuntu was used\
as the guest operating system with an intended allocation of **2 vCPU, 2**\
**GB RAM, and 20 GB disk**.

The VMware Workstation VM successfully completed the Sysbench CPU\
benchmark with:

- **Total Execution Time:** 10.0006 s
- **Total Events:** 24,366
- **Events per Second:** 2,436.05
- **Average Latency:** 0.41 ms

The Proxmox benchmark and resource-monitoring results are currently\
unavailable. They are therefore marked **TO BE ADDED**, and no\
unsupported comparison or conclusion has been made.

After obtaining the Proxmox benchmark results, the final comparison can\
be completed using execution time, total events, events per second, and\
average latency.

---

## 📚 Experiment Status

Component                        Status

---

Proxmox VE VM                    Completed\
VMware Workstation VM            Completed\
Ubuntu Guest OS                  Completed\
VMware Sysbench                  ✅ Completed\
Proxmox Sysbench                 ⏳ To be added\
VMware Results                   ✅ Available\
Proxmox Results                  ⏳ To be added\
Resource Monitoring Comparison   ⏳ To be added\
Final Performance Comparison     ⏳ To be added

---

### Author

**Cloud Computing Laboratory --- Experiment 01**

**Performance Analysis of Type-1 and Type-2 Hypervisors**
