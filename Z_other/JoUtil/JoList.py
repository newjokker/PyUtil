# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import copy


# 遍历的时候可以动态改变数据


class JoList(list):

    def __init__(self, init_list=None):
        super(JoList, self).__init__()
        if init_list:
            self.extend(init_list)

    def __add__(self, other):
        self.extend(other)
        return self

    def __sub__(self, other):
        return filter(lambda x: x not in other, self)

    def _check_empty(self):
        if not self:
            raise EOFError("list is empty")

    def choose(self, other):
        """ __sub__ 的反向操作"""
        return filter(lambda x: x in other, self)

    def as_type(self, func):
        """输入方法规范数据类型，这样写着别人看得懂"""
        self._check_empty()
        return map(func, self)

    def copy(self):
        return copy.deepcopy(self)

    def is_single_class(self):
        """是不是单层的, 元素中存在 dict list tuple set 都不算是单层的要素"""
        self._check_empty()
        for each_ele in self:
            if isinstance(each_ele, dict) or isinstance(each_ele, list) \
                    or isinstance(each_ele, tuple) or isinstance(each_ele, set):
                return False
        return True

    def isomorphism(self):
        """数据是不是同构的，列表中的所有元素是不是都是一样的类型"""
        self._check_empty()

        list_type = type(self[0])

        for each_ele in self[1:]:
            if type(each_ele) != list_type:
                return False
        return True


if __name__ == "__main__":
    a = JoList()

    a.append('1')
    a.append('2')

    b = a.copy()
    b.append('3')

    b.append(456)

    print('-' * 100)
