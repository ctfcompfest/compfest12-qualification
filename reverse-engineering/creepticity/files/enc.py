inp = input("input : ")
key = int(input("key : "))

out = []

for char in inp:
    char1 = chr(((ord(char)^key)%97)+30)
    key = (ord(char1)^key) % 128
    out.append(char1)

char1 = chr(((ord(out[0])^key)%97)+30)
key = (ord(char1)^key) % 128
out[0] = char1

print(ord(char1))

print("".join(out))
print(key)