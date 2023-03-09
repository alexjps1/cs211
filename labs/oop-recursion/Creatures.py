"""
OOP Recursion Lab
by Alex JPS
2023-03-08
CS 211
"""

class Creature(object):

    def __init__(self):
        raise NotImplementedError("Abstract classes should not be instanciated")

    def __str__(self) -> str:
        raise NotImplementedError("Abstract class methods should not be called")
        
    def search(self, value: str) -> bool:
        raise NotImplementedError("Abstract class methods should not be called")

class Head(Creature):

    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return self.name

    def search(self, term: str) -> bool:
        return self.name == term

class Orthrus(Creature):

    def __init__(self, left: Creature, right: Creature):
        self.left = left
        self.right = right

    def __str__(self):
        return f"{self.left} {self.right}"

    def search(self, term: str):
        return self.left.search(term) or self.right.search(term)

class Cerberus(Creature):

    def __init__(self, left: Creature, middle: Creature, right: Creature):
        self.left = left
        self.middle = middle
        self.right = right

    def __str__(self) -> str:
        return f"{self.left} {self.middle} {self.right}"
    
    def search(self, term: str) -> bool:
        return self.left.search(term) or self.middle.search(term) or self.right.search(term)
    


