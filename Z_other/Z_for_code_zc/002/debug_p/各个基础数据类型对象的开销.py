# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import sys

print('str : ', sys.getsizeof(''))
print('int : ', sys.getsizeof(int()))
print('float : ', sys.getsizeof(float()))
print('list : ', sys.getsizeof(list()))
print('dict : ', sys.getsizeof(dict()))
print('set : ', sys.getsizeof(set()))
print('tuple : ', sys.getsizeof(tuple()))
print('string : ', sys.getsizeof(""))


# 为什么矩阵应该存在数组里面而不是列表里面
# 为什么 gdal 返回 6 参数使用的是 tuple
