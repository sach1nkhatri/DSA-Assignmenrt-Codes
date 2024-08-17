def longest_hike(nums, k):
    n = len(nums)
    start = 0
    max_length = 0
    
    for end in range(1, n):
        if nums[end] > nums[end - 1]:
            gain = nums[end] - nums[end - 1]
            if gain > k:
                start = end
        else:
            start = end
        
        max_length = max(max_length, end - start + 1)
    
    return max_length

# Example Usage:
trail = [4, 2, 1, 4, 3, 4, 5, 8, 15]
k = 3
result = longest_hike(trail, k)
print(result)  # Output should be 5
