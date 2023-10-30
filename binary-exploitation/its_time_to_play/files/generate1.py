import random
import check
import copy
board_1 =[[4,5,6,2,7,1,8,3,9],
          [7,9,2,3,4,8,6,5,1],
          [1,3,8,9,5,6,2,4,7],
          [6,7,3,1,9,5,4,8,2],
          [2,1,9,4,8,3,7,6,5],
          [8,4,5,6,2,7,1,9,3],
          [5,2,4,8,1,9,3,7,6],
          [9,6,1,7,3,4,5,2,8],
          [3,8,7,5,6,2,9,1,4]]

board_2 = [[7,8,4,9,6,2,1,3,5],
           [5,6,3,4,1,8,7,9,2],
           [1,2,9,5,7,3,4,6,8],
           [3,4,8,6,2,7,5,1,9],
           [2,9,5,1,8,4,3,7,6],
           [6,1,7,3,9,5,8,2,4],
           [9,5,6,8,3,1,2,4,7],
           [4,7,1,2,5,6,9,8,3],
           [8,3,2,7,4,9,6,5,1]]

board_3 = [[1,2,7,9,5,3,8,4,6],
           [6,3,5,8,1,4,2,7,9],
           [9,4,8,6,7,2,3,1,5],
           [8,6,1,5,2,7,4,9,3],
           [2,7,4,3,9,8,6,5,1],
           [5,9,3,4,6,1,7,2,8],
           [7,8,9,1,4,6,5,3,2],
           [4,1,6,2,3,5,9,8,7],
           [3,5,2,7,8,9,1,6,4]]

huruf = ["A", "B", "C", "D", "E", "F", "G", "H"]
boards = [board_1, board_2, board_3]
my_string = ""
my_index = random.randint(0,2)
my_list = copy.deepcopy(boards[my_index])

for i in range(31):
    row = random.randint(0,8)
    col = random.randint(0,8)
    if i > 22:
        while str(my_list[row][col]).isalpha():
            row = random.randint(0,8)
            col = random.randint(0,8)
        my_list[row][col] = huruf[i-31]
        my_string += str((boards[my_index])[row][col])
    else:
        if my_list[row][col] != 0:
            my_list[row][col] = 0
        else:
            while my_list[row][col] == 0:
                row = random.randint(0,8)
                col = random.randint(0,8)
            my_list[row][col] = 0
print("Level 1 : Normal sudoku")
print()
check.PrintSudoku(my_list)
print(my_string)
