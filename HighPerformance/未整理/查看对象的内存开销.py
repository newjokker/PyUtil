# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
* 单位是字节
* 一般都有两种方式来看，sys.getsizeof() 和  object.__sizeof__()
* 对于列表，只是记录列表本身的开销，一个元素占用 8 个字节
"""

import sys
import random

# todo 写一个遍历列表的函数，计算里面每个元素的开销，加上列表本身的开销

a = []
for i in range(10**8):
    a.append(random.randrange(1,12))

size_a = sys.getsizeof(a)
size_b = a.__sizeof__()
size_c = [[1], 2.4, 3.2].__sizeof__()
print(format(size_a/1024/1024, '.4f'), 'M')
print(format(size_b/1000/1000, '.4f'), 'M')
print(format(size_c, '.4f'), '字节')  # list 开销 40 字节，一个 int 8 字节


