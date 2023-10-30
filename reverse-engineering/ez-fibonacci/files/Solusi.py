from pwn import *
import base64

def Function1(n):
	if n < 1:
		return 0
	elif n == 1:
		return 1
	else:
		return Function1(n-1) + Function1(n-2)
	
def Function2(n):
	a = 2
	b = 5
	for i in range(n):
		temp = a
		a = b
		b = b*3 + temp
	return b
   
def Function3(n):
	return str(n)[::-1]

def Function4(n):
	return n[145:]


# p = remote("localhost", 2020)
p = process('./Fibonacci.py')

clue = '''a = Function1(25)
		  b = Function2(1,2,a)
		  c = Function3(b)
		  d = Function4(c)
		  print(d)'''

a = Function1(25)
b = Function2(a-2)
c = Function3(b)
d = Function4(c)
f = b''
my_fibo_string = b''
flag = ''

# p.interactive()
# p.close()

for i in range(4848):
	# print(i)
	if i != 4847:
		payload = d[i*8:(i+1)*8]
		p.sendlineafter("here:", payload)
		f += p.recvline()
	else:
		payload = d[i*8:]
		p.sendlineafter("here:", payload)
		f += p.recvline()
		
f = f.split(b"\n")

for i in range(len(f)-1):
	my_fibo_string += f[i]

for i in range(10):
	base64_bytes = my_fibo_string
	message_bytes = base64.b64decode(base64_bytes)
	my_fibo_string = message_bytes.decode('ascii')

my_fibo_string = my_fibo_string[my_fibo_string.index('{')+1:]

for i in range(20):
	if i < 2:
		a = 1
		b = 2
		flag += my_fibo_string[i]
	else:
		temp = a
		a = b
		b += temp
		flag += my_fibo_string[b-1]

print(flag)