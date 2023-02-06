"""
Where's Waldo
by Alex JPS
2023-02-03
CS 211
"""

Waldo = 'W'
Other = '.'

def all_row_exists_waldo(lst):
    if len(lst) == 0:
        return True
    if len(lst[0]) == 0:
        return False
    for row in range(len(lst)):
        for col in range(len(lst[0])):
            if lst[row][col] == Waldo:
                break
            elif col == len(lst[0]) - 1:
                return False
    return True

def all_col_exists_waldo(lst):
    if len(lst) == 0:
        return True
    for col in range(len(lst[0])):
        for row in range(len(lst)):
            if lst[row][col] == Waldo:
                break
            elif row == len(lst) - 1:
                return False
    return True

def all_row_all_waldo(lst):
    for row in range(len(lst)):
        for col in range(len(lst[0])):
            if lst[row][col] != Waldo:
                return False
    return True

# redundant, same as above
def all_col_all_waldo(lst):
    if len(lst) == 0:
        return True
    for col in range(len(lst[0])):
        for row in range(len(lst)):
            if lst[row][col] != Waldo:
                return False
    return True

def exists_row_exists_waldo(lst):
    for row in range(len(lst)):
        for col in range(len(lst[0])):
            if lst[row][col] == Waldo:
                return True
    return False

# redundant, same as above
def exists_col_exists_waldo(lst):
    if len(lst) == 0:
        return False
    for col in range(len(lst[0])):
        for row in range(len(lst)):
            if lst[row][col] == Waldo:
                return True
    return False

def exists_row_all_waldo(lst):
    if len(lst) == 0:
        return False
    if len(lst[0]) == 0:
        return True
    for row in range(len(lst)):
        for col in range(len(lst[0])):
            if lst[row][col] == Waldo:
                if col == len(lst[0]) - 1:
                    return True
                continue
            else:
                break
    return False

def exists_col_all_waldo(lst):
    if len(lst) == 0:
        return False
    for col in range(len(lst[0])):
        for row in range(len(lst)):
            if lst[row][col] == Waldo:
                if row == len(lst) - 1:
                    return True
                continue
            else:
                break
    return False