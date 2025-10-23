#!/usr/bin/env python3
"""Micro-benchmark for augmentation throughput."""
import json
import time
from pathlib import Path
import pandas as pd
import subprocess
import sys

def run_benchmark(method_subset, num_methods=1):
    """Run benchmark for a subset of methods."""
    start = time.time()
    result = subprocess.run([
        "python", "tools/generate_augsets.py",
        "--input", "tests/fixtures/mini_annotations.csv",
        "--output-root", "/tmp/bench_output",
        "--combo-mode", "singletons",
        "--variants-per-sample", "1",
        "--seed", "42",
        "--num-proc", "1",
    ], capture_output=True, text=True)
    duration = time.time() - start

    if result.returncode != 0:
        print(f"Benchmark failed: {result.stderr}", file=sys.stderr)
        return None

    # Count output rows
    datasets = list(Path("/tmp/bench_output").rglob("dataset.parquet"))
    total_rows = sum(len(pd.read_parquet(d)) for d in datasets)

    return {
        "subset": method_subset,
        "rows": total_rows,
        "duration_sec": round(duration, 2),
        "rows_per_sec": round(total_rows / duration, 2) if duration > 0 else 0,
    }

def main():
    print("=== Augmentation Micro-Benchmark ===")
    results = []

    # Benchmark 1: CPU-only methods
    print("Running CPU benchmark...")
    cpu_result = run_benchmark("cpu_methods")
    if cpu_result:
        results.append(cpu_result)

    # Save results
    output_path = Path("benchmark_results.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print("\n--- Results ---")
    for r in results:
        print(f"{r['subset']}: {r['rows']} rows in {r['duration_sec']}s ({r['rows_per_sec']} rows/sec)")

    print(f"\nResults saved to {output_path}")

if __name__ == "__main__":
    main()
