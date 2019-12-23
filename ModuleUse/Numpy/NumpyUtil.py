# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import numpy as np

"""需要整理和掌握的 numpy 函数

* 百分位数
np.percentile(a, i, interpolation='midpoint')

* 裁切
np.clip(array, 0, inf) : 小于 0 变为 0

* 第一个非零元素的索引 
np.flatnonzero(array, 'ms') 


# 有 arg 的都是找的位置
np.argwhere(array==12) : 返回 array 中值为 12 的数据的位置，array 是几维，坐标就是几维
np.argmax()
np.argmin()

* 从 0 开始加 1 的一维矩阵
np.arange(100)

* 镜像
np.flip()

* 拼接
np.stack()

"""



class NumpyUtil(object):

    @staticmethod
    def flip(b, axis=1):
        """镜像"""
        np.flip(b, axis=1)

        # 左右翻转
        np.fliplr(b)

        # 上下翻转
        np.flipud(b)

        # 正反镜像

        # FIXME 旋转一定的角度

    @staticmethod
    def stack():
        """拼接"""
        np.stack()
        np.vstack()
        np.dstack()
        np.hstack()




