import heapq

def find_classroom_with_most_classes(n, classes):
    # Step 1: Sort the classes by their start time, and by duration in descending order if start times are the same
    classes.sort(key=lambda x: (x[0], -(x[1] - x[0])))

    # Step 2: Initialize a priority queue (min-heap) to manage room availability and an array to track the number of classes per room
    room_heap = []
    class_count = [0] * n

    for cls in classes:
        start, end = cls

        # Step 3: Free up rooms that are available by the current class's start time
        while room_heap and room_heap[0][0] <= start:
            heapq.heappop(room_heap)

        # Step 4: Assign the current class to an available room
        if len(room_heap) < n:
            # If a room is available, assign the class to it
            room_index = len(room_heap)
            heapq.heappush(room_heap, (end, room_index))
            class_count[room_index] += 1
        else:
            # Delay the class and allocate it to the earliest available room
            earliest_end_time, room_index = heapq.heappop(room_heap)
            heapq.heappush(room_heap, (earliest_end_time + (end - start), room_index))
            class_count[room_index] += 1

    # Step 5: Identify the room that hosted the most classes
    max_classes = max(class_count)
    for i in range(n):
        if class_count[i] == max_classes:
            return i

# Example 1
n1 = 2
classes1 = [[0, 10], [1, 5], [2, 7], [3, 4]]
print(find_classroom_with_most_classes(n1, classes1))  # Output: 0

# Example 2
n2 = 3
classes2 = [[1, 20], [2, 10], [3, 5], [4, 9], [6, 8]]
print(find_classroom_with_most_classes(n2, classes2))  # Output: 1
