#!/usr/bin/env python3

for n in range(1, 10):
    print('=' * 35)
    print('n:', n)
    print('-' * 35)
    lst = list()
    
    for i in range(2 * n - 1):
        tmp = list()
        for j in range(2 * n - 1):
            tmp.append(max(max(n - j, j - (n - 2)), max(n - i , i - (n - 2))))
        lst.append(tmp)
        
    for row in lst:
        print(' '.join(map(str, row)))
    print('=' * 35)

def getFlag():
    return 'COMPFEST12{my_fri3nd_s4ys_s0rry_888144}'
