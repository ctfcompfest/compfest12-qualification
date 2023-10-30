import random
import check
import copy
board_1 = [[6,9,7,5,2,3,1,8,4],
         [5,1,2,4,8,6,9,3,7],
         [3,8,4,9,7,1,2,5,6],
         [4,3,6,7,1,8,5,2,9],
         [9,2,8,3,5,4,7,6,1],
         [7,5,1,6,9,2,8,4,3],
         [2,4,9,8,6,7,3,1,5],
         [8,7,3,1,4,5,6,9,2],
         [1,6,5,2,3,9,4,7,8]]

board_2 = [[5,7,9,1,4,8,2,6,3],
         [3,6,8,2,5,9,7,4,1],
         [2,4,1,3,7,6,8,5,9],
         [7,2,4,8,3,1,5,9,6],
         [6,9,3,7,2,5,1,8,4],
         [8,1,5,6,9,4,3,7,2],
         [1,8,7,4,6,3,9,2,5],
         [4,5,2,9,1,7,6,3,8],
         [9,3,6,5,8,2,4,1,7]]

board_3 = [[1,5,4,6,8,2,3,7,9],
         [3,2,7,5,9,4,8,6,1],
         [9,6,8,7,1,3,2,4,5],
         [6,3,1,9,2,8,4,5,7],
         [4,8,9,3,5,7,6,1,2],
         [5,7,2,1,4,6,9,8,3],
         [2,1,3,4,6,5,7,9,8],
         [8,4,5,2,7,9,1,3,6],
         [7,9,6,8,3,1,5,2,4]]

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

print("Level 2 : Diagonal sudoku")
print()
check.PrintSudoku(my_list)
print(my_string)
