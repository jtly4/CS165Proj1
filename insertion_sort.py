def insertion_sort(nums: list[int]):
    num_comparisons = 0
    for i in range(1, len(nums)):
        j = i
        
        # if nums[j] < nums[j-1]:
        #     print(f"{nums[j]} is less than {nums[j-1]}")
        #     while j > 0 and nums[j] < nums[j-1]:
        #         num_comparisons += 1
        #         temp = nums[j]
        #         nums[j] = nums[j-1]
        #         j -= 1
        #         nums[j] = temp
        #         print(f"array after swapping: {nums}")
                
        #     print("-"*15)
        num_comparisons += 1
        while j > 0 and nums[j] < nums[j-1]:
            num_comparisons += 1
            temp = nums[j]
            nums[j] = nums[j-1]
            j -= 1
            nums[j] = temp
            print(f"array after swapping: {nums}")
        
        print("-"*15)
            
    return num_comparisons

arr1 = [2, 15, 8, 1, 17, 10, 12, 5]
arr2 = [3, 9, 6, 1, 2]
arr3 = [5, 2, 4, 1, 3, 11, 9, 8, 7, 6, 0, 10]

#print(insertion_sort(arr1))
#print(insertion_sort(arr2))
print(insertion_sort(arr3))

