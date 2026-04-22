"""
validate_benchmarks.py

Reads raw benchmark CSVs from:
    proj1/benchmark_data/<algorithm>/<permutation>.csv

For each (algorithm, permutation) pair it keeps exactly 10 rows per
valid input size and writes the trimmed data to:
    proj1/benchmark_data/<algorithm>/validated_<permutation>.csv

Valid sizes : 10, 500, 2500, 5000, 32678, 131072
Target count: 10 rows per size
"""

import os
import pandas as pd

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = os.path.join("CS165Proj1", "benchmark_data")

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

VALID_SIZES   = [10, 500, 2500, 5000, 32678, 131072]
TARGET_COUNT  = 10   # rows to keep per size

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def validate_file(src_path: str, dst_path: str) -> dict:
    """
    Read src_path, keep TARGET_COUNT rows per valid size, write to dst_path.
    Returns a summary dict for reporting.
    """
    df = pd.read_csv(src_path)

    # Normalise column names (strip whitespace, lowercase)
    df.columns = [c.strip().lower() for c in df.columns]

    if "size" not in df.columns or "time_ns" not in df.columns:
        raise ValueError(
            f"Expected columns 'size' and 'time_ns', got: {list(df.columns)}"
        )

    df["size"]    = pd.to_numeric(df["size"],    errors="coerce")
    df["time_ns"] = pd.to_numeric(df["time_ns"], errors="coerce")
    df.dropna(subset=["size", "time_ns"], inplace=True)
    df["size"] = df["size"].astype(int)

    summary = {}
    kept_frames = []

    for size in VALID_SIZES:
        rows = df[df["size"] == size]
        total = len(rows)

        if total == 0:
            summary[size] = {"found": 0, "kept": 0, "status": "MISSING"}
            continue

        if total < TARGET_COUNT:
            kept = rows.copy()
            status = f"WARN – only {total} rows (need {TARGET_COUNT})"
        else:
            kept = rows.head(TARGET_COUNT).copy()
            status = "OK" if total == TARGET_COUNT else f"TRIMMED ({total} → {TARGET_COUNT})"

        summary[size] = {"found": total, "kept": len(kept), "status": status}
        kept_frames.append(kept)

    if kept_frames:
        result = pd.concat(kept_frames, ignore_index=True)
        result = result[["size", "time_ns"]]          # canonical column order
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        result.to_csv(dst_path, index=False)
    else:
        summary["_error"] = "No valid rows found – output file NOT written."

    return summary


def print_summary(algorithm: str, permutation: str, summary: dict) -> None:
    print(f"\n  [{algorithm}] {permutation}")
    if "_error" in summary:
        print(f"    ERROR: {summary['_error']}")
        return
    for size in VALID_SIZES:
        info = summary.get(size, {"found": 0, "kept": 0, "status": "MISSING"})
        print(
            f"    size={size:>7}  found={info['found']:>4}  "
            f"kept={info['kept']:>2}  {info['status']}"
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("Benchmark CSV Validation")
    print("=" * 60)

    total_ok      = 0
    total_missing = 0
    total_warn    = 0

    for algorithm in ALGORITHMS:
        for permutation in PERMUTATIONS:
            src_path = os.path.join(BASE_DIR, algorithm, f"{permutation}.csv")
            dst_path = os.path.join(
                BASE_DIR, algorithm, f"validated_{permutation}.csv"
            )

            if not os.path.isfile(src_path):
                print(f"\n  [{algorithm}] {permutation}  →  SOURCE NOT FOUND: {src_path}")
                total_missing += 1
                continue

            try:
                summary = validate_file(src_path, dst_path)
                print_summary(algorithm, permutation, summary)

                # Tally overall health
                has_warn = any(
                    "WARN" in str(v.get("status", "")) or "MISSING" in str(v.get("status", ""))
                    for k, v in summary.items()
                    if k != "_error" and isinstance(v, dict)
                )
                if "_error" in summary or has_warn:
                    total_warn += 1
                else:
                    total_ok += 1

                if "_error" not in summary:
                    print(f"    → Written: {dst_path}")

            except Exception as exc:
                print(f"\n  [{algorithm}] {permutation}  →  ERROR: {exc}")
                total_warn += 1

    print("\n" + "=" * 60)
    print(
        f"Done.  OK: {total_ok}  |  Warnings/Errors: {total_warn}  "
        f"|  Missing sources: {total_missing}"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()