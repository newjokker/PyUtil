# -*- coding: utf-8  -*-
# -*- author: jokker -*-


# 只过了83.33% 。。。。。。。
# 思路： 深搜+剪枝


import sys
import numpy as np


def is_ok(sd_mat, index_i, index_y, num):
    """当前指定的数字是否合适"""
    for row in range(0, 9):
        if sd_mat[row][index_y] == num:
            return False
    for col in range(0, 9):
        if sd_mat[index_i][col] == num:
            return False
    ii = index_i / 3
    jj = index_y / 3
    for row in range(ii * 3, ii * 3 + 3):
        for col in range(jj * 3, jj * 3 + 3):
            if sd_mat[row][col] == num:
                return False
    return True


def dfs(sd_mat, index_i, index_j):
    if index_i == 9:
        return sd_mat
    if index_j == 9:
        return dfs(sd_mat, index_i + 1, 0)
    flag = False
    for col in range(index_j, 9):
        if sd_mat[index_i][col] == 0:
            flag = True
            isChange = False
            for num in range(1, 10):
                if is_ok(sd_mat, index_i, col, num):
                    isChange = True
                    sd_mat[index_i][col] = num
                    tpp = dfs(sd_mat, index_i, col + 1)
                    if tpp is None:
                        isChange = False
                        sd_mat[index_i][col] = 0
                        continue
                    else:
                        return tpp
            if not isChange:
                return None
    if not flag:
        return dfs(sd_mat, index_i + 1, 0)


if __name__ == '__main__':

    # while True:
    #     isCon = True
    #     mat = []
    #     for i in range(9):
    #         tp = sys.stdin.readline().strip()
    #         if not tp:
    #             isCon = False
    #             break
    #         tp = [int(i) for i in tp.split(' ')]
    #         mat.append(tp)
    #
    #     if not isCon:
    #         break

        m = [
            [6, 0, 0, 1, 0, 0, 7, 0, 8],
            [0, 0, 0, 8, 0, 0, 2, 0, 0],
            [2, 3, 8, 0, 5, 0, 1, 0, 0],
            [0, 0, 0, 0, 4, 0, 0, 9, 2],
            [0, 0, 4, 0, 0, 8, 6, 0, 0],
            [3, 7, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 3, 0, 0, 0, 5, 2, 6],
            [0, 0, 2, 0, 0, 4, 0, 0, 0],
            [9, 0, 7, 0, 0, 6, 0, 0, 0]
        ]

        mat = dfs(np.array(m, dtype=np.int), 0, 0)
        for i in mat:
            print(' '.join(str(j) for j in i))
