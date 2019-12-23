# -*- coding: utf-8  -*-
# -*- author: jokker -*-

# 参考：https://blog.csdn.net/zr7116/article/details/90911876

import numpy as np


class Broadcast(object):

    @staticmethod
    def test_001():
        """两个一维扩展为二维"""
        a = np.array(list(range(10)))
        b = np.array([[1]]*10)
        c = a*b
        print(a)
        print('-' * 100)
        print(b)
        print('-' * 100)
        print(c)


if __name__ == "__main__":

    Broadcast.test_001()


