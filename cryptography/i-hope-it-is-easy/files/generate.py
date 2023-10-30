from Crypto.Util.number import getPrime
    
FLAG = open('flag.txt', 'rb').read()
encrypted = []
a = 10**400
b = 10**500
for c in FLAG:
    n = getPrime(700)
    if (not(a<=n*n<b)):
        print('WRONG')
        print(n*n-a)
        print(b-n*n)
        exit()
    encrypted.append(c ^ (n*n))

txtFile = open('encrypted.txt', 'w')
txtFile.write(', '.join(list(map(str, encrypted))))
