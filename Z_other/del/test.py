# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import cv2


import sys
import scipy
import numpy as np
from scipy import spatial
from scipy.spatial.distance import cdist

sys.path.append(r'D:\Code\GdalUtil\Function')

from ReadData.PickleUtil import PickleUtil

# 读取矩阵数据
data = PickleUtil.load_data_from_pickle_file(r'C:\Users\Administrator\Desktop\GX\test.pkl')
lon = data['lon']
lat = data['lat']


# 转为一维矩阵
a = lon.flatten()
a2 = lat.flatten()

# 生成 X * 2  样式的矩阵
b = np.zeros((a.shape[0], 2))
b[:, 0] = a
b[:, 1] = a2

# 计算指点点和所有点的距离
assign_point = np.array([(109.4, 25.23)])  # 指定点的坐标
distance = cdist(b, assign_point, metric='euclidean')  # 计算指定点和所有点之间的距离

# 找到最近点的行列号
loc = np.argwhere(distance==min(distance))[0]  # 找到距离最小点的位置
x, y = loc[0]/lon.shape[0], loc[0]%lon.shape[0]  # 转为二维坐标

print(x, y)  # 打印二维行列号
print(lon[x, y], lat[x, y])  # 打印二维坐标对应的 经纬度值，用于核对






