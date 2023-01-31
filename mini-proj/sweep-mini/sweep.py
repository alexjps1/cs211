"""
sweep.py
by Alex JPS
2023-01-18
CS 211
"""

def all_same(l: list) -> bool:
    for i in l:
        if i != l[0]:
            return False
    return True

def dedup(l: list) -> list:
    result = []
    for i in range(len(l)):
        if i > 0:
            if l[i] != l[i-1]:
                result.append(l[i])
        else:
            result.append(l[i])
    return result

def max_run(l: list) -> int:
    result = 0
    for i in range(len(l)):
        if i == 0:
            run, result  = 1, 1
        elif l[i] == l[i-1]:
            run += 1
            if run > result:
                result = run
        else:
            run = 1
    return result
