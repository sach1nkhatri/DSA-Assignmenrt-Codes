import heapq

def dijkstra(graph, source, n, weights):
    distances = [float('inf')] * n
    distances[source] = 0
    
    pq = [(0, source)]
    
    while pq:
        curr_dist, node = heapq.heappop(pq)
        
        if curr_dist > distances[node]:
            continue
        
        for neighbor, weight in graph[node]:
            if weight == -1:
                continue
            
            new_dist = curr_dist + weights[weight]
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))
    
    return distances

def find_valid_modifications(n, roads, source, destination, target_time):
    graph = [[] for _ in range(n)]
    weights = []
    under_construction = []
    
    for i, (u, v, w) in enumerate(roads):
        graph[u].append((v, i))
        graph[v].append((u, i))
        weights.append(w)
        if w == -1:
            under_construction.append(i)
    
    distances = dijkstra(graph, source, n, weights)
    initial_dist = distances[destination]
    
    if initial_dist == float('inf'):
        return []
    
    if initial_dist > target_time:
        return []
    
    low, high = 1, 2 * 10**9
    
    for edge_idx in under_construction:
        left, right = low, high
        
        while left <= right:
            mid = (left + right) // 2
            weights[edge_idx] = mid
            
            distances = dijkstra(graph, source, n, weights)
            dist = distances[destination]
            
            if dist == target_time:
                break
            elif dist < target_time:
                left = mid + 1
            else:
                right = mid - 1
        
        weights[edge_idx] = mid
    
    distances = dijkstra(graph, source, n, weights)
    if distances[destination] == target_time:
        return [[roads[i][0], roads[i][1], weights[i]] for i in range(len(roads))]
    else:
        return []

# Example Usage
n = 5
roads = [[4, 1, -1], [2, 0, -1], [0, 3, -1], [4, 3, -1]]
source = 0
destination = 1
target_time = 5

solution = find_valid_modifications(n, roads, source, destination, target_time)
print(solution)
