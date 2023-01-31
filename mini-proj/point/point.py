"""
Point Mini-Project
by Alex JPS
2023-01-13
CS 211
"""

class Point:
    
    def __init__(self, x, y):
        """Assigns given coordinates to self"""
        self.x = x
        self.y = y
    
    def move(self, dx, dy):
        "Moves point by given delta dx and dy"""
        self.x += dx
        self.y += dy
    
    def __eq__(self, other: "Point") -> bool:
        """Evaluates points as equal if they have the same coordinates"""
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __str__(self):
        """Represents point as a string showing a coordinate pair"""
        return f"({self.x}, {self.y})"
