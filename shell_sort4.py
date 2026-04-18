def shell_sort4(nums:list[int]):
    n = len(nums)
    if n == 1:
        return nums
    num_comparisons, p, q = 0, 0, 0
    last_gap, gap = float('inf'), float('inf')
    
    gaps = []

    while True:
        if (2 ** p) >= n:
            break
        q = 0
        while True:
            gap = (2 ** p) * (3 ** q)
            if gap >= n:
                break
            if gap != last_gap:
                gaps.append(gap)
            q += 1
        p += 1

    

    if not gaps or gaps[0] != 1:
        gaps.append(1)

    gaps = sorted(gaps, reverse=True)
    
    
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
            # print(nums)
            # print("-"*30)
    
    return num_comparisons

def swap(nums:list[int], j: int, val: int):
    nums[j] = val

arr3 = [5, 2, 4, 1, 3, 11, 9, 8, 7, 6, 0, 10]
# print(shell_sort4(arr3))