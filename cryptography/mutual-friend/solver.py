

from pwn import *
from Crypto.Util.number import *
import sys
sys.setrecursionlimit(2000)

p = remote('3.0.58.217', 2002)

def gcd(a, b):
	if(b == 0):
		return a
	return gcd(b, a%b)

moduli = []

for i in range(200):
	p.sendline()
	p.recvuntil('N = ')
	moduli.append(int(p.recvuntil('\n')))

P = 1
Q = 1
N = 1
done = False
j = 1

while(True):
	print j
	j+=1
	p.sendline()
	p.recvuntil('N = ')
	N = int(p.recvuntil('\n'))
	for i in moduli:
		if(gcd(N, i) != 1):
			P = gcd(N, i)
			Q = N / P
			done = True
			break
	if(done):
		break

p.recvuntil('c = ')
c = int(p.recvuntil('\n'))
x = (P-1)*(Q-1)
e = 65537

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

d = modinv(e, x)
print 'd:', d
print


m = pow(c, d, N)
print m
print 
print long_to_bytes(m)

p.interactive()
p.close()

