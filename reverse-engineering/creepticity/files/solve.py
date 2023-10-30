file = open("out.txt", "r")

encrypted = file.read()
Lastkey = ord(encrypted[-1])
encstring = encrypted[:-2]

char = encstring[0]
key = chr(Lastkey ^ ord(char))
char1 = chr((ord(char)-30) ^ ord(key))
encstring = char1 + encstring[1:]
enclist = [char for char in encstring]

# There are two char possibilities each char so there is charselect to
# select between two possibilities. Decrypting straight up only gives a
# part of the flag. (0 -> charvalue not reduced by 97 after xor)
# charselect = [char for char in "00000000000000000000000000000000000"]
charselect = [char for char in "01000100100001000000001000101001010"]

for i in range(1, len(enclist)+1):
    char = enclist[-i]
    key = chr(ord(key) ^ ord(char))
    char1 = chr((ord(char)-30) ^ ord(key))
    char2 = chr((ord(char)+67) ^ ord(key))
    print(char1 + " " + char2 + " key = " + str(ord(key)) + " charselect = " + charselect[-i])
    if (charselect[-i] == "0"):
        enclist[-i] = char1
    else:
        enclist[-i] = char2

print("".join(enclist))
print(ord(key))