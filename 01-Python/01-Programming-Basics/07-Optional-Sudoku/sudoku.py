# pylint: disable=missing-docstring

def all_numbers(list_9):
    """Are all the numbers in list_9 ?"""
    for i in range(1,10):
        if (i in list_9) is False:
            return False
    return True

def sudoku_validator(grid):
    """Is grid OK ?"""
    #import ipdb; ipdb.set_trace()
    for line in grid:
        if all_numbers(line) is False:
            return False
    for i in range(9):
        col =[]
        for k in range(9):
            col.append(grid[k][i])
        if all_numbers(col) is False:
            return False
    for i in range(0, 9, 3):
        for j in range(0,9,3):
            square = []
            for i_2 in range(3):
                for j_2 in range(3):
                    square.append(grid[i+i_2][j+j_2])
            if all_numbers(square) is False:
                return False
    return True
