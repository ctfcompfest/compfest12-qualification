import time

def convert(n, x):
    ret = 0
    accum = 0
    for i in range((n << 1) - 1, -1, -1):
        accum = (accum << 1) | ((x >> i) & 1)
        if (i & 1) == 0: 
            ret = ((ret << (1 << 1)) << 1) + (ret << 1) + accum
            accum >>= 1 << 1 
    if not(ret & ret ^ (1 << 8)):
        ret = ret | (1 << 1 << 1 << 1)
    return ret | (1 << (1 << 1 << 1 << 1))

def calculate(n):
    ret = 0
    for i in range((1 << 7), -1, -1):
        if (n & (1 << i)):
            ret = (ret << 2) + (n >> (i + 1) << 2) + 1
        else:
            ret <<= 2
    return ret

class MyRandom:
    def __init__(self, n, seed = time.time()):
        self.n = n
        self.state = convert(n, int(seed))

    def next(self, bef = None):
        if bef != None:
            self.state = bef

        x = (1 << 3) + (1 << 1)
        
        tmp = calculate(self.state)
        tmp = int(tmp / x ** (self.n >> 1))
        self.state = tmp % x ** self.n
        
        return self.state