# -*- coding: utf-8  -*-
# -*- author: jokker -*-

# 参考 ： https://blog.csdn.net/zhtysw/article/details/80510113

"""
* operator模块输出一系列对应Python内部操作符的函数。例如：operator.add(x, y)等价于表达式x+y。
许多函数的名称都被一些特定的方法使用，没有下划线加持。为了向下兼容，它们中的许多都保留着由双下划线的变体。
那些不具备双下划线的变体是为了使表达更清晰。

* 这些函数在各种函数目录里扮演者对相比较、逻辑操作、数学运算以及序列操作等角色。

* 对于所有对象来讲对象比较函数是十分有用的，并且这些函数以它们支持的丰富的比较操作命名。
"""

from operator import itemgetter

a = itemgetter([1,2,3])

print(a)
