# -*- coding: utf-8  -*-
# -*- author: jokker -*-

# 参考网址：https://www.runoob.com/numpy/numpy-array-manipulation.html

# 要弄懂的用法

# a[[1,2,3],:,:], 这种切片方式相当好用

# np.tile, 在 一维矩阵转为多纬矩阵中很好用，单波段图像转为多波段图像

# np.ix_

# np.reshape

# 线性插值

# np.nditer

# numpy.ndarray.flat 是一个数组元素迭代器

# numpy.ndarray.flatten 返回一份数组拷贝，对拷贝所做的修改不会影响原始数组

# numpy.ravel() 展平的数组元素，顺序通常是"C风格"，返回的是数组视图（view，有点类似 C/C++引用reference的意味），修改会影响原始数组。

# transpose，对换数组的维度

# ndarray.T	和 self.transpose() 相同

# rollaxis	向后滚动指定的轴, np.rollaxis(a,0, 3).shape ，将 (3,x,y) 转为 (x,y,3)

"""
numpy.rollaxis(arr, axis, start)
参数说明：

arr：数组
axis：要向后滚动的轴，其它轴的相对位置不会改变
start：默认为零，表示完整的滚动。会滚动到特定位置
"""

# swapaxes	对换数组的两个轴

"""
numpy.swapaxes(arr, axis1, axis2)
arr：输入的数组
axis1：对应第一个轴的整数
axis2：对应第二个轴的整数
"""

# broadcast	产生模仿广播的对象

# broadcast_to	将数组广播到新形状

# expand_dims	扩展数组的形状

# squeeze	从数组的形状中删除一维条目

# 连接数组

# concatenate	连接沿现有轴的数组序列

# stack	沿着新的轴加入一系列数组。
# hstack	水平堆叠序列中的数组（列方向）
# vstack	竖直堆叠序列中的数组（行方向）

# 分割数组

# split	将一个数组分割为多个子数组
# hsplit	将一个数组水平分割为多个子数组（按列）
# vsplit	将一个数组垂直分割为多个子数组（按行）

# 数组元素的增加与删除

# resize	返回指定形状的新数组
# append	将值添加到数组末尾
# insert	沿指定轴将值插入到指定下标之前
# delete	删掉某个轴的子数组，并返回删除后的新数组
# unique	查找数组内的唯一元素


# 矩阵翻转（镜像）


"""
for x in np.nditer(a, order='F'):Fortran order，即是列序优先；
for x in np.nditer(a.T, order='C'):C order，即是行序优先；

对象有另一个可选参数 op_flags。 默认情况下，nditer 将视待迭代遍历的数组为只读对象（read-only），为了在遍历数组的同时，
实现对数组元素值得修改，必须指定 read-write 或者 write-only 的模式。
for x in np.nditer(a, op_flags=['readwrite']): nditer

广播迭代
"""


#

