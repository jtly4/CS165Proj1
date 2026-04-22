import argparse
import csv
import math
import random
import time
from enum import Enum
from pathlib import Path
from typing import Callable

import requirements

DATA_DIRECTORY = Path("benchmark_data")

SORTING_ALGORITHMS: dict[str, Callable[[list[int]], int]] = {
    "insertion_sort": requirements.insertion_sort,
    "tim_sort": requirements.tim_sort,
    "shell_sort1": requirements.shell_sort1,
    "shell_sort2": requirements.shell_sort2,
    "shell_sort3": requirements.shell_sort3,
    "shell_sort4": requirements.shell_sort4,
    "shell_sort5": requirements.shell_sort5,
    "skip_list_sort": requirements.skip_list_sort,
}


class PermutationType(Enum):
    UNIFORMLY_DISTRIBUTED = "uniform"
    ALMOST_SORTED = "almost"
    TWO_ALTERNATING_RUNS = "alternating"


def generate_input(size: int, permutation: PermutationType) -> list[int]:
    nums = list(range(1, size + 1))

    match permutation:
        case PermutationType.UNIFORMLY_DISTRIBUTED:
            random.shuffle(nums)

        case PermutationType.ALMOST_SORTED:
            if size > 1:
                num_swaps = max(1, int(math.log2(size)))
                for _ in range(num_swaps):
                    i = random.randint(0, size - 1)
                    j = random.randint(0, size - 1)
                    nums[i], nums[j] = nums[j], nums[i]

        case PermutationType.TWO_ALTERNATING_RUNS:
            odds = list(range(1, size + 1, 2))
            evens = list(range(2, size + 1, 2))
            nums = odds + evens

    return nums


def is_sorted(nums: list[int]) -> bool:
    for i in range(1, len(nums)):
        if nums[i - 1] > nums[i]:
            return False
    return True


def get_data_path(algorithm_name: str, permutation: PermutationType) -> Path:
    directory = DATA_DIRECTORY / algorithm_name
    directory.mkdir(parents=True, exist_ok=True)
    return (directory / permutation.value).with_suffix(".csv")


def append_data(algorithm_name: str, permutation: PermutationType, size: int, elapsed_time_ns: int) -> None:
    path = get_data_path(algorithm_name, permutation)
    write_header = not path.exists()

    with path.open("a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["size", "time_ns"])
        writer.writerow([size, elapsed_time_ns])


def clear_existing_data() -> None:
    if DATA_DIRECTORY.exists():
        for path in DATA_DIRECTORY.rglob("*.csv"):
            path.unlink()


def run_benchmark(size: int, permutation: PermutationType, iterations: int) -> None:
    for _ in range(iterations):
        base_input = generate_input(size, permutation)

        for algorithm_name, algorithm in SORTING_ALGORITHMS.items():
            nums = base_input.copy()

            start_time_ns = time.perf_counter_ns()
            algorithm(nums)
            end_time_ns = time.perf_counter_ns()

            if not is_sorted(nums):
                raise ValueError(f"{algorithm_name} failed to sort correctly")

            elapsed_time_ns = end_time_ns - start_time_ns
            append_data(algorithm_name, permutation, size, elapsed_time_ns)

            print(
                f"Algorithm: {algorithm_name}, "
                f"Size: {size}, "
                f"Permutation: {permutation.value}, "
                f"Time(ns): {elapsed_time_ns}"
            )


def run_benchmarks(sizes: list[int], iterations: int) -> None:
    for size in sizes:
        for permutation in PermutationType:
            run_benchmark(size, permutation, iterations)


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark sorting algorithms.")
    parser.add_argument("--iterations", type=int, default=5)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--clear", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = get_args()
    random.seed(args.seed)

    if args.clear:
        clear_existing_data()

    sizes = [10, 500, 2500, 5000, 32678, 131072]
    run_benchmarks(sizes, args.iterations)


if __name__ == "__main__":
    main()