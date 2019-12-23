# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from skimage import data, io
import cv2
import matplotlib.pyplot as plt

# ------------------------- 读取图片 -----------------------------------------------------------------------------------
img = io.imread(r'C:\Users\74722\Desktop\test.jpg', cv2.COLOR_RGB2BGR)  # skimage 读取图像，返回矩阵, 通常使用 BGR 模式

coins = data.coins()  # skimage 载入自带图像，

happy = data.jokker_good()  # 读取自定义图片，可以通过修改 py 文件放入自己喜欢的图片 D:\Anaconda\envs\MachineLearning\Lib\site-packages\skimage\data\__init__.py

image = cv2.imread(r'C:\Users\74722\Desktop\test.jpg', cv2.IMREAD_GRAYSCALE)  # cv2 以灰色模式读取图像，返回的是 array

# ------------------------- 写图片 -------------------------------------------------------------------------------------

io.imsave(r'C:\Users\74722\Desktop\b32.png', coins)  # skimage 保存图像

cv2.imwrite(r'C:\Users\74722\Desktop\b32324.png', happy)  # FIXME 以灰色模式进行保存, 写的时候是 BGR 和 常用的 RGB 是相反的要注意

plt.imshow(image, cmap='gray')
plt.show()







