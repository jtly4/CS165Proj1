"""
plot_benchmarks.py

Reads avg.csv from each algorithm folder and produces log-log plots,
one per permutation type per algorithm.

Output: benchmark_data/<algorithm>/plots/<permutation>_loglog.png

Each plot includes:
  - Scatter points of (input_size, avg_time_ns)
  - Line of best fit (linear regression in log-log space)
  - Slope annotation (= exponent in O(n^slope) growth rate)

Your professor's note explained:
  If T(n) = a * n^c, then log(T) = log(a) + c*log(n)
  So in log-log space this is a straight line with slope c —
  that slope IS the exponent in the growth rate.

Run from inside proj1/
"""

import csv
import math
import os
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR    = Path("benchmark_data")
ALGORITHMS  = [
    "insertion_sort",
    "shell_sort1",
    "shell_sort2",
    "shell_sort3",
    "shell_sort4",
    "shell_sort5",
    "tim_sort",
]
PERMUTATIONS = ["almost", "alternating", "uniform"]

# Colour per permutation for quick visual distinction
PERM_COLOURS = {
    "almost":      "#4C9BE8",
    "alternating": "#E8854C",
    "uniform":     "#4CE87A",
}

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_avg_csv(path: Path) -> dict[str, list]:
    """
    Returns {"permutation": [...], "input_size": [...], "avg_time_ns": [...]}
    """
    data: dict[str, list] = {"permutation": [], "input_size": [], "avg_time_ns": []}
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data["permutation"].append(row["permutation"].strip())
            data["input_size"].append(int(row["input_size"].strip()))
            data["avg_time_ns"].append(float(row["avg_time_ns"].strip()))
    return data

# ---------------------------------------------------------------------------
# Regression
# ---------------------------------------------------------------------------

def log_log_fit(sizes: list[int], times: list[float]) -> tuple[float, float]:
    """
    Fits  log(T) = slope * log(n) + intercept  via least squares.
    Returns (slope, intercept) — slope is the growth-rate exponent.
    """
    log_n = np.log(sizes)
    log_t = np.log(times)
    slope, intercept = np.polyfit(log_n, log_t, 1)
    return slope, intercept

# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def plot_permutation(
    algorithm: str,
    permutation: str,
    sizes: list[int],
    times: list[float],
    out_dir: Path,
) -> float:
    """
    Draws and saves a single log-log plot.
    Returns the fitted slope.
    """
    slope, intercept = log_log_fit(sizes, times)

    # Fitted line over a smooth range
    n_fit  = np.linspace(min(sizes) * 0.8, max(sizes) * 1.2, 300)
    t_fit  = np.exp(intercept) * n_fit ** slope

    colour = PERM_COLOURS.get(permutation, "#AAAAAA")

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor("#0F1117")
    ax.set_facecolor("#1A1D27")

    # Scatter
    ax.scatter(
        sizes, times,
        color=colour, s=70, zorder=5,
        edgecolors="white", linewidths=0.5,
        label="Observed avg",
    )

    # Best-fit line
    ax.plot(
        n_fit, t_fit,
        color="white", linewidth=1.6, linestyle="--",
        label=f"Best fit  (slope = {slope:.4f})",
    )

    ax.set_xscale("log")
    ax.set_yscale("log")

    # Axis styling
    for spine in ax.spines.values():
        spine.set_edgecolor("#444455")
    ax.tick_params(colors="#CCCCDD", which="both")
    ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.ticklabel_format(style="plain", axis="both")

    ax.set_xlabel("Input size  (n)", color="#CCCCDD", fontsize=11)
    ax.set_ylabel("Avg time  (ns)", color="#CCCCDD", fontsize=11)
    ax.set_title(
        f"{algorithm}  ·  {permutation}  —  log-log plot",
        color="white", fontsize=13, fontweight="bold", pad=12,
    )

    # Slope annotation box
    ax.annotate(
        f"slope ≈ {slope:.4f}\n⟹  O(n^{slope:.2f})",
        xy=(0.97, 0.05),
        xycoords="axes fraction",
        ha="right", va="bottom",
        fontsize=10, color="white",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#2A2D3A", edgecolor=colour, linewidth=1.2),
    )

    legend = ax.legend(
        facecolor="#2A2D3A", edgecolor="#444455",
        labelcolor="white", fontsize=9,
    )

    ax.grid(True, which="both", color="#2E3040", linewidth=0.6, linestyle="--")

    plt.tight_layout()
    out_path = out_dir / f"{permutation}_loglog.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)

    return slope

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("Log-Log Benchmark Plotter")
    print("=" * 60)

    for algorithm in ALGORITHMS:
        algo_dir  = BASE_DIR / algorithm
        avg_path  = algo_dir / "avg.csv"

        if not avg_path.is_file():
            print(f"\n[{algorithm}]  avg.csv not found — skipping")
            continue

        data     = load_avg_csv(avg_path)
        out_dir  = algo_dir / "plots"
        out_dir.mkdir(exist_ok=True)

        print(f"\n[{algorithm}]")

        for permutation in PERMUTATIONS:
            # Filter rows for this permutation
            pairs = [
                (s, t)
                for s, t, p in zip(
                    data["input_size"],
                    data["avg_time_ns"],
                    data["permutation"],
                )
                if p == permutation and t > 0
            ]

            if len(pairs) < 2:
                print(f"  {permutation:12s}  →  not enough data points, skipping")
                continue

            sizes, times = zip(*sorted(pairs))
            slope = plot_permutation(algorithm, permutation, list(sizes), list(times), out_dir)

            print(f"  {permutation:12s}  slope = {slope:.4f}  →  O(n^{slope:.2f})")

        print(f"  Plots saved to: {out_dir}")

    print("\n" + "=" * 60)
    print("Done.")
    print("=" * 60)


if __name__ == "__main__":
    main()