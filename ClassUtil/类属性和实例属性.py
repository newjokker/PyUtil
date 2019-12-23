# -*- coding: utf-8  -*-
# -*- author: jokker -*-

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