def check1(n, num, pos):
    for i in range(len(n[0])):
        if n[pos[0]][i] == num and pos[1] != i:
            return False

    for i in range(len(n)):
        if n[i][pos[1]] == num and pos[0] != i:
            return False
    
    x = pos[1] // 3
    y = pos[0] // 3

    for i in range(y*3, y*3 + 3):
        for j in range(x*3, x*3 + 3):
            if n[i][j] == num and (i,j) != pos:
                return False

    return True

def check2(n, num, pos):
    for i in range(len(n[0])):
        if n[pos[0]][i] == num and pos[1] != i:
            return False

    for i in range(len(n)):
        if n[i][pos[1]] == num and pos[0] != i:
            return False
    
    x = pos[1] // 3
    y = pos[0] // 3

    for i in range(y*3, y*3 + 3):
        for j in range(x*3, x*3 + 3):
            if n[i][j] == num and (i,j) != pos:
                return False

    if pos[0] == pos[1]:
        for i in range(len(n)):
            if n[i][i] == num:
                return False

    if pos[1] + pos[0] == len(n)-1:
        for i in range(len(n)):
            if n[i][len(n)-i-1] == num:
                return False

    return True

def check3(n, num, pos):
    for i in range(len(n[0])):
        if n[pos[0]][i] == num and pos[1] != i:
            return False

    for i in range(len(n)):
        if n[i][pos[1]] == num and pos[0] != i:
            return False
    
    x = pos[1] // 3
    y = pos[0] // 3

    for i in range(y*3, y*3 + 3):
        for j in range(x*3, x*3 + 3):
            if n[i][j] == num and (i,j) != pos:
                return False

    if pos[0] == pos[1]:
        for i in range(len(n)):
            if n[i][i] == num:
                return False

    if pos[1] + pos[0] == len(n)-1:
        for i in range(len(n)):
            if n[i][len(n)-i-1] == num:
                return False

    A = [2, 1, -1, -2, -2, -1, 1, 2]
    B = [1, 2, 2, 1, -1, -2, -2, -1]

    for i in range(8):
        a = pos[0] + A[i]
        b = pos[1] + B[i]

        if(a >= 0 and b >= 0 and a < 9 and b < 9 and n[a][b] == num):
            return False

    return True

def PrintSudoku(n):
    for i in range(len(n)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        for j in range(len(n[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end ="")
            if j == 8:
                print(n[i][j])
            else:
                print(str(n[i][j]) + " ", end="")