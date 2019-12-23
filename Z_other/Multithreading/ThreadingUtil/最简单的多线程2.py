# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import time
from threading import Thread


def print_time(n):
    for i in range(n):
        print('print time : {0}'.format(time.strftime('%Y%m%D %H-%M-%S')))
        time.sleep(1)

def print_time_2(n):
    for i in range(n):
        print('print time : {0}'.format(time.strftime('now')))
        time.sleep(2)


t1 = Thread(target=print_time, args=(10, ))
t2 = Thread(target=print_time_2, args=(10, ))

t1.start()
t2.start()

t1.join()
t2.join()


