def optimize_boarding(head, k):
    n = len(head)
    for i in range(0, n, k):
        # Only reverse if there are k elements remaining
        if i + k <= n:
            head[i:i + k] = head[i:i + k][::-1]
    return head

# Example 1
head = [1, 2, 3, 4, 5]
k = 2
print(optimize_boarding(head, k))  # Output: [2, 1, 4, 3, 5]

# Example 2
head = [1, 2, 3, 4, 5]
k = 3
print(optimize_boarding(head, k))  # Output: [3, 2, 1, 4, 5]
