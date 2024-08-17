def can_friends_sit_together(nums, indexDiff, valueDiff):
    # Set to store seat numbers in the current sliding window
    window = set()
    
    for i in range(len(nums)):
        # Check if there's a seat in the window that satisfies the movie preference (valueDiff)
        for num in window:
            if abs(nums[i] - num) <= valueDiff:
                return True
        
        # Add the current seat to the window
        window.add(nums[i])
        
        # Maintain the sliding window size to ensure only indices within indexDiff are considered
        if i >= indexDiff:
            window.remove(nums[i - indexDiff])
    
    return False

# Example usage:
nums = [2, 3, 5, 4, 9]
indexDiff = 2
valueDiff = 1
print(can_friends_sit_together(nums, indexDiff, valueDiff))  # Output: True
