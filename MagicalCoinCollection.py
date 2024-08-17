class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def find_largest_magical_grove(root):
    def post_order_traversal(node):
        if not node:
            # Return a tuple: (is_bst, sum, min_value, max_value)
            return True, 0, float('inf'), float('-inf')
        
        left_is_bst, left_sum, left_min, left_max = post_order_traversal(node.left)
        right_is_bst, right_sum, right_min, right_max = post_order_traversal(node.right)
        
        # Check if the current node is a valid BST
        if left_is_bst and right_is_bst and left_max < node.val < right_min:
            # The current subtree is a BST
            current_sum = node.val + left_sum + right_sum
            # Update the global maximum sum if needed
            nonlocal max_grove_sum
            max_grove_sum = max(max_grove_sum, current_sum)
            # Return the updated values
            return True, current_sum, min(node.val, left_min), max(node.val, right_max)
        else:
            # If not a BST, return False and sum as 0
            return False, 0, float('-inf'), float('inf')
    
    # Initialize the maximum sum
    max_grove_sum = 0
    # Start post-order traversal from the root
    post_order_traversal(root)
    return max_grove_sum

# Example Usage:
# Constructing the binary tree from the example
root = TreeNode(1)
root.left = TreeNode(4)
root.right = TreeNode(3)
root.left.left = TreeNode(2)
root.left.right = TreeNode(4)
root.right.left = TreeNode(2)
root.right.right = TreeNode(5)
root.right.right.left = TreeNode(4)
root.right.right.right = TreeNode(6)

# Finding the largest magical grove
output = find_largest_magical_grove(root)
print(output)  # Output should be 20
