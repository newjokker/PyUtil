# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

#定义一个函数
ripple = lambda x,y:np.sqrt(x**2 + y**2) + np.sin(x**2 + y**2)

# 生成grid数据，复数定义了生成grid数据的step，若无该复数则step为5
grid_x, grid_y = np.mgrid[0:5:1000j, 0:5:1000j]

# 生成待插值的样本数据
xy = np.random.rand(1000, 2)
sample = ripple(xy[:,0] * 5 , xy[:,1] * 5)

# 用cubic方法插值
grid_z0 = griddata(xy * 5, sample, (grid_x, grid_y), method='linear')

plt.imshow(grid_z0)

plt.show()

print('ok')
