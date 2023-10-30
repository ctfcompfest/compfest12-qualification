

from zipbomb import write_zip_quoted_overlap
import string
import random
import os
import shutil

def get_random_string(n=100):
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    result_str = ''.join(random.choice(letters) for i in range(100))
    return result_str

flag = "COMPFEST12{2iP_f11e_Go35_kAAbo0ooOoOm_25a919}"
num_files = [10*i for i in range(len(flag))]
num_files[0] = 2
sizes = [1000, 5000, 10000, 100000] + [1000000*i for i in range(1, len(flag)-3)]


if os.path.exists("hasil_generate/"):
	shutil.rmtree("hasil_generate/")

os.mkdir("hasil_generate/")

for i in range(len(flag)):
	print(i)
	filename = str(i+1) + ".zip"
	write_zip_quoted_overlap(open(f"hasil_generate/{filename}", "wb"), num_files[i], compressed_size=sizes[i], max_uncompressed_size=None, compression_method=8, zip64=True, template=[], extra_tag=None, max_quoted=0, flag=ord(flag[i]))

print("Done!")
