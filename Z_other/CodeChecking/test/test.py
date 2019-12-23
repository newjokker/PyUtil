# -*- coding: utf-8  -*-
# -*- author: jokker -*-

# 参考 : https://blog.csdn.net/loner_fang/article/details/80877491
# 参考 : https://blog.csdn.net/loner_fang/article/details/80877491

"""
* 我从代码中体会到的东西

    * 函数两种调用方法 (1) self.method() (2) ClassName.method() (2)

    * 一共有三种函数，（1）实例函数，用到实例属性 （2）静态函数，@staticmethod，不用类属性和实例属性 （3）类函数，@classmethod，用到类属性

    * 类属性和实例属性的区别，（1）属于所有函数还是由单一实例所有

    * 类属性的特性 --> 磊哥实现单例模式使用的方法  --> 磊哥代码的进一步规范化（调用类属性，定义为类函数 @classmethod, cls 关键字）

"""


class A():

    lei_name = 'jokker'

    def __init__(self):
        self.name = 'jokker'

    def print_ok(self):
        print('ok')

    @staticmethod
    def print_ok_2():
        print('ok_2')
        # if a:
        #     print(a.name)

    @classmethod
    def print_ok_3(cls):
        print(cls.lei_name)

    def do_process(self):
        self.print_ok()
        self.print_ok_2()
        self.print_ok_3()

        # A.print_ok_2()
        # A.print_ok(self)




if __name__ == '__main__':

    a = A()
    a.do_process()

    b = A()
    A.lei_name = 'fucxk'  # 更改类属性，用于单例模式
    b.do_process()

    a.do_process()