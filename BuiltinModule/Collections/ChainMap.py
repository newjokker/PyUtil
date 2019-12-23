# -*- coding: utf-8  -*-
# -*- author: jokker -*-

# 参考 ： https://www.cnblogs.com/BeautifulWorld/p/11712684.html

"""
ChainMap提供了一种多个字典整合的方式，它没有去合并这些字典，而是将这些字典放在一个 maps (一个列表)里，
内部实现了很多 dict 的方法，大部分 dict 的方法，ChainMap 都能使用。
"""

from collections import ChainMap

a = {'x': 1, 'z': 3}
b = {'y': 2, 'z': 4}
d = {'k': 3, 'z': 5}

c = ChainMap(a, b, d)

print(c['x'])  # Outputs 1 (from a)
print(c['y'])  # Outputs 2 (from b)
print(c['z'])  # Outputs 3 (from a)
print(c['k'])  # Outputs 3 (from a)

# 将多个字典的信息整合为一个字典的信息
# 和新增加一个字典的区别是，ChainMap 没有新建字典，这样就会节约内存
