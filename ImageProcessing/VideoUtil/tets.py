# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import cv2
import matplotlib.pyplot as plt


vc = cv2.VideoCapture(r'D:\000_缓存\Thunder\辛普森一家.The.Simpsons.S30E20.中英字幕.WEBrip.720P-人人影视.mp4')

index = 0
need = [57 * 24 - 10, 57 * 24 + 10]

vc.set(cv2.CAP_PROP_POS_FRAMES, need[0])  # 指定帧

while True:
    index += 1
    a = vc.read()  # 读取一帧影像
    cv2.imwrite(r'C:\Users\Administrator\Desktop\del\deldel\{0}.png'.format(index), a[1])  # 将数据写到本地

    if index > 10:
        break
