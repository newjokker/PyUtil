# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import threading
import time

"""
需要执行多线程的部分，写成一个类，然后调用就完了
"""

# join() 的使用 ： https://www.cnblogs.com/cnkai/p/7504980.html


class MyThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.counter = counter

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print("Starting " + '-' * 30 + self.name)
        print_time(self.name, self.counter, 5)
        print("Exiting " + '-' * 30 + self.name)


class MyThreadNew(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.counter = counter

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print("Starting : 2 " + '*' * 30 + self.name)
        print_time(self.name, self.counter, 5)
        print("Exiting : 2 " + '*' * 30 + self.name)


def print_time(thread_name, delay, counter):
    while counter:
        time.sleep(delay)
        print("%s: %s" % (thread_name, time.ctime(time.time())))
        counter -= 1


# 创建新线程
thread1 = MyThreadNew(1, "Thread-1", 1)
thread2 = MyThread(2, "Thread-2", 2)

# 开启线程
thread1.start()
thread2.start()

# 若果没有这两个 join 主线程会一直运行， 等待至线程中止
thread1.join()  # 线程 1 结束后执行主线程
thread2.join()  # 线程 2 借宿后执行主线程

print("这边执行新的操作")


