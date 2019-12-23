# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
列表中删除最后一个元素比删除第一个元素要快得多得多，我试了一下能相差一百倍之多
使用 from collections import deque ，实现会快得多，特别是删除第一个元素的时候
"""

from collections import deque

# 栈：先进后出

# 节点 A 开始，找到子节点，入栈
# 从栈中拿取一个数据进行操作，有新的数据就入栈，没有新的数据重新拿一个数据，周而复始，直到栈中不存在元素了

"""
使用 deque 能大大简化深度遍历和广度遍历的代码
from collections import deque
入栈 append()
出栈 pop()
"""

# 使用栈得到 0 1 开始分叉，最后的个数

a = deque(['1'])
all = []
while len(a):

    # b = a.pop()
    b = a.popleft()
    if len(b) < 5:
        a.append(b+'0')
        a.append(b+'1')
    else:
        print(b)
        all.append(b)

print(len(all))






