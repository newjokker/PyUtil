# -*- coding: utf-8  -*-
# -*- author: jokker -*-

# 参考 ： https://www.liaoxuefeng.com/wiki/897692888725344/973805065315456

from collections import namedtuple

"""
但是，看到(1, 2)，很难看出这个tuple是用来表示一个坐标的。定义一个class又小题大做了，这时，namedtuple就派上了用场
"""

Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
print(p.x)
print(p.y)

# 这个特性在很多的地方非常有用，在 出 xml 中的 table 的时候，都是用的字典来做，如果用一个这样的 tuple 会方便太多，这个思维非常不错

"""
namedtuple是一个函数，它用来创建一个自定义的tuple对象，并且规定了tuple元素的个数，并可以用属性而不是索引来引用tuple的某个元素。
这样一来，我们用namedtuple可以很方便地定义一种数据类型，它具备tuple的不变性，又可以根据属性来引用，使用十分方便。
"""
