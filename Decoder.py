def shift_character(c, direction):
    # Function to shift a character 'c' either clockwise or counter-clockwise
    if direction == 1:  # Clockwise shift
        return chr((ord(c) - ord('a') + 1) % 26 + ord('a'))
    else:  # Counter-clockwise shift
        return chr((ord(c) - ord('a') - 1) % 26 + ord('a'))

def decode_message(s, shifts):
    # Transform the string into a list for in-place modifications
    s = list(s)
    
    # Apply each shift instruction to the specified range of characters
    for shift in shifts:
        start_disc, end_disc, direction = shift
        for i in range(start_disc, end_disc + 1):
            s[i] = shift_character(s[i], direction)
    
    # Convert the list back into a string and return the result
    return ''.join(s)

# Example Usage
s = "hello"
shifts = [[0, 1, 1], [2, 3, 0], [0, 2, 1]]
result = decode_message(s, shifts)
print(result)  # Output: "jglko"
