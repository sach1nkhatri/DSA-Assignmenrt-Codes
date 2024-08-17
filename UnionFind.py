class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [1] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.parent[rootX] = rootY
            else:
                self.parent[rootY] = rootX
                self.rank[rootX] += 1

def can_friend_requests_be_approved(n, restrictions, requests):
    uf = UnionFind(n)
    result = []
    
    for req in requests:
        x, y = req
        rootX = uf.find(x)
        rootY = uf.find(y)
        
        # Check if this union violates any restriction
        violates_restriction = False
        for r in restrictions:
            r1, r2 = r
            if (uf.find(r1) == rootX and uf.find(r2) == rootY) or (uf.find(r1) == rootY and uf.find(r2) == rootX):
                violates_restriction = True
                break
        
        if not violates_restriction:
            uf.union(x, y)
            result.append("approved")
        else:
            result.append("denied")
    
    return result

# Example usage:
n = 5
restrictions = [[0, 1], [1, 2], [2, 3]]
requests = [[0, 4], [1, 2], [3, 1], [3, 4]]
print(can_friend_requests_be_approved(n, restrictions, requests))  # Output: ['approved', 'denied', 'approved', 'denied']
