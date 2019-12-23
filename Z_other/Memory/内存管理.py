# -*- coding: utf-8  -*-
# -*- author: jokker -*-

#先下载psutil库:pip install psutil
import psutil
import os,datetime,time
from guppy import hpy
import sys

def getMemCpu():
    """得到 内存 和 CPU 的使用情况"""
    data = psutil.virtual_memory()
    total = data.total #总内存,单位为byte
    free = data.available #可以内存
    memory = "Memory usage:%d"%(int(round(data.percent)))+"%"+" "
    cpu = "CPU:%0.2f"%psutil.cpu_percent(interval=1)+"%"
    # print('total : {0}, free : {1}'.format(total/(1024*1024), free/(1024*1024)))
    return memory + cpu

def main():
    while True:
        info = getMemCpu()
        time.sleep(0.1)
        print(info)

if __name__=="__main__":

    # my_func()
    # main()

    from guppy import hpy

    hxx = hpy()
    heap = hxx.heap()
    byrcs = hxx.heap().byrcs

    print(heap)
    print('-'*100)
    print(hxx)
    print('-'*100)
    print(byrcs)




