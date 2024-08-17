import random

def calculate_distance(path, distance_matrix):
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += distance_matrix[path[i]][path[i+1]]
    return total_distance

def generate_initial_solution(num_cities):
    path = list(range(num_cities))
    random.shuffle(path)
    path.append(path[0])  # Return to the starting city
    return path

def get_neighbors(path):
    neighbors = []
    for i in range(1, len(path) - 2):
        for j in range(i + 1, len(path) - 1):
            neighbor = path[:]
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]  # Swap cities
            neighbors.append(neighbor)
    return neighbors

def hill_climbing(distance_matrix):
    num_cities = len(distance_matrix)
    current_solution = generate_initial_solution(num_cities)
    current_cost = calculate_distance(current_solution, distance_matrix)
    
    while True:
        neighbors = get_neighbors(current_solution)
        next_solution = None
        next_cost = current_cost
        
        for neighbor in neighbors:
            neighbor_cost = calculate_distance(neighbor, distance_matrix)
            if neighbor_cost < next_cost:
                next_solution = neighbor
                next_cost = neighbor_cost
        
        if next_cost < current_cost:
            current_solution = next_solution
            current_cost = next_cost
        else:
            break  # Local optimum reached
    
    return current_solution, current_cost

# Example Usage:
distance_matrix = [
    [0, 2, 9, 10],
    [1, 0, 6, 4],
    [15, 7, 0, 8],
    [6, 3, 12, 0]
]

best_path, best_cost = hill_climbing(distance_matrix)
print(f"Best path: {best_path}")
print(f"Cost of the best path: {best_cost}")
