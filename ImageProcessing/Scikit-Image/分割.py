# -*- coding: utf-8  -*-
# -*- author: jokker -*-


from skimage import filters
from skimage import data
from skimage import color
import matplotlib.pyplot as plt

img = color.rgb2gray(data.coins())

thresh = filters.threshold_otsu(img)  # 基于otsu阀值分割方法
dst = (img <= thresh) * 1.0

plt.figure("img", figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.imshow(img, plt.cm.gray)

plt.subplot(1, 2, 2)
plt.title("otsu")
plt.imshow(dst, plt.cm.gray)

plt.show()