import pandas as pd
import matplotlib.pyplot as plt

# Performance data from the completed workload testing
data = {
    "Workload": ["W1", "W2", "W3", "W4", "W5"],
    "Concurrency": [1, 2, 4, 8, 16],
    "Response_Time_ms": [12.40, 11.95, 8.37, 9.71, 15.31],
    "Throughput_req_s": [32.45, 48.16, 54.05, 48.12, 47.97],
    "CPU_Percent": [1.91, 0.67, 0.20, 0.25, 0.26],
    "Memory_MB": [35.27, 35.29, 35.35, 35.41, 35.51],
    "Success": [200, 200, 200, 200, 200],
    "Failed": [0, 0, 0, 0, 0],
}

df = pd.DataFrame(data)

# Save observation table
df.to_csv("performance_observation_table.csv", index=False)

# Response time graph
plt.figure()
plt.plot(df["Concurrency"], df["Response_Time_ms"], marker="o")
plt.xlabel("Concurrent Requests")
plt.ylabel("Average Response Time (ms)")
plt.title("Concurrent Requests vs Average Response Time")
plt.grid(True)
plt.savefig("response_time.png", dpi=200, bbox_inches="tight")
plt.close()

# Throughput graph
plt.figure()
plt.plot(df["Concurrency"], df["Throughput_req_s"], marker="o")
plt.xlabel("Concurrent Requests")
plt.ylabel("Throughput (requests/second)")
plt.title("Concurrent Requests vs Throughput")
plt.grid(True)
plt.savefig("throughput.png", dpi=200, bbox_inches="tight")
plt.close()

# CPU graph
plt.figure()
plt.plot(df["Concurrency"], df["CPU_Percent"], marker="o")
plt.xlabel("Concurrent Requests")
plt.ylabel("Average CPU Utilization (%)")
plt.title("Concurrent Requests vs CPU Utilization")
plt.grid(True)
plt.savefig("cpu_utilization.png", dpi=200, bbox_inches="tight")
plt.close()

# Memory graph
plt.figure()
plt.plot(df["Concurrency"], df["Memory_MB"], marker="o")
plt.xlabel("Concurrent Requests")
plt.ylabel("Average Memory Usage (MB)")
plt.title("Concurrent Requests vs Memory Utilization")
plt.grid(True)
plt.savefig("memory_utilization.png", dpi=200, bbox_inches="tight")
plt.close()

print("All performance graphs and observation table generated successfully.")