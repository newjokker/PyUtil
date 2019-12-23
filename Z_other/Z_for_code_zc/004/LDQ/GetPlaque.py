# -*- coding: utf-8  -*-
# -*- author: jokker -*-


from collections import deque
import numpy as np
import random
import matplotlib.pylab as plt


class GetPlaque(object):
    """广度遍历得到斑块"""

    @staticmethod
    def __get_neb(point, neb_num=8):
        """ 4 邻接"""
        x, y = point[0], point[1]
        if neb_num == 8:
            return [(x - 1, y - 1), (x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1), (x + 1, y + 1), (x + 1, y - 1),
                    (x - 1, y + 1)]
        elif neb_num == 4:
            return [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
        else:
            raise ValueError('neb_num can only be int 4 or 8')

    @staticmethod
    def get_plaque_index_data(point_mat, ban_all):
        """获取斑块的 index 矩阵，每一个斑块获取一个唯一的 index"""
        res = np.zeros_like(point_mat, dtype=np.int)
        for plaque_index, each_plqque in enumerate(ban_all):
            for each_point in each_plqque:
                res[each_point[0], each_point[1]] = plaque_index + 1
        return res

    @staticmethod
    def get_plaque(point_mat, neb_num=8, re_mode='MAT'):
        """获取斑块"""
        # 获得需要合并的点
        points_not_merge = set(map(lambda x: tuple(x), np.argwhere(point_mat == 1)))
        ban_all = []
        while points_not_merge:
            assign_seed = points_not_merge.pop()
            deque_temp = deque([assign_seed])
            ban_temp = [assign_seed]
            while deque_temp:
                point_temp = deque_temp.pop()
                point_neb = GetPlaque.__get_neb(point_temp, neb_num)
                for each_neb in point_neb:
                    if each_neb in points_not_merge:
                        ban_temp.append(each_neb)
                        points_not_merge.remove(each_neb)
                        deque_temp.append(each_neb)
            # 存储一个斑块
            ban_all.append(ban_temp)

        # 返回规范后的矩阵
        if re_mode == 'MAT':
            return GetPlaque.get_plaque_index_data(point_mat, ban_all)
        else:
            return ban_all


if __name__ == "__main__":

    a_length = 35
    test_dect = np.zeros((a_length, a_length), np.bool)

    # 添加随机点
    for i in range(150):
        test_dect[random.randint(0, a_length-1), random.randint(0, a_length-1)] = 1

    # a = GetPlaque.get_plaque(test_dect, neb_num=8, re_mode='000')
    # print(len(a))

    # 结果可视化
    GetPlaque.get_plaque(test_dect, neb_num=8)
    # plt.matshow(GetPlaque.get_plaque(test_dect, neb_num=8), cmap='CMRmap_r')
    # plt.show()



