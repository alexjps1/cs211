"""
Function Dispatcher
by Alex JPS
2023-02-24
CS 211
"""

from typing import List, Callable, Dict

def total_sum(lst: List[int]):
    result = 0
    for i in lst:
        result += i
    return result

def apply(func: Callable, lst: List[int]):
    result = []
    for i in lst:
        result.append(func(i))
    return result

def square(lst: List[int]):
    return apply(lambda x: x**2, lst)

def magnitude(lst: List[int]):
    squared = square(lst)
    result = total_sum(squared)**(1/2)
    return result

dispatch_table = {1: total_sum,
                  2: square,
                  3: magnitude
                  }

class FunctionDispatcher:

    def __init__(self, funcs: Dict[int, Callable]):
        self.funcs = funcs

    def process_command(self, key: int, lst: List[int]):
        return self.funcs[key](lst)
