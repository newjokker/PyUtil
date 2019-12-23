# -*- coding: utf-8  -*-
# -*- author: jokker -*-

# 参考 ： https://docs.python.org/zh-cn/3/library/multiprocessing.html

"""
* multiprocessing 是一个用于产生进程的包，具有与 threading 模块相似API。

*  multiprocessing 包同时提供本地和远程并发，使用子进程代替线程，有效避免 Global Interpreter Lock 带来的影响。因此，
multiprocessing 模块允许程序员充分利用机器上的多核。可运行于 Unix 和 Windows 。

* multiprocessing 模块还引入了在 threading 模块中没有的API。一个主要的例子就是 Pool 对象，它提供了一种快捷的方法，
赋予函数并行化处理一系列输入值的能力，可以将输入数据分配给不同进程处理（数据并行）。



* freeze_support
如果没有调用 freeze_support() 在尝试运行被冻结的可执行文件时会抛出 RuntimeError 异常。
对 freeze_support() 的调用在非 Windows 平台上是无效的。如果该模块在 Windows 平台的 Python 解释器中正常运行
(该程序没有被冻结)， 调用``freeze_support()`` 也是无效的。


"""



import multiprocessing
from multiprocessing import Pool


def f(x):
    return x*x


if __name__ == '__main__':
    with Pool(5) as p:
        print(p.map(f, [1, 2, 3]))








