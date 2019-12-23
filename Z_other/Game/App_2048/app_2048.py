# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import numpy as np


class App_2048(object):

    def __init__(self, line_num=4, column_num=4):
        # 当前的数字矩阵
        self.mat = None
        # 执行的步数
        self.step_num = 0
        # 矩阵的行列数
        self.line_num = line_num
        self.column_num = column_num
        # 初始化
        self.initialize_mat()

    @staticmethod
    def move_slice(slice_temp):
        """处理一个切片，方向是自上而下，n*1 的矩阵操作"""
        focus_index = slice_temp.shape[0] - 1
        index = focus_index -1
        while index >= 0:
            if slice_temp[focus_index] == slice_temp[index] and slice_temp[focus_index] != 0:
                slice_temp[focus_index] *= 2
                slice_temp[index]= 0
                index -= 2
                focus_index = index - 1
            elif slice_temp[focus_index] != 0 and slice_temp[index] != 0:
                index -= 1
                focus_index -= 1
            elif slice_temp[focus_index] != 0 and slice_temp[index] == 0:
                index -= 1
            elif slice_temp[focus_index] == 0 and slice_temp[index] != 0:
                focus_index = index
                index -= 1
            else:  # 都为 0
                index -= 2
                focus_index -= 1

        slice_not_0 = slice_temp[slice_temp != 0]  # 存在非零元素，将其移动到最下方
        if len(slice_not_0) > 0:
            num_not_0 = slice_not_0.shape[0]
            num_slice = slice_temp.shape[0]
            slice_temp.fill(0)
            slice_temp[num_slice - num_not_0:num_slice] = slice_not_0
        return slice_temp

    def initialize_mat(self):
        """初始化矩阵"""
        # 初始化矩阵
        self.mat = np.zeros((self.line_num, self.column_num), dtype=np.uint16)
        # 指定种子点
        seed_x, seed_y = np.random.randint(self.line_num), np.random.randint(self.column_num)
        self.mat[seed_x, seed_y] = np.random.choice([2, 4])
        print('-'*100)
        print(self.mat)

    def set_mat(self, assign_mat):
        """强制指定矩阵"""
        if assign_mat.shape == self.mat.shape:
            self.mat = assign_mat
            a.re_fresh()
        else:
            raise ValueError('assign mat shape error')

    def move_down(self):
        """往下滑动"""
        # 自左到右一列一列处理
        for index in range(self.column_num):
            # 获取切片，操作切片，替换切片
            slice_temp = self.mat[:, index].copy()
            self.mat[:, index] = App_2048.move_slice(slice_temp)

    def move_up(self):
        """往上滑动"""
        for index in range(self.column_num):
            slice_temp = np.flipud(self.mat[:, index]).copy()  # 对切片进行翻转
            self.mat[:, index] = np.flipud(App_2048.move_slice(slice_temp))

    def move_left(self):
        """往左滑动"""
        for index in range(self.column_num):
            slice_temp = np.flipud(self.mat[index, :]).copy()  # 对切片进行翻转
            self.mat[index, :] = np.flipud(App_2048.move_slice(slice_temp))

    def move_right(self):
        """往右滑动"""
        for index in range(self.column_num):
            # 获取切片，操作切片，替换切片
            slice_temp = self.mat[index, :].copy()
            self.mat[index, :] = App_2048.move_slice(slice_temp)

    def re_fresh(self):
        """刷新 mat 找一个为 0 的区域设置为 2 或者 4"""
        self.step_num += 1

        location_x_y = np.argwhere(self.mat == 0)
        empty_grid_num = len(location_x_y)  # 找到还剩几个空余的位置

        if empty_grid_num == 0:  # 没有空余的位置了，失败
            print('没有空位置了')
            return False

        index = np.random.randint(empty_grid_num)
        self.mat[location_x_y[index][0], location_x_y[index][1]] = np.random.choice([2, 4])  # 随机替换一个 2 或 4
        print('-'*100)
        print(u"step : {0}".format(self.step_num))
        print(self.mat)
        return True


if __name__ == '__main__':

    # FIXME 读取键盘事件

    a = App_2048(14, 14)

    # a.set_mat(np.array([[0, 0, 0, 4], [0, 0, 0, 0], [16, 0, 0, 0], [2, 4, 2, 0]]))

    while True:
        keybord_str = input(":")
        if keybord_str == 'w':
            a.move_up()
        elif keybord_str == 's':
            a.move_down()
        elif keybord_str == 'a':
            a.move_left()
        elif keybord_str == 'd':
            a.move_right()
        elif keybord_str == 'q':
            print("exit ")
            break
        else:
            continue

        if not a.re_fresh():
            break



