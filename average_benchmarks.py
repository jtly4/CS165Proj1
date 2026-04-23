"""
average_benchmarks.py
 
Reads validated benchmark CSVs from:
    benchmark_data/<algorithm>/validated_<permutation>.csv
 
Computes the average time_ns per input size and writes:
    benchmark_data/<algorithm>/avg.csv
 
Headers: permutation, input_size, avg_time_ns
 
Run from inside proj1/
"""
 
import csv
import os
from pathlib import Path
 
# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
 
BASE_DIR = Path("benchmark_data")
 
ALGORITHMS = [
    "insertion_sort",
    "shell_sort1",
    "shell_sort2",
    "shell_sort3",
    "shell_sort4",
    "shell_sort5",
    "tim_sort",
]
 
PERMUTATIONS = ["almost", "alternating", "uniform"]
 
VALID_SIZES = [10, 500, 2500, 5000, 32678, 131072]
 
# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
 
def compute_averages(src_path: Path) -> dict[int, float]:
    """Return {size: avg_time_ns} from a validated CSV."""
    buckets: dict[int, list[int]] = {}
 
    with src_path.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            size = int(row["size"].strip())
            time_ns = int(row["time_ns"].strip())
            buckets.setdefault(size, []).append(time_ns)
 
    return {
        size: sum(times) / len(times)
        for size, times in buckets.items()
    }
 
 
# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
 
def main() -> None:
    print("=" * 60)
    print("Computing Average Benchmark Times")
    print("=" * 60)
 
    for algorithm in ALGORITHMS:
        algo_dir = BASE_DIR / algorithm
        avg_rows: list[dict] = []
 
        print(f"\n[{algorithm}]")
 
        for permutation in PERMUTATIONS:
            src_path = algo_dir / f"validated_{permutation}.csv"
 
            if not src_path.is_file():
                print(f"  {permutation:12s}  →  SKIPPED (source not found: {src_path})")
                continue
 
            averages = compute_averages(src_path)
 
            for size in VALID_SIZES:
                if size not in averages:
                    print(f"  {permutation:12s}  size={size:>7}  →  MISSING")
                    continue
 
                avg = averages[size]
                avg_rows.append({
                    "permutation":  permutation,
                    "input_size":   size,
                    "avg_time_ns":  round(avg, 2),
                })
                print(f"  {permutation:12s}  size={size:>7}  avg={avg:>15.2f} ns")
 
        if not avg_rows:
            print(f"  No data found — avg.csv not written.")
            continue
 
        # Sort by permutation then size for a clean file
        avg_rows.sort(key=lambda r: (r["permutation"], r["input_size"]))
 
        dst_path = algo_dir / "avg.csv"
        with dst_path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["permutation", "input_size", "avg_time_ns"])
            writer.writeheader()
            writer.writerows(avg_rows)
 
        print(f"  → Written: {dst_path}")
 
    print("\n" + "=" * 60)
    print("Done.")
    print("=" * 60)
 
 
if __name__ == "__main__":
    main()
 