def shell_sort1(nums:list[int]):
    num_comparisons, k = 0, 1
    last_gap, gap = float('inf'), float('inf')
    n = len(nums)
    gaps = []

    while gap > 1:
        gap = n // (2 ** k)

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
    return num_comparisons

def swap(nums:list[int], j: int, val: int):
    nums[j] = val
    
'''
arr1 = [2, 15, 8, 1, 17, 10, 12, 5]
arr2 = [3, 9, 6, 1, 2]
arr3 = [5, 2, 4, 1, 3, 11, 9, 8, 7, 6, 0, 10]

#print(insertion_sort(arr1))
#print(insertion_sort(arr2))
print(shell_sort1(arr3))
'''