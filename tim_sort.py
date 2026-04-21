def tim_sort(nums: list[int]):
    num_comparisons = 0
    stack = []
    runs = run_decomp(nums)

    for run in runs:
        stack.append(runs.pop(0))

        while True:
            h = len(stack)
            r1, r2, r3, r4 = 0, 0, 0, 0
            s1, s2, s3, s4 =  [], [], [], []
            # setting up
            if h >= 1:
                s1 = stack[-1]
                r1 = len(s1)

            if h >= 2:
                s2 = stack[-2]
                r2 = len(s2)

            if h >= 3:
                s3 = stack[-3]
                r3 = len(s3)

            if h >= 4:
                s4 = stack[-4]
                r4 = len(s4)

            # merging
            if h > 3 and r1 > r3:
                merged_list, comparisons = merger(s3, s2)
                stack[-3:-1] = [merged_list]
            elif h > 2 and (r1 >= r2):
                merged_list, comparisons = merger(s3, s2)
                stack[-3:-1] = [merged_list]
            elif h > 3 and ((r1+r2) >= r3):
                merged_list, comparisons = merger(s2, s1)
                stack[-2:] = [merged_list]
            elif h > 4 and ((r2 + r3) >= r4):
                merged_list, comparisons = merger(s2, s1)
                stack[-2:] = [merged_list]
            else:
                break
            
            num_comparisons += comparisons

    while len(stack) > 1:
        merged_list, comparisons = merger(stack[-2], stack[-1])
        stack[-2:] = [merged_list]
        num_comparisons += comparisons

    if stack:
        nums[:] = stack[0]
    else:
        nums[:] = []

    #print(nums)

    return num_comparisons

def merger(list1: list[int], list2: list[int]):
    merged_list = []
    i, j, num_comparisons = 0, 0, 0

    while i < len(list1) and j < len(list2):
        num_comparisons += 1
        if list1[i] < list2[j]:
            merged_list.append(list1[i])
            i += 1
        else:
            merged_list.append(list2[j])
            j += 1

    if i < len(list1):
        merged_list.extend(list1[i:])
    if j < len(list2):
        merged_list.extend(list2[j:])

    return merged_list, num_comparisons

def run_decomp(nums: list[int]):
    runs = []
    n, i = len(nums), 0

    while i < n:
        begin = i

        if i == n - 1:
            runs.append([nums[i]])
            break

        ascend = False
        if nums[i] <= nums[i + 1]:
            ascend = True
        
        i += 1 

        if ascend:
            while i < n and nums[i - 1] <= nums[i]:
                i += 1
            runs.append(nums[begin:i])

        else:
            while i < n and nums[i - 1] > nums[i]:
                i += 1
            runs.append(nums[begin:i][::-1])
    return runs

'''def run_decomp(nums: list[int]) -> list[list[int]]:
    runs = []
    n = len(nums)
    i = 0

    while i < n:
        start = i

        if i == n - 1:
            runs.append([nums[i]])
            break

        ascending = nums[i] <= nums[i + 1]
        i += 1

        if ascending:
            while i < n and nums[i - 1] <= nums[i]:
                i += 1
            runs.append(nums[start:i])
        else:
            while i < n and nums[i - 1] > nums[i]:
                i += 1
            runs.append(nums[start:i][::-1])

    return runs
    '''
arr3 = [5, 2, 4, 1, 3, 11, 9, 8, 7, 6, 0, 10]
print(run_decomp(arr3))
print(tim_sort(arr3))