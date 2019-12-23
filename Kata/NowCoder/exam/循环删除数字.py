# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
每一遍先将对应的元素标记下来，到结束的时候进行删除
"""

a = list(range(8))

index = 2
while len(a) > 1:
    if index > len(a) - 1:
        print(a)
        index = index - len(a)
        b = a.copy()
        a = []
        for i in b:
            if i is not None:
                a.append(i)
    else:
        a[index] = None
        index += 3

print(a[0])
