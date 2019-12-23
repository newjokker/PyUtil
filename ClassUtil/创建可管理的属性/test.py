# -*- coding: utf-8  -*-
# -*- author: jokker -*-

# 参考 : https://python3-cookbook.readthedocs.io/zh_CN/latest/c08/p06_create_managed_attributes.html


class Person:
    def __init__(self, first_name):
        self.first_name = first_name

    # Getter function
    @property
    def first_name(self):
        return "first name : {0}".format(self._first_name)

    # Setter function
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    # Deleter function (optional)
    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")


if __name__ == "__main__":

    a = Person('jokker')

    a.first_name = 12

    print(a.first_name)

    del a.first_name
