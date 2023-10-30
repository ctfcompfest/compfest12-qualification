from Crypto.Util.number import isPrime
import math
import timeit
start_time = timeit.default_timer()
encrypted = list(map(int, open('encrypted.txt').read().split(', ')))
FLAG = list()

def squareroot(n):
    l = 1
    r = n
    m = (l+r)//2
    while(l<=r):
        m = (l+r)//2
        x = m*m
        if (x==n):
            return m
        if (x < n):
            l = m + 1
        else:
            r = m - 1
    return l

for c in encrypted:
    for i in range(1, 256):
        p2 = c ^ i
        p = squareroot(p2)
        if (isPrime(p)):
            if (p*p == p2):
                FLAG.append(i)
                break


print('FLAG:', end=' ')
print(''.join(map(str, list(map(chr, FLAG)))))
end_time = timeit.default_timer()
print("Finished in {:.2f} s".format(end_time - start_time))
