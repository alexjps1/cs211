"""
Binary Search Trees Lab
by Alex JPS
2023-02-01
CS 211
"""

class Node:

    def __init__(self, node_data: int):
        self.node_data = node_data

    def sum_node_data(self):
        raise NotImplementedError("Do not implement in abstract class")
    
class Leaf(Node):

    def __init__(self, node_data: int):
        self.node_data = node_data

    def sum_node_data(self):
        return self.node_data
    
    def __str__(self):
        return str(self.node_data)
    
class Internal(Node):

    def __init__(self, node_data: int, left: Node, right: Node):
        self.node_data = node_data
        self.left = left
        self.right = right

    def sum_node_data(self):
        return self.node_data + self.left.sum_node_data() + self.right.sum_node_data()

    def __str__(self):
        return f"<{str(self.node_data)}, {str(self.left)}, {str(self.right)}>"
    
def main(): 
    l1 = Leaf(3)
    l2 = Leaf(6)
    l3 = Leaf(9)
    i = Internal(7, l2, l3)
    root = Internal(5, l1, i)
    print(root.sum_node_data())
    print(root)

if __name__ == '__main__':
    main()
