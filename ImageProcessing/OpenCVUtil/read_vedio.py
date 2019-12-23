# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import cv2
import matplotlib.pyplot as plt


vc = cv2.VideoCapture(r'C:\迅雷下载\爱宠大机密2.mp4')

index = 0
while True:
    index += 1
    a = vc.read()  # 读取一帧影像
    if index % (24*5) == 1:
        print(index)
        cv2.imwrite(r'C:\Users\74722\Desktop\img\{0}.png'.format(index), a[1])  # 将数据写到本地
