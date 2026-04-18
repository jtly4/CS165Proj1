def tim_sort(nums: list[int]):
    pass

def merge_comp(l: list[int], r: list[int]):
    pass

def run_decomp(nums: list[int]):
    runs = []
    n = len(nums)

    for i in range(n):
        begin = i

        back = nums[i] <= nums[i + 1]
        i += 1 
