# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import scipy.ndimage as ndi
from skimage import data
import numpy as np
import matplotlib.pyplot as plt
from skimage import morphology

coin = data.coins()  # 选择图像

mean_0 = lambda x: np.percentile(x, 50)  # 自定义的卷积函数


foot_print = morphology.disk(radius=1)  # 卷积核的大小 radius = 3 就是 7*7 的窗口
# a = ndi.generic_filter(coin, mean_0, footprint=foot_print)
a = ndi.generic_filter(coin, mean_0, size=3)  #

plt.imshow(a, cmap='gray')
plt.show()

