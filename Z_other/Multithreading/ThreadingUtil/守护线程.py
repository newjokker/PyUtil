# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import threading
from threading import Thread
import time


"""
* 选用守护线程实现报时功能，每隔多少秒提醒一下
* 守护线程无法 join 在主线程执行完毕后会被销毁
"""


def daemon():
    while True:
        print(time.strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(5)


def print_new(n):
    for i in range(n):
        print(i)
        time.sleep(1)


t1 = Thread(target=print_new, args=(20, ))
t2 = Thread(target=daemon, daemon=True)  # 守护线程的关键点在于 设置 daemon 属性

t1.start()
t2.start()
t1.join()


print('end')

