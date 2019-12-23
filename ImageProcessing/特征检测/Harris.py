# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import cv2
import numpy as np
from skimage import data
import matplotlib.pyplot as plt

# 参考 ： opencv3 计算机视觉 P84

img = cv2.imread(r'C:\Users\74722\Desktop\aa.png', cv2.COLOR_RGB2BGR)

# img = data.coffee()
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
gray = np.float32(gray)

dst = cv2.cornerHarris(gray, 2, 23, 0.04)

img[dst > 0.01*dst.max()] = [0, 0, 255]  # 超过阈值转为红色

cv2.imshow('candy', img)
cv2.waitKey()






