# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
* 我从代码中体会到的东西
    * 函数两种调用方法 (1) self.method() (2) ClassName.method()  | 将静态函数当做实例函数使用的方法 ： self.stat_city(self, INV_tif, 'INV')
    * 一共有三种函数，（1）实例函数，用到实例属性 （2）静态函数，@staticmethod，不用类属性和实例属性 （3）类函数，@classmethod，用到类属性
    * 类属性和实例属性的区别，（1）属于所有函数还是由单一实例所有
    * 类属性和实例属性的区别 （类属性的特性）--> 磊哥实现单例模式使用的方法  --> 磊哥代码的进一步规范化（调用类属性，定义为类函数 @classmethod, cls 关键字）
"""

# 参考 : https://www.cnblogs.com/huchong/p/8244279.html


import time
import threading


class Singleton(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        time.sleep(1)

    @classmethod
    def instance(cls):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = Singleton()
        return Singleton._instance


# -----------------------------------------------------------------------------

# import threading
#
# class Singleton(object):
#     _instance_lock = threading.Lock()
#
#     def __init__(self):
#         pass
#
#
#     def __new__(cls, *args, **kwargs):
#         if not hasattr(Singleton, "_instance"):
#             with Singleton._instance_lock:
#                 if not hasattr(Singleton, "_instance"):
#                     Singleton._instance = object.__new__(cls)
#         return Singleton._instance
#
# obj1 = Singleton()
# obj2 = Singleton()
# print(obj1, obj2)
#
# def task(arg):
#     obj = Singleton()
#     print(obj)
#
# for i in range(10):
#     t = threading.Thread(target=task,args=[i,])
#     t.start()
#

if __name__ == "__main__":

    a = Singleton.instance()

    a.name = 'jokker'

    print(a.name)

    b = Singleton.instance()

    print(b.name)




