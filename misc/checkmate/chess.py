#!/usr/bin/env python

import random
import sys
import time

HORSE_MOVE = []
for i in range(-2, 3):
    for j in range(-2, 3):
        if abs(i) + abs(j) == 3:
            HORSE_MOVE.append((i, j))

def get_horses_numstep(col: int, row: int, horses: list, target: tuple) -> list:
    """Get number of step needed for a horses to reach target
    
    Arguments:
        col {int} -- chess board column size
        row {int} -- chess board row size
        kuda {list} -- list of (x, y) that define there is horse in column x, row y
        target {tuple} -- (x, y) that define target is in column x, row y
    
    Returns:
        list -- number of step needed for a horses to reach the target
    """
    tx, ty = target
    dist = [[-1 for _ in range(col)] for __ in range(row)]
    dist[ty - 1][tx - 1] = 0

    step = 0
    cnt_now = 1
    cnt_nxt = 0
    queue = [(tx - 1, ty - 1)]

    while len(queue) > 0:
        if cnt_now == 0:
            step += 1
            cnt_now, cnt_nxt = cnt_nxt, 0
        
        px, py = queue.pop(0)
        cnt_now -= 1
        for sx, sy in HORSE_MOVE:
            nx, ny = px + sx, py + sy
            if 0 <= nx < col and 0 <= ny < row:
                if dist[ny][nx] == -1:
                    dist[ny][nx] = step + 1
                    queue.append((nx, ny))
                    cnt_nxt += 1
    
    return [dist[hy - 1][hx - 1] for hx, hy in horses]


def board(col, row):
    rand_coor = []
    max_horses = max(col, row)
    for i in range(random.randint(1, max_horses) + 1):
        while True:
            temp = (random.randint(1, col), random.randint(1, row))
            if temp in rand_coor:
                continue
            rand_coor.append(temp)
            break

    horses = rand_coor[:-1]
    target = rand_coor[-1]

    print("-" * (2 * col + 1))
    for i in range(row):
        for j in range(col):
            if (j + 1, i + 1) == target:
                print("|X", end="")
            elif (j + 1, i + 1) in horses:
                print("|K", end="")
            else:
                print("| ", end="")
        print("|")
        print("-" * (2 * col + 1))
    
    horses_numstep = get_horses_numstep(col, row, horses, target)
    ans = min(horses_numstep)

    try:
        start = time.time()
        guess = int(input("Your guess: "))
        now = time.time()
        if now - start >= 60:
            print("Too weak, too slow")
            exit(0)
    except:
        return False

    if ans == guess:
        return True
    return False


def main():
    BOARD_SIZE_RANGE = [(5, 10), (20, 30), (50, 100), (100, 200), (200, 300), (500, 500), (500, 500)]
    for lo, hi in BOARD_SIZE_RANGE:
        col = random.randint(lo, hi)
        row = random.randint(lo, hi)
        if board(col, row) == False:
            print("You're not the chess grandmaster!")
            exit(0)
    flag  = open("flag.txt", "r") 
    print(flag.read())


if __name__ == "__main__":
    main()