import re

FILE = 'lol.bf'
f = open(FILE).read().replace("\n","")

#Find Substraction Cell for each cycle using regex
#START = "[>>>--[++++[[-<+]-<+]->>>>"
#END   = ">>><[-]+++[-[-->++]-->+++]---<++]]" (See Documentation)
RGX_CELL = r"""(?<=\[>>>--\[\+\+\+\+\[\[-<\+]-<\+]->>>>)(.*?)(?=>>><\[-]\+\+\+\[-\[-->\+\+]-->\+\+\+]---<\+\+]])"""
cell_lst = re.findall(RGX_CELL,f)

#Find Substraction Cell for each character using regex
#START  = ">+++>+<[>-<---]>[-<---+[[-<+]-<+]->>>>>>]<<<[-]>>[-]>[-]"
#END    = "[<<<+>[<->-[>+<-]]>[<+>-]<<[->-<]>>>-]<<" (See Documentation)
RGX_SUB  = r"""(?<=>\+\+\+>\+<\[>-<---]>\[-<---\+\[\[-<\+]-<\+]->>>>>>]<<<\[-]>>\[-]>\[-])(.*?)(?=\[<<<\+>\[<->-\[>\+<-]]>\[<\+>-]<<\[->-<]>>>-]<<)"""
sub_lst  = [re.findall(RGX_SUB,x) for x in cell_lst]

#Populate character list by length
str_lst = [0 for x in sub_lst[0]]

#Adding the length of '+' operation to determine ASCII char
for x in sub_lst:
    for y in range(len(x)):
        str_lst[y] += len(x[y])
        
#Print flag
flag = ""
for x in str_lst:
    flag = flag + chr(x)
    
print repr(flag)