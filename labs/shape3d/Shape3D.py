"""
Shape 3D
by Alex JPS
2023-01-25
CS 211
"""

import math

class Shape3D:

    def __init__(self):
        raise NotImplementedError("Abstract class cannot be instantiated")

    def volume(self) -> float:
        raise NotImplementedError("Not implemented for abstract class")

    def area(self) -> float:
        raise NotImplementedError("Not implemented for abstract class")

    def print_info(self) -> str:
        return f"Area: {self.area()} Volume: {self.volume()}"

class Cylinder(Shape3D):

    def __init__(self, radius: float, height: float):
        self.radius = float(radius)
        self.height = float(height)
    
    def volume(self) -> float:
        return math.pi * (self.radius**2) * self.height

    def area(self) -> float:
        return (2 * math.pi * (self.radius**2)) + (2 * math.pi * self.radius * self.height)

class Cuboid(Shape3D):

    def __init__(self, width: float, length: float, height: float):
        self.width = float(width)
        self.length = float(length)
        self.height = float(height)

    def volume(self):
        return self.width * self.length * self.height

    def area(self):
        return 2*(self.width*self.length) + 2*(self.width*self.height) + 2*(self.length*self.height)

class Cube(Cuboid):

    def __init__(self, width: float):
        width = float(width)
        self.width = width
        self.length = width
        self.height = width