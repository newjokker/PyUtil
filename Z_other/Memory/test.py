# -*- coding: utf-8  -*-
# -*- author: jokker -*-
import psutil
import os,datetime,time
from guppy import hpy
import sys

@profile
def my_func():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a

if __name__ == '__main__':
    my_func()