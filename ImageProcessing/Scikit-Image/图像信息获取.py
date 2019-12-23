# -*- coding: utf-8  -*-
# -*- author: jokker -*-

# 参考 ： https://blog.csdn.net/weixin_42346564/article/details/85160079

from skimage import io, data

img = data.chelsea()
# io.imshow(img)
# io.show()

"""
打印图片信息
"""

print(type(img))  # 类型
print(img.shape)  # 形状
print(img.shape[0])  # 图片宽度
print(img.shape[1])  # 图片高度
print(img.shape[2])  # 图片通道数
print(img.size)  # 显示总像素个数
print(img.max())  # 最大像素值
print(img.min())  # 最小像素值
print(img.mean())  # 像素平均值
