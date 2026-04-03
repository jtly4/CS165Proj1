def insertion_sort(nums: list[int]):
    num_comparisons = 0
    for i in range(1, len(nums)):
        j = i
        k = j-1
        if nums[j] < nums[k]:
            # print(f"{nums[j]} is less than {nums[k]}")
            temp = nums[j]
            while nums[j] < nums[k] and k >=0:
                num_comparisons += 1
                # print(f"swapping values: nums[j] ({nums[j]}) and nums[k] ({nums[k]})")
                nums[j] = nums[k]
                j -= 1
                k -= 1
                nums[j] = temp
                print(f"array after swapping: {nums}")
                

            
            print(f"array after inserting: {nums}")
            print("-"*15)

        
    return num_comparisons

arr1 = [2, 15, 8, 1, 17, 10, 12, 5]
arr2 = [3, 9, 6, 1, 2]

print(insertion_sort(arr1))
print(insertion_sort(arr2))

