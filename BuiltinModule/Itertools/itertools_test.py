# -*- coding: utf-8  -*-
# -*- author: jokker -*-

# 参考：https://blog.csdn.net/sinat_38682860/article/details/98963728,
# https://blog.csdn.net/weixin_41084236/article/details/81626968


"""
itertools 是python的迭代器模块，itertools提供的工具相当高效且节省内存。
使用这些工具，你将能够创建自己定制的迭代器用于高效率的循环。

* count(初值=0, 步长=1):count 迭代器会返回从传入的起始参数开始的均匀间隔的数值。count 也可以接收指定的步长参数。

* islice(count(10), 5)：从 10 开始，输出 5 个元素后结束。islice 的第二个参数控制何时停止迭代。
但其含义并不是”达到数字 5 时停止“，而是”当迭代了 5 次之后停止“。

* cycle:这里我们创建了一个 for 循环，使其在三个字母 XYZ 间无限循环。

* accumulate(可迭代对象[, 函数])
　　 accumulate 迭代器将返回累计求和结果，或者传入两个参数的话，由传入的函数累积计算的结果。默认设定为相加，

* chain 迭代器能够将多个可迭代对象合并成一个更长的可迭代对象。

* itertools.repeat(object[, times]),object为可迭代对象 ,times为迭代次数，默认为无限次

* compress(data, selectors),data为数据对象 ,selectors为选择器(规则),作用:返回数据对象中对应规则为True的元素

"""

from itertools import chain
from itertools import count
from itertools import islice
from itertools import cycle
from itertools import accumulate
from itertools import repeat
from itertools import groupby
import itertools
import operator


class ItertoolsUtil(object):

    # todo 还有一部分未进行整理，只整理觉得现阶段有用的内容

    @staticmethod
    def count_test():
        # 从10开始无限循环
        for i in count(10, 12):
            if i > 200:
                break
            else:
                print(i)

    @staticmethod
    def islice_test():
        for i in islice(count(10), 5):
            print(i)

    @staticmethod
    def cycle_test():
        count = 0
        for item in cycle('XYZ'):
            if count > 7:
                break
            print(item)
            count += 1

    @staticmethod
    def accumulate_test():
        print(list(range(1, 10)))
        print(list(accumulate(range(1, 10))))
        print(list(accumulate(range(1, 10), operator.mul)))

    @staticmethod
    def chain_test():
        numbers = list(range(5))
        cmd = ['ls', '/some/dir']
        my_list = list(chain(['foo', 'bar'], cmd, numbers))
        print(my_list)

    @staticmethod
    def repeat_test():
        its = ['1', '2', '3', '4']
        for item in repeat(its, 4):
            print(item)

    @staticmethod
    def compress_test():
        """输出正确的数据"""
        its = ["a", "b", "c", "d", "e", "f", "g", "h"]
        selector = [True, False, 1, 0, 3, False, -2, "y"]
        for item in itertools.compress(its, selector):
            print(item)

    @staticmethod
    def group_by_test():
        """
        要想对整体进行分组需要先进行排序，因为这个函数只会把邻近的属于一组的数据放在一起，如果不排序分组的话，适合识别 excel
        中的哪些单元格可以合并
        """
        assign_data = [
            {'a': '1', 'b': 1323},
            {'a': '2', 'b': 1243},
            {'a': '1', 'b': 123},
            {'a': '2', 'b': 125343},
            {'a': '3', 'b': 1236},
            {'a': '2', 'b': 1223},
            {'a': '3', 'b': 12354},
        ]
        #
        assign_data.sort(key=operator.itemgetter('a'))
        #
        for key_str, each_item in groupby(assign_data, key=operator.itemgetter('a')):
            print(key_str)
            for i in each_item:
                print(i)

    @staticmethod
    def dropwhile_test():
        """跳过指定的行"""
        # fixme 结果和想的不一致，查找哪里出了问题
        with open(r'C:\Users\Administrator\Desktop\123.txt', 'r', encoding='utf-8') as f:
            for line in itertools.dropwhile(lambda x: len(x) < 3, f):
                print(line)

    @staticmethod
    def permutations_test():
        """排列组合"""
        data = [1, 2, 3, 4, 5]
        assign_num = 2
        for p in itertools.permutations(data, assign_num):
            print(p)


if __name__ == '__main__':

    # todo 模仿真实的文件，并进行读取
    # todo 完善每个函数对应的解释

    ItertoolsUtil.permutations_test()
