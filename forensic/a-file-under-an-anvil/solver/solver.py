#!/usr/bin/python3
import nbt,io,re
import mca_reader as mcr

FILE = "r.-1.0.mca"
mca = mcr.Mca(FILE)

"""
In between "TAG_String('piece'): " and "\n\t\t\t\t\t\t}"
"""
RGX = r"""(?<=TAG_String\('piece'\): )(.*?)(?=\n\t\t\t\t\t\t})"""


string = ""

for x in range(32):
    for y in range(32):
        chunk = nbt.nbt.NBTFile(buffer = io.BytesIO(mca.get_data(x,y)))
        string += chunk.pretty_tree() + "\n"
        
flag = re.findall(RGX,string)
print("".join(flag))
