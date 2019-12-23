# -*- coding: utf-8  -*-
# -*- author: jokker -*-

# https://www.cnblogs.com/xinsiwei18/p/5937952.html


class MyType(type):

    def __call__(cls, *args, **kwargs):
        obj = cls.__new__(cls, *args, **kwargs)
        print('在这里面..')
        print('==========================')
        print('来咬我呀')
        obj.__init__(*args, **kwargs)
        return obj


class Foo(metaclass=MyType):

    def __init__(self):
        self.name = 'alex'


f = Foo()
print(f.name)