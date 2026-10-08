"""Reads results/results.csv and draws execution-time, speedup and efficiency graphs."""
import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results/results.csv")
os.makedirs("graphs", exist_ok=True)

def label(n):
    return f"N = {n/1e6:g}M"

# 1. Execution time vs threads
plt.figure(figsize=(7, 4.5))
for n, g in df.groupby("N"):
    plt.plot(g["threads"], g["par_time_s"] * 1000, marker="o", label=label(n))
plt.xlabel("Number of threads"); plt.ylabel("Parallel execution time (ms)")
plt.title("Execution time vs threads"); plt.yscale("log")
plt.xticks(sorted(df["threads"].unique())); plt.grid(alpha=0.3); plt.legend()
plt.tight_layout(); plt.savefig("graphs/execution_time.png", dpi=150); plt.close()

# 2. Speedup vs threads (with ideal line)
plt.figure(figsize=(7, 4.5))
t = sorted(df["threads"].unique())
plt.plot(t, t, "k--", label="Ideal (linear)")
for n, g in df.groupby("N"):
    plt.plot(g["threads"], g["speedup"], marker="o", label=label(n))
plt.xlabel("Number of threads"); plt.ylabel("Speedup (T_seq / T_par)")
plt.title("Speedup vs threads"); plt.xticks(t); plt.grid(alpha=0.3); plt.legend()
plt.tight_layout(); plt.savefig("graphs/speedup.png", dpi=150); plt.close()

# 3. Efficiency vs threads
plt.figure(figsize=(7, 4.5))
for n, g in df.groupby("N"):
    plt.plot(g["threads"], g["efficiency"] * 100, marker="o", label=label(n))
plt.axhline(100, color="k", ls="--", label="Ideal (100%)")
plt.xlabel("Number of threads"); plt.ylabel("Efficiency (%)")
plt.title("Efficiency vs threads"); plt.xticks(t); plt.grid(alpha=0.3); plt.legend()
plt.tight_layout(); plt.savefig("graphs/efficiency.png", dpi=150); plt.close()

# 4. Sequential vs parallel time vs vector size (at max threads)
plt.figure(figsize=(7, 4.5))
seq = df.groupby("N")["seq_time_s"].min() * 1000
for th in t:
    g = df[df["threads"] == th]
    plt.plot(g["N"] / 1e6, g["par_time_s"] * 1000, marker="o", label=f"{th} thread(s)")
plt.plot(seq.index / 1e6, seq.values, "k--", marker="s", label="Sequential")
plt.xlabel("Vector size (millions of elements)"); plt.ylabel("Time (ms)")
plt.title("Execution time vs vector size"); plt.grid(alpha=0.3); plt.legend()
plt.tight_layout(); plt.savefig("graphs/time_vs_size.png", dpi=150); plt.close()

print("Graphs saved in graphs/")
