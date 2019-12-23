# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from threading import Thread, Event
import time

"""
如果程序中有其他线程需要判断某个线程是否已经到达执行过程中的某个点，根据这个判断来执行后面的操作，那么这就产生了
非常棘手的线程同步问题，可以使用 threading 库中的 Event 对象来解决
"""


def countdown(n, srated_evt):
    print('countdown starting')
    time.sleep(2)
    srated_evt.set()  # 开始执行后面的操作

    for i in range(10):
        print(i)
        time.sleep(1)


start_env = Event()
t = Thread(target=countdown, args=(10, start_env))
t.start()
start_env.wait()

print('ending')
