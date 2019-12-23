# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
* 设置 递归的深度 sys.setrecursionlimit(1500)
* 传出递归后的结果会比较困难，除了使用全局不良，不知道还有什么其他办法
* 记住递归的形式就行，使用递归的时候看看能不能使用动态规划对数据过程进行简化
"""



from Report.DecoratorUtil import DecoratorUtil
import sys
sys.setrecursionlimit(1500)  # fixme 修改递归调用深度



# fixme 递归中数据的输出


def recur_fibo(n):
    """递归函数, 输出斐波那契数列"""
    if n <= 1:
        return n
    else:
        return recur_fibo(n - 1) + recur_fibo(n - 2)


print(recur_fibo(39))
