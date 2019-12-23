# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
注意点：
（1）必须三个方法一起出现
（2）属性名和方法名不能一样，三个方法名一定要一样
（3）设置和删除两个方法无返回值
"""


class Test(object):

    def __init__(self):
        self._name = ''

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, set_name):
        if len(set_name) > 10:
            print('name length must less then 10')
        else:
            self._name = set_name
            print('set name success')

    @name.deleter
    def name(self):
        raise TypeError('can not delete attribute')


if __name__ == "__main__":

    a = Test()

    a.name = '12'

    a.name = '12' * 10

    print(a.name)

    del a.name





