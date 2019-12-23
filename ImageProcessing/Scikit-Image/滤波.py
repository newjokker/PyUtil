# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
支持的滤波类型
"""

from skimage import filters
from skimage import data
import skimage.morphology as sm
import matplotlib.pyplot as plt

image = data.coins()
edges = filters.median(image, sm.disk(5))  # 中值滤波, 第二个参数代表滤波器的形状，disk代表平面圆形，当然还有什么正方形，矩形啥的

plt.subplot(1, 2, 1)
plt.imshow(image, plt.cm.gray)

plt.subplot(1, 2, 2)
plt.imshow(edges, plt.cm.gray)

plt.show()