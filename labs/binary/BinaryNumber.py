"""
Binary Number Simulator
by Alex JPS
2023-02-16
CS 211
"""
from typing import List

class BinaryNumber:

    def __init__(self, val: List[int]):
        self.val = val

    def __or__(self, other: 'BinaryNumber') -> 'BinaryNumber':
        """Return new BinaryNumber object for OR operation"""
        assert len(self.val) == len(other.val)
        result = BinaryNumber([])
        for i in range(len(self.val)):
            result.val.append(1 if self.val[i] or other.val[i] else 0)
        return result

    def __and__(self, other: 'BinaryNumber') -> 'BinaryNumber':
        """Return new BinaryNumber object for AND operation"""
        assert len(self.val) == len(other.val)
        result = BinaryNumber([])
        for i in range(len(self.val)):
            result.val.append(1 if self.val[i] and other.val[i] else 0)
        return result

    def __str__(self):
        return str(self.val)

    def left_shift(self, amount: int):
        """Directly modify object, left shifting bits by amount"""
        result = []
        for i in range(len(self.val) - amount):
            result.append(self.val[i + amount])
        result += [0]*amount
        self.val = result

    def right_shift(self, amount: int):
        """Directly modify object, right shifting bits by amount"""
        result = []
        result += [0]*amount
        for i in range(len(self.val) - amount):
            result.append(self.val[i])
        assert len(self.val) == len(result)
        self.val = result

    def extract(self, start: int, end:int) -> 'BinaryNumber':
        result = BinaryNumber(self.val)
        result.right_shift(start)
        diff = end - start
        zeros = len(self.val) - diff - 1
        ones = diff + 1
        mask = BinaryNumber([0]*zeros + [1]*ones)
        return result & mask