import random
import check
import copy
board_1 = [[3,0,0,0,1,0,0,0,9],
           [0,0,0,0,0,0,0,0,0],
           [0,0,4,0,0,0,7,0,0],
           [0,0,0,8,3,4,0,0,0],
           [4,0,0,1,5,9,0,0,6],
           [0,0,0,6,7,2,0,0,0],
           [0,0,3,0,0,0,6,0,0],
           [0,0,0,0,0,0,0,0,0],
           [1,0,0,0,9,0,0,0,7]]

board_2 = [[1,0,0,0,4,0,0,0,3],
           [0,0,0,0,0,0,0,0,0],
           [0,0,7,0,0,0,1,0,0],
           [0,0,0,8,3,4,0,0,0],
           [0,0,0,1,5,9,0,0,0],
           [0,0,0,6,7,2,0,0,0],
           [0,0,9,0,0,0,3,0,0],
           [0,0,0,0,0,0,0,0,0],
           [7,0,0,0,6,0,0,0,9]]

board_3 = [[8,0,0,0,0,0,0,0,9],
           [0,0,0,0,0,0,0,0,0],
           [0,0,9,0,0,0,3,0,0],
           [0,0,0,6,7,2,9,0,1],
           [0,0,0,1,5,9,0,0,0],
           [0,0,0,8,3,4,0,2,0],
           [0,0,7,0,0,0,1,0,0],
           [0,0,0,0,0,0,0,0,0],
           [1,0,0,0,0,0,0,0,2]]

def Solve(n):
    find = EmptySpace(n)
    if not find:
        return True
    else:
        row, col = find
    for i in range(1,10):
        if check.check3(n, i, (row, col)):
            n[row][col] = i
            if Solve(n):
                return True
            n[row][col] = 0
    
    return False

def EmptySpace(n):
    for i in range(len(n)):
        for j in range(len(n[0])):
            if n[i][j] == 0:
                return (i, j)
    return None

huruf = ["A", "B", "C", "D", "E", "F", "G", "H"]
boards = [board_1, board_2, board_3]
my_string = ""
my_index = random.randint(0,2)
my_list = copy.deepcopy(boards[my_index])
Solve(boards[my_index])

for i in range(8):
    row = random.randint(0,8)
    col = random.randint(0,8)
    while my_list[row][col] != 0:
        row = random.randint(0,8)
        col = random.randint(0,8)
    my_list[row][col] = huruf[i]
    my_string += str((boards[my_index])[row][col])

print("Level 3 : Diagonal with anti-knight move sudoku")
print()
check.PrintSudoku(my_list)
print(my_string)

