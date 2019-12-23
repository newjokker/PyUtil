# -*- coding: utf-8  -*-
# -*- author: jokker -*-


def convertToTitle(n):
    """
    :type n: int
    :rtype: str
    """

    """从最后一位开始计算，
    每次都除以一个进制的数，除以第几次其实就是获取反过来第几位的信息了"""

    res = ''  # 结果
    while n:  # 当商大于0时
        n -= 1  # 要先减1才能找到对应的数字
        r, n = n % 26, n // 26  # 获取当前的商和余数
        print(r, n)
        res = chr(65 + r) + res  # 寻找当前位对应的字符，加入到结果的最高位
    return res


if __name__ == "__main__":

    print(convertToTitle(715))




