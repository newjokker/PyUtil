# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""超时退出

目前的思路，开两个线程/进程，一个专门监测时间和是否需要退出，一个就是正常的任务

"""

import time
import eventlet #导入eventlet这个模块
eventlet.monkey_patch() #必须加这条代码


def ok():
   for i in range(100):
      print(i)
      time.sleep(1)


with eventlet.Timeout(4, False):   #设置超时时间为2秒
   # time.sleep(4)
   ok()
   print('没有跳过这条输出')


print('跳过了输出')






