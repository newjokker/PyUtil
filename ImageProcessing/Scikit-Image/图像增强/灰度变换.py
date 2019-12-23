# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from skimage import data
from skimage import exposure, img_as_float
import matplotlib.pyplot as plt


# ------------------- 灰度变换 -----------------------------------------------------------------------------------------
imge5 = img_as_float(data.coffee()) # 把图像的像素值转换为浮点数
gam1 = exposure.adjust_gamma(imge5, 2)  # 使用伽马调整，第二个参数控制亮度，大于1增强亮度，小于1降低。
log1 = exposure.adjust_log(imge5, 0.7)  # 对数调整

# 用一行两列来展示图像
plt.subplot(1, 3, 1)
# plt.imshow(imge5, plt.cm.gray)
plt.imshow(imge5)

plt.subplot(1, 3, 2)
# plt.imshow(gam1, plt.cm.gray)
plt.imshow(gam1)

plt.subplot(1, 3, 3)
# plt.imshow(log1, plt.cm.gray)
plt.imshow(log1)

plt.show()