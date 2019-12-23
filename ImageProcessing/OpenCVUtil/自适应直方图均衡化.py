# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import cv2
import numpy as np
from PIL import Image
import scipy
import matplotlib.image as img

# 参考 ： https://www.cnblogs.com/my-love-is-python/p/10405811.html

data = img.imread(r'C:\Users\Administrator\Desktop\aaa.jpg')

# cv2.equalizeHist(img)  # 表示进行直方图均衡化

clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(10, 10))  # 用于生成自适应均衡化图像, # LAB 它是用数字化的方法来描述人的视觉感应 https://blog.csdn.net/denghecsdn/article/details/78031825
claheB = clahe.apply(np.array(data, dtype=np.uint8))
cv2.imwrite(r'C:\Users\Administrator\Desktop\123.png', data)

# FIXME 可以先调整为 LAB 颜色空间，然后对 L（light）进行直方图自适应均衡化，就能让整个图片的亮度保持均衡

# 参数说明：clipLimit : 颜色对比度的阈值， titleGridSize : 进行像素均衡化的网格大小，即在多少网格下进行直方图的均衡化操作