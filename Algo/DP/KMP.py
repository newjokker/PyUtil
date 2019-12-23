# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import numpy as np


def find_max_substring(str_a, str_b):
    """寻找最长相同子串"""
    f_array = np.zeros((len(str_a), len(str_b)))
    for i in range(1, len(str_a)):
        for j in range(1, len(str_b)):
            if str_a[i] == str_b[j]:
                f_array[i, j] += (1 + f_array[i-1, j-1])

    x, y = np.argwhere(f_array == np.max(f_array))[0].tolist()  # 找到结束的字符的位置
    return str_a[x - int(np.max(f_array)) + 1: x+1]


# KMP 算法来解决

A = "afghjhgfdsdfghgfdsdfgaaassaasjhgfdsasdfgfdsakjhgfdsfgmn"
B = "fdfghjkjhgfdfghjkjhgfdsgfdsdfgaaassaasghjklkhgfdsfgjkjhgfdsdhj"


def KMP_algorithm(string, substring):
    """KMP字符串匹配的主函数, 若存在字串返回字串在字符串中开始的位置下标，或者返回-1"""
    pnext = gen_pnext(substring)
    n = len(string)
    m = len(substring)
    i, j = 0, 0
    while (i < n) and (j < m):
        if string[i] == substring[j]:
            i += 1
            j += 1
        elif j != 0:
            j = pnext[j - 1]
        else:
            i += 1
    if j == m:
        return i - j
    else:
        return -1

def gen_pnext(substring):
    """构造临时数组pnext"""
    index, m = 0, len(substring)
    pnext = [0] * m
    i = 1
    while i < m:
        if substring[i] == substring[index]:
            pnext[i] = index + 1
            index += 1
            i += 1
        elif index != 0:
            index = pnext[index - 1]
        else:
            pnext[i] = 0
            i += 1
    return pnext


if __name__ == "__main__":
    string = 'abcxabcdabcdabcy'
    substring = 'abcdabcy'
    out = KMP_algorithm(string, substring)
    print(out)

#
#
# if __name__ == "__main__":
#
#     str_A = "afghjhgfdsdfghgfdsdfgaaassaasjhgfdsasdfgfdsakjhgfdsfgmn"
#     str_B = "fdfghjkjhgfdfghjkjhgfdsgfdsdfgaaassaasghjklkhgfdsfgjkjhgfdsdhj"
#
#     max_sub_str = find_max_substring(str_A, str_B)
#     print(max_sub_str)
