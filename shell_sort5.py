def shell_sort5(nums:list[int]):
    num_comparisons = 0
    n = len(nums)
    k, gap = 1, float('inf')

    gaps = []

    while k < n:
        gap = ((3 ** k) - 1) // 2
        if gap < n:
            gaps.append(int(gap))
        k += 1
    gaps = sorted(gaps, reverse=True)
    for g in gaps:
        for i in range(g, n):
            j = i
            temp = nums[i]
            while j >= g:
                num_comparisons += 1
                shell = nums[j - g]
                if shell > temp:
                    swap(nums, j, shell)
                    j -= g
                else:
                    break
            
            swap(nums, j, temp) 

    return num_comparisons

def swap(nums:list[int], j: int, val: int):
    nums[j] = val

arr3 = [5, 2, 4, 1, 3, 11, 9, 8, 7, 6, 0, 10]
print(shell_sort5(arr3))