# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
使用list存储数据时，按索引访问元素很快，但是插入和删除元素就很慢了，因为list是线性存储，数据量大的时候，插入和删除效率很低。
deque是为了高效实现插入和删除操作的双向列表，适合用于队列和栈：
deque除了实现list的 append() 和 pop() 外，还支持 appendleft()和 popleft()，这样就可以非常高效地往头部添加或删除元素。
"""

from collections import deque

q = deque(['a', 'b', 'c'])
q.append('x')
q.pop()
q.appendleft('left')
q.appendleft('left_2')
q.popleft()

print(q)
