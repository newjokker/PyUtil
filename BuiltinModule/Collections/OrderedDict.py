# -*- coding: utf-8  -*-
# -*- author: jokker -*-


"""
使用dict时，Key是无序的。在对dict做迭代时，我们无法确定Key的顺序。

如果要保持Key的顺序，可以用OrderedDict：


OrderedDict可以实现一个FIFO（先进先出）的dict，当容量超出限制时，先删除最早添加的Key：
"""

from collections import OrderedDict

od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])

# 注意，OrderedDict的Key会按照插入的顺序排列，不是Key本身排序：
od['z'] = 1
od['y'] = 2
od['x'] = 3

print(od.keys())  # 按照插入的Key的顺序返回
print(od)

