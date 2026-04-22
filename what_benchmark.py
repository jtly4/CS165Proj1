import argparse, time, csv, random

from enum import Enum
from pathlib import Path
from typing import Callable

import requirements
DATA_DIRECTORY = Path('demo_data')

# create dictionary

#incomplete
SORTING_ALGORITHMS: dict[str, Callable[[list[int]], None]] = {
    'python_sort'
}



# generate permutations
class PermutationType(Enum):
    UNIFORMLY_DISTRIBUTED = 'uniform'
    REVERSE = 'reverse'
    ALMOST_SORTED = 'almost'

def generate_random_list(size: int, permutation: PermutationType) -> list[int]:
    nums = list(range(size)) 

    match permutation:
        case PermutationType.UNIFORMLY_DISTRIBUTED:
            random.shuffle(nums) # fisher yates shuffle

        case PermutationType.REVERSE:
            nums.reverse()
        case PermutationType.ALMOST_SORTED:
            pass

    return nums

def run_basic_test(size: int):
    nums = generate_random_list(size, PermutationType.UNIFORMLY_DISTRIBUTED)
    start_time_ns = 0
    SORTING_ALGORITHMS['python_sort'](nums)
    end_time_ns = time.process_time_ns()

    print(f"Size: {size}, Time(ns): {end_time_ns - start_time_ns}")


#  save data
def get_data_path(alogirthm_name: str, permuatation: PermutationType) -> Path:
    directory = DATA_DIRECTORY / algorithm_name
    directory.mkdir(parents=True, exist_ok=True)
    return (directory/permutation.name).with_suffix('.csv')

def save_data():
    pass)


# benchmark over all algos - one size, one perm, x iter
def run_benchmark(size: int, permutation: PermutationType, iterations: int):
    for _ in range(iterations):
        nums = generate_random_list(size, permutation)

        for algorithm_name, algorithm in SORTING_ALGORITHMS.items():
            copy_nums = nums.copy()
            start_time_ns = time.process_time_ns()
            algorithm(copy_nums)
            end_time_ns = time.process_time_ns()

            elapsed_time = end_time_ns - start_time_ns

            print(f"Algorithm: {algorithm_name}, Size: {size}, Permutation: {permutation.name}, Time: {elapsed_time}")



# benchmark over all input sizes
# factor by 2 bc it looks nicer on a log log plot
def run_benchmarks(min_size: int, max_size: int, factor: int, iterations: int):
    size = min_size
    while size <= max_size:
        for permutation in PermutationType:
            run_benchmark(size, permutation, iterations)

        size *= factor


def get_args():
    pass
    

if __name__ == "__main__":
    # run_basic_test(1000)
    # run_benchmark(min_size=2, max_size=1000, factor=2, permutation=PermutationType.UNIFORMLY_DISTRIBUTED, iterations=5)
    run_benchmarks(2, 1000, 2, 5)

