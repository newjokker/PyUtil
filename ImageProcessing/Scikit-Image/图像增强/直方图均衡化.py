# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from skimage import data, exposure
import matplotlib.pyplot as plt

# 直方图均衡化

img6 = data.coffee()
# 指定绘制的大小
plt.figure("hist", figsize=(8, 8))

# 把图像的二维数组按行转为一维数组，这样才能绘制直方图
arr = img6.flatten()

plt.subplot(2, 2, 1)
plt.imshow(img6, plt.cm.gray)
plt.subplot(2, 2, 2)
# 绘制直方图
plt.hist(arr, bins=256, normed=1, edgecolor='None', facecolor='red')

# 对直方图进行均衡化
img_c = exposure.equalize_hist(img6)
arr_c = img_c.flatten()
plt.subplot(2, 2, 3)
plt.imshow(img_c, plt.cm.gray)
plt.subplot(2, 2, 4)
plt.hist(arr_c, bins=256, normed=1, edgecolor='None', facecolor='red')

plt.show()
