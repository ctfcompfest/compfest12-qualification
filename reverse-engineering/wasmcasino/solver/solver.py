import os

#require WABT module
os.system("wasm-decompile index.wasm -o index2.c")

# On jacpot, address of flag in memory is printed,
# revealing the flag char squence.
# Can also use objdump...
f = open("index2.c")
a = f.readlines()
flag = ("".join(a[913:925])).replace('"', "").replace('\\00', "").replace(' ', "").replace('\n', "")[10:87]

print(flag)

os.system("rm index2.c")