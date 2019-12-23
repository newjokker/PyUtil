# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
我能每次变出一个能出现在棋盘任何位置的的分身，它是我的目标，我有我和我的分身将它团团围住，
不留一个缝隙我才能胜利，我的分身是有限的，分身用完了，它还没抓住，它就胜利了
"""

import numpy as np
import logging


class SurroundIt(object):
    """抓住它，使用最少的点包围一个点，可以是单人双人游戏，一人控制被围住的点，一人控制落点"""

    def __init__(self, line_num: int = 21, column_num: int = 21, my_clone_num=20):
        if line_num < 10 or column_num < 10:
            raise ValueError('line num and column num should bigger then 10')

        self.__line_num = int(line_num / 2) * 2 + 1
        self.__column_num = int(column_num / 2) * 2 + 1
        self.__it_loc = (0, 0)  # it
        self.__my_loc = None  # 我现在的的位置
        self.__my_cloned_locs = set()  # 我分身的位置集合
        self.__my_clone_num = my_clone_num  # 分身的个数
        self.restoration()

    def get_neighbors(self, assign_point):
        """获取指定点的邻居"""
        x_loc, y_loc = assign_point
        neighbors_set = set()
        if x_loc == 0:
            neighbors_set.add((x_loc + 1, y_loc))
        elif x_loc == self.__line_num - 1:
            neighbors_set.add((x_loc - 1, y_loc))
        else:
            neighbors_set.add((x_loc - 1, y_loc))
            neighbors_set.add((x_loc + 1, y_loc))

        if y_loc == 0:
            neighbors_set.add((x_loc, y_loc + 1))
        elif y_loc == self.__column_num - 1:
            neighbors_set.add((x_loc, y_loc - 1))
        else:
            neighbors_set.add((x_loc, y_loc - 1))
            neighbors_set.add((x_loc, y_loc + 1))
        return neighbors_set

    def restoration(self):
        """复位"""
        self.__it_loc = (int(self.__line_num / 2), int(self.__column_num / 2))  # it 的位置在棋盘正中央
        self.__my_loc = None  # 我的位置在第一个
        self.__my_cloned_locs = set()

    def refresh(self, mode='dict'):
        """刷新"""
        if mode == 'dict':
            return {'it': self.__it_loc, 'my_clone': self.__my_cloned_locs, 'my': self.__my_loc}
        else:
            mat_new = np.zeros((self.__line_num, self.__column_num), dtype=np.uint8)
            for each_point in self.__my_cloned_locs:
                mat_new[each_point[0], each_point[1]] = 1  # 分身
            mat_new[self.__it_loc[0], self.__it_loc[1]] = 2  # it

            if self.__my_loc:
                mat_new[self.__my_loc[0], self.__my_loc[1]] = 3  # my

    def is_it_be_trapped(self):
        """是不是被困住了"""
        neighbors = self.get_neighbors(self.__it_loc)  # 获取 it 四周的落点
        if neighbors.issubset(self.__my_cloned_locs):  # 判断这四周的落点是不是全部在我的落点上，是的话返回 True
            return True
        else:
            return False

    def is_my_clone_use_up(self):
        """分身是否用完了"""
        if self.__my_clone_num > 0:
            return False
        else:
            return True

    def move_it(self, move_x: int, move_y: int):
        """ it 走一步棋"""
        loc_x, loc_y = self.__it_loc

        if (move_x in [-1, 0, 1]) and (move_y in [-1, 0, 1]):  # it 每次只能走一步
            loc_x += move_x
            loc_y += move_y
        else:
            logging.error('move_it, move_x and move_y not in [-1, 0, 1]')
            return False

        if (loc_x, loc_y) in self.__my_cloned_locs:  # it 不能落子在我的分身上
            logging.error(u'已经有棋子，不能下在这边')
            return False

        if not ((0 <= loc_y <= self.__line_num - 1) and (0 <= loc_x <= self.__column_num - 1)):  # it 位置是否在棋盘外
            logging.error(u"it 越界了")
            return False

        if (move_x in [-1, 1]) and (move_y in [-1, 1]):  # 如果是斜过来走，要看看是不是拌着腿
            if {(self.__it_loc[0] + move_x, self.__it_loc[1]), (self.__it_loc[0], self.__it_loc[1] + move_y)} \
                    .issubset(self.__my_cloned_locs):
                logging.error("it 被分身绊住了")
                return False

        self.__it_loc = (loc_x, loc_y)
        return True

    def add_one_clone(self, loc_x, loc_y):
        """我走一步棋"""
        if not (0 <= loc_y <= self.__line_num - 1 and 0 <= loc_x <= self.__column_num - 1):  # 是否越界
            logging.error(u"分身越界了")
            return False

        if {(loc_x, loc_y)}.issubset(self.__my_cloned_locs.union({self.__it_loc})):  # 此处是否已有落子
            logging.error(u"不能在同一个地方重复下子")
            return False

        self.__my_cloned_locs.add((loc_x, loc_y))  # 增加分身
        self.__my_loc = (loc_x, loc_y)
        self.__my_clone_num -= 1  # 分身减 1
        return True


if __name__ == '__main__':

    a = SurroundIt()

    a.get_neighbors((0, 10))
