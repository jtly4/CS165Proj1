"""
plot_benchmarks.py

Reads avg.csv from each algorithm folder and produces one log-log plot
per algorithm, with all three permutation types overlaid.

Output: benchmark_data/<algorithm>/plots/loglog.png

Each plot includes:
  - Scatter points per permutation (distinct colours)
  - Line of best fit per permutation
  - Slope annotation per permutation
  - X-axis labelled as powers of 2 (2^1 … 2^17)

Your professor's note:
  If T(n) = a * n^c, then log(T) = log(a) + c*log(n)
  Slope in log-log space = exponent c in the growth rate O(n^c).

Run from inside proj1/
"""

import csv
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

PERM_COLOURS = {
    "almost":      "#4C9BE8",   # blue
    "alternating": "#E8614C",   # red-orange
    "uniform":     "#4CE87A",   # green
}

# Powers of 2 for x-axis ticks: 2^1=2 … 2^17=131072
POWER2_TICKS       = [2 ** i for i in range(1, 18)]
POWER2_TICK_LABELS = [f"$2^{{{i}}}$" for i in range(1, 18)]

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_avg_csv(path: Path) -> dict[str, list]:
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
    Fits log(T) = slope * log(n) + intercept via least squares.
    Returns (slope, intercept).
    """
    log_n = np.log(sizes)
    log_t = np.log(times)
    slope, intercept = np.polyfit(log_n, log_t, 1)
    return slope, intercept

# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def plot_algorithm(algorithm: str, data: dict[str, list], out_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#0F1117")
    ax.set_facecolor("#1A1D27")

    slopes: dict[str, float] = {}

    for permutation in PERMUTATIONS:
        colour = PERM_COLOURS[permutation]

        pairs = sorted(
            (s, t)
            for s, t, p in zip(
                data["input_size"],
                data["avg_time_ns"],
                data["permutation"],
            )
            if p == permutation and t > 0
        )

        if len(pairs) < 2:
            print(f"  {permutation:12s}  →  not enough data, skipping")
            continue

        sizes, times = zip(*pairs)
        slope, intercept = log_log_fit(list(sizes), list(times))
        slopes[permutation] = slope

        # Fitted line over a smooth range
        n_fit = np.linspace(min(sizes) * 0.8, max(sizes) * 1.2, 300)
        t_fit = np.exp(intercept) * n_fit ** slope

        # Scatter points
        ax.scatter(
            sizes, times,
            color=colour, s=70, zorder=5,
            edgecolors="white", linewidths=0.4,
            label=f"{permutation}  (slope = {slope:.3f})",
        )

        # Best-fit line (dashed, same colour)
        ax.plot(
            n_fit, t_fit,
            color=colour, linewidth=1.8, linestyle="--", alpha=0.85,
        )

    # --- Axes ---
    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.set_xticks(POWER2_TICKS)
    ax.set_xticklabels(POWER2_TICK_LABELS, fontsize=8)
    ax.xaxis.set_minor_locator(ticker.NullLocator())   # suppress minor ticks

    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.ticklabel_format(style="plain", axis="y")
    ax.tick_params(colors="#CCCCDD", which="both")

    for spine in ax.spines.values():
        spine.set_edgecolor("#444455")

    ax.set_xlabel("Input size  (n)", color="#CCCCDD", fontsize=11)
    ax.set_ylabel("Avg time  (ns)", color="#CCCCDD", fontsize=11)
    ax.set_title(
        f"{algorithm}  —  log-log plot",
        color="white", fontsize=13, fontweight="bold", pad=12,
    )

    # --- Slope annotation box ---
    slope_lines = "\n".join(
        f"{p:12s}  slope ≈ {s:.3f}"
        for p, s in slopes.items()
    )
    ax.annotate(
        slope_lines,
        xy=(0.97, 0.05),
        xycoords="axes fraction",
        ha="right", va="bottom",
        fontsize=9,
        color="white",
        fontfamily="monospace",
        bbox=dict(
            boxstyle="round,pad=0.5",
            facecolor="#2A2D3A",
            edgecolor="#666677",
            linewidth=1.0,
        ),
    )

    # --- Legend ---
    ax.legend(
        facecolor="#2A2D3A", edgecolor="#444455",
        labelcolor="white", fontsize=9,
        loc="upper left",
    )

    ax.grid(True, which="both", color="#2E3040", linewidth=0.6, linestyle="--")

    plt.tight_layout()
    out_path = out_dir / "loglog.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)

    print(f"  Saved: {out_path}")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("Log-Log Benchmark Plotter")
    print("=" * 60)

    for algorithm in ALGORITHMS:
        algo_dir = BASE_DIR / algorithm
        avg_path = algo_dir / "avg.csv"

        if not avg_path.is_file():
            print(f"\n[{algorithm}]  avg.csv not found — skipping")
            continue

        data    = load_avg_csv(avg_path)
        out_dir = algo_dir / "plots"
        out_dir.mkdir(exist_ok=True)

        print(f"\n[{algorithm}]")
        plot_algorithm(algorithm, data, out_dir)

    print("\n" + "=" * 60)
    print("Done.")
    print("=" * 60)


if __name__ == "__main__":
    main()