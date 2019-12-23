# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
Counter是一个简单的计数器，例如，统计字符出现的个数：

Counter({'g': 2, 'm': 2, 'r': 2, 'a': 1, 'i': 1, 'o': 1, 'n': 1, 'p': 1})
Counter实际上也是dict的一个子类，上面的结果可以看出，字符'g'、'm'、'r'各出现了两次，其他字符各出现了一次。

小结
collections模块提供了一些有用的集合类，可以根据需要选用。
"""

from collections import Counter
c = Counter()
for ch in 'programming':
    c[ch] = c[ch] + 1

print(c)



