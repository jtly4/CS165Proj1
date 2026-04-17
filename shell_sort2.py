def shell_sort2(nums:list[int]):
    num_comparisons, k = 0, 1
    last_gap, gap = float('inf'), float('inf')
    n = len(nums)
    gaps = []

    while gap > 1:
        gap = 2 * (n // (2 ** (k + 1))) + 1

        if gap != last_gap:
            gaps.append(gap)
            last_gap = gap

        k += 1

    if not gaps or gaps[-1] != 1:
        gaps.append(1)

    
    for g in gaps:
        for i in range(g, n):
            temp = nums[i]
            j = i
            while j >= g:
                num_comparisons += 1
                shell = nums[j - g]

                if shell > temp:
                    swap(nums, j, shell)
                    j -= g

                else:
                    break

            swap(nums, j, temp)    
            print(nums)
            print("-"*30)
    return num_comparisons

def swap(nums:list[int], j: int, val: int):
    nums[j] = val

arr3 = [5, 2, 4, 1, 3, 11, 9, 8, 7, 6, 0, 10]
print(shell_sort2(arr3))
    