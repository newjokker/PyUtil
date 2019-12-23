# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
常用到的一些零碎，未能整理的内容整理
"""

import heapq
from collections import OrderedDict
from collections import Counter
from operator import itemgetter
from itertools import groupby
import random
from itertools import dropwhile
from itertools import islice
from itertools import permutations
from itertools import chain


class AssistUtil(object):

    def __init__(self):
        self.date = 123

    @staticmethod
    def find_nlargest_nsmallest(find_num, data, func=None, find_nlargest=True):
        """找到最大或者最好的几个元素"""
        if find_nlargest:
            return heapq.nlargest(find_num, data, key=func)
        else:
            return heapq.nsmallest(find_num, data, key=func)

        # use_example
        # a = {'a': 12, 'b': 24, 'c': 3}
        # b = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        # print AssistUtil.find_nlargest_nsmallest(2, a.values(), None)
        # print AssistUtil.find_nlargest_nsmallest(2, b, lambda x: x[1], False)

    @staticmethod
    def get_order_dict():
        """获得有序字典"""
        # TODO 书上说可以在生成xml的时候让字段变得有序，可以试一下
        return OrderedDict()

    @staticmethod
    def most_common(data, need_num=None):
        """找出序列中出现次数最多的元素，输入 list，返回值，第一个是元素值，第二个是元素个数"""
        counter = Counter(data)
        if need_num is None:
            return counter.most_common()
        else:
            return counter.most_common(need_num)

        # # use example
        # c = [1, 2, 3, 3, 2, 4, 5, 5, 6, 6, 332, 2, 22, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
        # print AssistUtil.most_common(c, 2)

    @staticmethod
    def sort_list_dict(assign_dict, assign_key):
        """使用公共键对字典列表进行排序"""
        return sorted(assign_dict, key=itemgetter(assign_key))

        # # use example
        # d = [{'a': 1}, {'a': 12}, {'a': 34}, {'a': 2}]
        # print AssistUtil.sort_list_dict(d, 'a')

    @staticmethod
    def group_by(assign_data, assign_key):
        """根据字典将字段分组"""
        assign_data.sort(key=itemgetter(assign_key))
        return groupby(assign_data, key=itemgetter(assign_key))

        # # use example
        # e = [
        #     {'a':'1', 'b':1323},
        #     {'a':'2', 'b':1243},
        #     {'a':'1', 'b':123},
        #     {'a':'2', 'b':125343},
        #     {'a':'3', 'b':1236},
        #     {'a':'2', 'b':1223},
        #     {'a':'3', 'b':12354},
        # ]
        # for a, each in AssistUtil.group_by(e, 'a'):
        #     print a
        #     for i in each:
        #         print

    # ------------------------ other ---------------------------------
    @staticmethod
    def reversed(data):
        """反序, 可以用于序列的反向输出"""
        return reversed(data)

    # 迭代排列组合
    @staticmethod
    def permutations(data, assign_num=None):
        """排列组合, 可以指定一次提取的个数"""
        for p in permutations(data, assign_num):
            print(p)


# 跳过可迭代对象的前一部分元素
def dropwhile():
    """跳过指定的一些行"""
    with open(r'', 'r') as f:
        for line in dropwhile(lambda x: x.startswith('#'), f):
            print(line)


# 知道要跳过多少元素
def islice():
    """知道要跳过多少行，跳过他们"""
    items = [1, 2, 3, 4, 5, 6, 7]
    # 输出除乐前三个元素之外的所有元素
    for x in islice(items, 3, None):
        print(x)


# 对多个序列进行迭代
def chain(data):
    """对多个序列进行迭代，可以使用 chain 将多个序列锁起来"""
    for i in chain([1, 2, 3], {4, 5, 6}, (7, 8, 9)):
        print(i)


if __name__ == '__main__':

    a = {'a': 12, 'b': 24, 'c': 3}

    b = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    c = [1, 2, 3, 3, 2, 4, 5, 5, 6, 6, 332, 2, 22, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]

    # c = ['1','2','3','4','1']

    d = [{'a': 1}, {'a': 12}, {'a': 34}, {'a': 2}]

    e = [
        {'a': '1', 'b': 1323},
        {'a': '2', 'b': 1243},
        {'a': '1', 'b': 123},
        {'a': '2', 'b': 125343},
        {'a': '3', 'b': 1236},
        {'a': '2', 'b': 1223},
        {'a': '3', 'b': 12354},
    ]

    print(AssistUtil.find_nlargest_nsmallest(2, a.values(), None))
    print(AssistUtil.find_nlargest_nsmallest(2, b, lambda x: x[1], False))

    print(AssistUtil.most_common(c, 2))

    for a, each in AssistUtil.group_by(e, 'a'):
        print(a)
        for i in each:
            print(i)
