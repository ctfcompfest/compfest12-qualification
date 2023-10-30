#!/usr/bin/env python
import qrtools
from PIL import Image
import zbar
import cv2
import os

video_name = ['ichi','ni','san','shi','go','roku','sichi','hachi','kyu']

count = 0
for vid in video_name:
  vidcap = cv2.VideoCapture(vid+'.avi')
  success,image = vidcap.read()
  while success:
    cv2.imwrite("%d.png" % count, image)     # save frame as PNG file
    success,image = vidcap.read()
    qr = qrtools.QR()
    qr.decode('%d.png' % count)
    print 'inspecting frame number: %d' % count
    #print(qr.data)
    if ('COMPFEST' in qr.data):
        print(qr.data)
        exit()
    os.system('rm %d.png' % count)
    count += 1
