# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import numpy as np
import copy
import random


class GetPlaque(object):
    """广度遍历得到斑块"""

    @staticmethod
    def __neb_8(point):
        """ 8 邻接"""
        x, y = point[0], point[1]
        return [(x - 1, y - 1), (x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1), (x + 1, y + 1), (x + 1, y - 1),
                (x - 1, y + 1)]

    @staticmethod
    def __neb_4(point):
        """ 4 邻接"""
        x, y = point[0], point[1]
        return [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]

    @staticmethod
    def __get_method(neb_num):
        """返回对应的方法"""
        if neb_num == 8:
            return GetPlaque.__neb_8
        elif neb_num == 4:
            return GetPlaque.__neb_4
        else:
            raise TypeError('neb_num can only be 4 or 8')

    @staticmethod
    def get_plaque(point_mat, neb_num=8):
        """合并相邻点得到斑块，0为背景，1为斑块"""

        # todo 使用深度遍历或者广度遍历进行重写

        # 获取邻居的模式
        neb_method = GetPlaque.__get_method(neb_num)
        # 获得需要合并的点
        points = set(map(lambda x: tuple(x), np.argwhere(point_mat == 1)))
        # 所有斑块
        all_ban = []
        while points:
            # --------------- ☆ ----------------
            # 种子点
            seed = points.pop()
            ban = [seed]
            new_seed_list = [seed]  # 难点是要想到有 new_seed_list 这个结构，并每次清空
            # -----------------------------------
            # 当还存在种子点
            while new_seed_list:
                seed_to_find = copy.deepcopy(new_seed_list)  # 广度遍历新的种子点
                new_seed_list = []  # 清空，重新获取新种子点
                for each_seed in seed_to_find:
                    for each_point in neb_method(each_seed):
                        if each_point in points:
                            ban.append(each_point)
                            points.remove(each_point)
                            new_seed_list.append(each_point)
            # 新增一个斑块
            all_ban.append(ban)

        return all_ban

    @staticmethod
    def get_point_dict(point_mat, neb_num=8):
        """获得点坐标和斑块之间的一一对应的关系"""
        point_dict = {}
        plaques = GetPlaque.get_plaque(point_mat, neb_num)

        for plaque_index, each_plaque in enumerate(plaques):
            for each_point in each_plaque:
                point_dict[each_point] = plaque_index

        return point_dict


if __name__ == '__main__':

    test_dect = np.zeros((10000, 10000), np.bool)

    for i in range(1000):
        test_dect[random.randint(0, 45), random.randint(0, 45)] = 1

    for each in GetPlaque.get_plaque(test_dect, 4):
        print(each)

    # a = GetPlaque.get_point_dict(test_dect, neb_num=4)

    print('ok')
