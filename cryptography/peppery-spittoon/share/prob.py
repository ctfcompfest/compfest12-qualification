#!/usr/bin/env python3

import random
from fractions import Fraction

token = 'the token'

def generate(x):
	l = len(x)
	
	for i in range(l):
		for j in range(len(x[i])):
			x[i][j] = Fraction(x[i][j])
	
	try:
		for i in range(l):
			if (x[i][i] == 0):
				for j in range(l+1):
					temp = x[i][j]
					x[i][j] = x[i+1][j]
					x[i+1][j] = temp
			if (x[i][i] != 1):
				par = x[i][i]
				for j in range(l+1):
					x[i][j] = x[i][j]/par
			for j in range(i+1, l):
				par = x[j][i]
				for k in range(l+1):
					x[j][k] = x[j][k]-par*x[i][k]
			for i in range(l):
				for j in range(0, l-1-i):
					par = x[j][l-1-i]
					for k in range(l+1):
						x[j][k] = x[j][k]-par * x[l-1-i][k]
		for i in range(l):
			for j in range(l+1):
				if(x[i][j] == -0):
					x[i][j] = 0.0
		
		y = list()
		for i in range(l): 
			y.append(x[i].pop(l))
		return y
		
	except:
		print('Unknown error occured. Try again.')
		return -1337
    
def make_token():
	hint = 'P3ppeR'
	n = len(hint)
	x = list()
	for i in range(n):
		tmp = list()
		for j in range(n):
			tmp.append(random.randint(0, 99))
		tmp.append(ord(hint[i]))
		x.append(tmp)
	
	y = generate(x)
	if (y==-1337):
		return
	
	global token
	token = y
	
	print('Here is a clue for you:')
	print('Clue:','|'.join(map(str,y)))

def auth():
	token_input = input('Gimme the token: ')
	x = token_input.split('|')
	if (len(x) < 42):
		print('Are you kidding? It is invalid.')
		return
	x = [list(map(int,x[7*i:7*i+7])) for i in range(6)]
	y = generate(x)
	
	global token
	
	if (token == y):
		print('Wow, you are the 1337 one. Then I will give this to you.')
		try:
			print(open('flag.txt').read())
		except FileNotFoundError:
			print('The flag is not here, contact administrator if this happened.')
		exit()
	else:
		print('Are you kidding? It is invalid.')

def greeting():
	print('Welcome to Peppery Spittoon :P')
	print('How 1337 are ya?')
	
def print_menu():
	print('=============MENU=============')
	print('1. Generate token')
	print('2. Input token')
	print('3. Exit')
	print('==============================')
	print('What do you want?: ', end='')
	
if (__name__ == '__main__'):
	greeting()
	while(1):
		print_menu()
		try:
			choice = int(input())
			if (choice == 1):
				make_token()
			elif (choice == 2):
				auth()
			elif (choice == 3):
				print('Okay, bye!')
				exit()
			else:
				print('Try again.')
		except ValueError:
			print('Do not be salty. We are peppery :P')
		except KeyboardInterrupt:
			print('Okay, bye!')
			exit()
