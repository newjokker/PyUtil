# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
使用dict时，如果引用的Key不存在，就会抛出KeyError。如果希望key不存在时，返回一个默认值，就可以用defaultdict：
注意默认值是调用函数返回的，而函数在创建 defaultdict 对象时传入。
除了在Key不存在时返回默认值，defaultdict 的其他行为跟dict是完全一样的。
"""

from collections import defaultdict

dd = defaultdict(lambda: 'None')  # 默认函数是调用函数返回的

dd['key1'] = 'abc'
print(dd['key1'])  # key1存在
print(dd['key2'])  # key2不存在，返回默认值
