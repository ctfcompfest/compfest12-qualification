#!/usr/bin/python
import random

GREET_STR = "Please end the input with new line character.\nInput the flag:\n"
FAIL_STR = "Lol, wrong flag, try again."
SUCCESS_STR = "Nice! You got it!"
FLAG = "COMPFEST12{d0n7_fck_y0uR_Br41n_l1K3_SEr10USlY_8f036017c2}" + "\n"

BF_PRINT_CLEAN = "->++++++++++[>#DIV#+[-<+]->-]>#MOD#+[-<+]>>[.[-]>]"

# Layout = 255 255 0 0 CharText_00_CharText 0 0 254 253 0 0 1 0 0 1 0 0 1 0 0 1 0 0 1 0 0 1 0 0 1 0 0 1 0 0 1 0 0 1
BF_PROGRAM     = "-> #PRINT_GREET_CLEAN# +[-<+]"                                                                                                      \
               + "->- ----------[++++++++++>>>,----------]++++++++++ >>> -- > --- >>> + >>> + >>> + >>> + >>> + >>> + >>> + >>> + >>> + >>> +"        \
               + "+++[---<+++]---"                                                                                                      \
               + "["                                                                                                                    \
               + " [>>> --[+++ +[[-<+]-<+]-> >>> #SUBS0# >>> <[-]+++[-[-->++]-->+++]---<++ ]]  >+++ >[-]+ <[[-]<++>>-<] >[-<--->]<<"    \
               + " [>>> --[+++ +[[-<+]-<+]-> >>> #SUBS1# >>> <[-]+++[-[-->++]-->+++]---<++ ]]  >+++ >[-]+ <[[-]<++>>-<] >[-<--->]<<"    \
               + " [>>> --[+++ +[[-<+]-<+]-> >>> #SUBS2# >>> <[-]+++[-[-->++]-->+++]---<++ ]]  >+++ >[-]+ <[[-]<++>>-<] >[-<--->]<<"    \
               + " [>>> --[+++ +[[-<+]-<+]-> >>> #SUBS3# >>> <[-]+++[-[-->++]-->+++]---<++ ]]  >+++ >[-]+ <[[-]<++>>-<] >[-<--->]<<"    \
               + " [>>> --[+++ +[[-<+]-<+]-> >>> #SUBS4# >>> <[-]+++[-[-->++]-->+++]---<++ ]]  >+++ >[-]+ <[[-]<++>>-<] >[-<--->]<<"    \
               + " [>>> --[+++ +[[-<+]-<+]-> >>> #SUBS5# >>> <[-]+++[-[-->++]-->+++]---<++ ]]  >+++ >[-]+ <[[-]<++>>-<] >[-<--->]<<"    \
               + " [>>> --[+++ +[[-<+]-<+]-> >>> #SUBS6# >>> <[-]+++[-[-->++]-->+++]---<++ ]]  >+++ >[-]+ <[[-]<++>>-<] >[-<--->]<<"    \
               + " [>>> --[+++ +[[-<+]-<+]-> >>> #SUBS7# >>> <[-]+++[-[-->++]-->+++]---<++ ]]  >+++ >[-]+ <[[-]<++>>-<] >[-<--->]<<"    \
               + " [>>> --[+++ +[[-<+]-<+]-> >>> #SUBS8# >>> <[-]+++[-[-->++]-->+++]---<++ ]]  >+++ >[-]+ <[[-]<++>>-<] >[-<--->]<<"    \
               + " [>>> --[+++ +[[-<+]-<+]-> >>> #SUBS9# >>> <[-]+++[-[-->++]-->+++]---<++ ]]  -->"                                     \
               + "]"                                                                                                                    \
               + "+[[-<+]-<+]>"                                                                                                         \
               + "-[+>>> [>+++>+ <[--->-<<[-] -< +[-<+]- <+>> +[->+]>] >[-<---<++<+>>>] <<] <[>+<-] >-]-- "                             \
               + ">"                                                                                                                    \
               + "++[[-]>++]"                                                                                                           \
               + "+[[-]<+]-"                                                                                                            \
               + ">+<<[[-]>>-> #PRINT_CLEAN_FAIL# +[-<+] <] >>[-> #PRINT_CLEAN_SUCCESS# +[-<+]]"
               
BF_SUB         = ">+++>+ <[>-<---] >[-<--- +[[-<+]-<+]-> >>>>>]<<  <[-]>>[-]>[-]#SUB#[<<<+>[<->-[>+<-]]>[<+>-]<<[->-<]>>>-]<<"
BF_OUT         = ""
               
"""

                                                                                    # Start at 253:
BF_SUBS_CELL   =   "[>>> --[+++ +[[-<+]-<+]-> >>> #THE_SUBS# >>>++]]"               # If 1st next cell is not 2 then run The Subs.
BF_IF_CELL     =   ">>>+++  <<[-]+ >[-]"                                            # Else if 2nd next cell is not 253
                 + ">[---<<<++ >- >> [<+>-]] <[>+<-]"                               # then add revert changes and continue next cell.
                 + "<[>>---<< -] <"                                                 # Else revert changes and back to 254.
BF_LAST_CELL   =   "-->>>"                                                          # For at 254 then make this cell 254 again else make the last 1s cell to 254.

BF_CHECK       =   "+[[-<+]-<+]>"                                                   # Back to 255|255 START and change 255|255 START to 0|255 START
                 + ">>>++[-- [[-] -< +[-<+]- <+>> +[->+]] >>>++]"                   # Count how many character mistakes until 254
                 + "++[[-]>++]"                                                     # Clean up right until hits 254
                 + "+[[-]<+]-"                                                      # Clean up left until hits 255
                 + ">+<<[[-]>>-> #PRINT_CLEAN_FAIL# <]"                             # If character mistakes > 0 then print FAIL_STR
                 + ">>[#PRINT_CLEAN_SUCCESS#]"                                      # Else print SUCCESS_STR
"""

def print_brainfuck(txt):
    lst = list(txt)
    div_lst = [ord(x) // 10 for x in lst]
    mod_lst = [ord(x) % 10 for x in lst]
    DIV = '>'.join(['+'*i for i in div_lst])
    MOD = '>'.join(['+'*i for i in mod_lst])
    tmp = BF_PRINT_CLEAN.replace('#DIV#',DIV)
    tmp2 = tmp.replace('#MOD#',MOD)
    return tmp2

def rand_decomposition(num,length):
    r = num // length
    lst = []
    for i in range(length):
        n = random.randint(0, r)
        lst.append(n)
        num -= n
    for i in range(num):
        lst[i % length] += 1
    return lst
   
def gen_subs(cell_length):
    subs = [rand_decomposition(ord(x),int(cell_length)) for x in list(FLAG)]
    cells = []
    for i in range(10):
        bf_sub = '>>>'.join(BF_SUB.replace('#SUB#','+'*x[i]) for x in subs)
        cells.append(bf_sub)
    return cells

def minify(txt):
    txt = txt.replace(' ','')
    tmp = ''
    for i in range(len(txt)):
        if (i % 80 == 0):
            tmp += '\n' + txt[i]
        else:
            tmp += txt[i]
    return tmp

BF_OUT = BF_PROGRAM
subs_lst = gen_subs(10)
for i in range(len(subs_lst)):
    BF_OUT = BF_OUT.replace('#SUBS' + str(i) + '#',subs_lst[i])

BF_OUT = BF_OUT.replace('#PRINT_CLEAN_FAIL#',print_brainfuck(FAIL_STR))
BF_OUT = BF_OUT.replace('#PRINT_CLEAN_SUCCESS#',print_brainfuck(SUCCESS_STR))
BF_OUT = BF_OUT.replace('#PRINT_GREET_CLEAN#',print_brainfuck(GREET_STR))

print(minify(BF_OUT))