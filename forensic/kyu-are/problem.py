#!/usr/bin/env python3
import qrcode
import cv2
import os
import itertools
import random
from PIL import Image

#numbers of qrcodes, should be congruent to 1 (mod 9)
n = 10000
if (n % 9 != 1):
    print('wrong number of qrcodes!')
    exit()

#the obfuscator
items = ['D34DC0D3','D34DB33F!22153','!388131337133713371337','uuuulalalal','papapapa','skiddiesulajfjabjgkagba','do','you','understand?']
permutations_object = itertools.permutations(items)
permutations_list = list(permutations_object)

#the flag i is in one of the videos
flag = 'COMPFEST12{kyu4r31337_318bc0}'
flag += ''.join(items)
flag = flag[:len(''.join(items))]
#print(flag)    
flag_number = 8086
flag_image = qrcode.make(flag) 

#process the qrcodes
img_array = []
video_name = ['ichi','ni','san','shi','go','roku','sichi','hachi','kyu']

i = 0
now = 0
for filename in range (n-1):
    rd = random.randint(0,len(permutations_list)-1)
    if (flag_number == filename):
        flag_image = flag_image.resize((128,128),Image.ANTIALIAS)
        flag_image.save('flag.png')
        flag_img = cv2.imread('flag.png')
        img_array.append(flag_img)
        #print('now we are making flag.png')
        os.system('rm flag.png')
    the_image = qrcode.make(''.join(permutations_list[rd]))
    the_image = the_image.resize((128,128),Image.ANTIALIAS)
    the_image.save('%d.png' % filename)
    img = cv2.imread('%d.png' % filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
    #print('now we are making %s.png' % filename)
    os.system('rm %d.png' % filename)
    
    #processing the videos    
    if ((filename%100 == 0 or (filename+1)%(n//9)==0)  and filename>0): 
        print('processing',video_name[i]+str(now),'with',len(img_array),'frames')
        out = cv2.VideoWriter(video_name[i]+str(now)+'.avi',cv2.VideoWriter_fourcc(*'DIVX'), 100, size)
        for j in range(len(img_array)):
            out.write(img_array[j])
        out.release()
        img_array = []
        now += 1

    if ((filename+1)%(n//9)==0 and filename>0):
        the_vids = [video_name[i]+str(p)+'.avi' for p in range(now)]
        os.system('ffmpeg -i "concat:%s" -c copy %s.avi' %('|'.join(the_vids),video_name[i]))
        os.system('rm %s' % ' '.join(the_vids))
        i += 1
        now = 0

print('DONE!')
