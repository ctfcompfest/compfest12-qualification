#!/usr/bin/env python

def Function1(n):
    if n < 1:
        return 0
    elif n == 1:
        return 1
    else:
        return Function1(n-1) + Function1(n-2)

def Function2(a, b, n):
    if n <= 1:
        return b
    else:
        return Function2(b+a, a+a, n-1) + Function2(a, b+a, n-1)

def Function3(n):
    if len(str(n)) == 0:
        return n
    else:
        return Function3(str(n)[1:]) + str(n)[0]

def Function4(n):
    return n[145:]

a = (open("check.txt", "r").read()).split("\n")
b = (open("1<3Fibonacci.txt", "r").read()).split("\n")

print("This is your clue, warrior: CmEgPSBGdW5jdGlvbjEoMjUpCmIgPSBGdW5jdGlvbjIoMSwyLGEpCmMgPSBGdW5jdGlvbjMoYikKZCA9IEZ1bmN0aW9uNChjKQpwcmludChkKQo=")
print("Have you found the answer?")
print("Now i want you to name each of the 8 digits of the answer you found earlier")
print("For each correct answer, i'll give you a piece of clue that will guide you to find what you need")
print()

for i in range(4848):
    c = input("Enter the 8 digits here: ")
    if c == a[i]:
        print(b[i])
    else:
        print("Oops! You are prohibited from entering the fibonacci world!")
        break
