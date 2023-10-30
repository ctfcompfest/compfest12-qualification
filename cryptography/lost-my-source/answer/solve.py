the_chars = list(open('encrypted.txt').read())
the_nums = list()
for i in (the_chars):
	the_nums.append(ord(i))

decrypt_num = list()
for i in range(32):
	decrypt_num.append(the_nums[31-i]^i)
	
potential = 'COMPFEST12'
key = "abcdefghijklmnopqrstuvwxyzabcdef"


for i in range(len(potential)):
	character = ord(potential[i])
	for j in range(128):
		if ((j^character)==decrypt_num[i]):
			print(chr(j),chr(character))


for i in range(32):
	print(chr(ord(key[31-i])^decrypt_num[i]),end='')
