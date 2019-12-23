# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from skimage import data, io
import cv2
import matplotlib.pyplot as plt


coffee = data.coffee()  # skimage 载入自带图像，


# plt.imshow(coffee, cmap='gray')  # 灰色模式
# plt.imshow(coffee)
# plt.show()

plt.subplot(221), plt.imshow(coffee)  # 多个图像一起展示
plt.subplot(222), plt.imshow(coffee)
plt.show()


# cv2.imshow('candy', array)
# cv2.waitKey()