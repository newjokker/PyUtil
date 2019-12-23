# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""自定义卷积函数"""

import numpy as np
import cv2
from skimage import data
import matplotlib.pyplot as plt
# from ArcpyUtil.classification_zonal_statistics.GdalUtil import GdalBase


im_data = data.coins()  # 硬币图像

core = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]).astype(np.float32)/9  # 卷积核
res = cv2.filter2D(im_data, -1, core)  # 卷积

# 查看图像
plt.subplot(211),plt.imshow(im_data, cmap = 'gray')
plt.subplot(212),plt.imshow(res, cmap = 'gray')
plt.show()

