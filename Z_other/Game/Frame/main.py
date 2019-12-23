# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import pygame
import numpy as np
import sys
import random
from pygame.locals import *  # 导入所有的常量名


class Frame(object):
    """矩阵游戏框架"""

    def __init__(self, mat_shape:tuple, height, width):
        pygame.init()
        self.mat_shape = mat_shape  # 矩阵点的多少
        self.mat = np.zeros(self.mat_shape, dtype=np.int8)
        self.b_height = height  # 砖块的高
        self.b_width = width  # 砖块的宽
        self.color_map = {}  # 矩阵中的每一个值对应的一个颜色
        # self.screen = pygame.display.set_mode((self.mat_shape[0] * self.b_height, self.mat_shape[1] * self.b_width))  # 画板
        self.screen = pygame.display.set_mode((self.mat_shape[0] * self.b_height, self.mat_shape[1] * self.b_width))  # 画板
        self.clock = pygame.time.Clock()  # 定时器
        self.grid_line_color = (0, 0, 0)  # 格网线的颜色
        self.fill_color = (230, 230, 130)  # 背景填充色
        self.bricks = []  # 需要绘制的砖块
        self.focus_point_x = 0  # 当前的焦点
        self.focus_point_y = 0  # 当前的焦点
        self.status_bricks = []  # 基准砖块，这些砖块一般不变换的，

    def draw_grid(self):
        """画格网"""
        # 横线
        for i in range(1, self.mat_shape[0]):
            pygame.draw.line(self.screen, self.grid_line_color, (self.b_width, i * self.b_height),
                             (self.b_width * (self.mat_shape[0] - 1) , i * self.b_height), 1)
        # 纵线
        for i in range(1, self.mat_shape[1]):
            pygame.draw.line(self.screen, self.grid_line_color, (i * self.b_width, self.b_height),
                             (i * self.b_width, self.b_height * (self.mat_shape[1] - 1)), 1)

        # 边框线
        pygame.draw.line(self.screen, self.grid_line_color, (self.b_width, self.b_height),
                         (self.b_width, self.b_height * (self.mat_shape[1] - 1)), 3)

        pygame.draw.line(self.screen, self.grid_line_color, ((self.mat_shape[1]-1) * self.b_width, self.b_height),
                         ((self.mat_shape[1]-1) * self.b_width, self.b_height * (self.mat_shape[1] - 1)), 3)

        pygame.draw.line(self.screen, self.grid_line_color, (self.b_width, self.b_height),
                         (self.b_width * (self.mat_shape[0] - 1), self.b_height), 3)

        pygame.draw.line(self.screen, self.grid_line_color, (self.b_width, (self.mat_shape[0] - 1) * self.b_height),
                         (self.b_width * (self.mat_shape[0] - 1), (self.mat_shape[0] - 1) * self.b_height), 3)

        # 棋盘上的四个点
        # self.mat_shape[0] -4

        pygame.draw.circle(self.screen, self.grid_line_color, (self.b_width * 4, self.b_height * 4), 4)
        pygame.draw.circle(self.screen, self.grid_line_color, (self.b_width * (self.mat_shape[1] - 4),
                                                               self.b_height * 4), 4)
        pygame.draw.circle(self.screen, self.grid_line_color, (self.b_width * 4,
                                                               self.b_height * (self.mat_shape[0] - 4)), 4)
        pygame.draw.circle(self.screen, self.grid_line_color, (self.b_width * (self.mat_shape[1] - 4),
                                                               self.b_height * (self.mat_shape[0] - 4)), 4)

        # 画矩形棋子
        pygame.draw.circle(self.screen, (255, 255, 255), (self.b_width * 4, self.b_height * 4), 20)

        # 粘贴图片作为棋子
        qz = pygame.image.load(r'./AuxData/qz.jpg')
        qz2 = pygame.image.load(r'./AuxData/qz.jpg')

        position = qz.get_rect()
        position2 = qz2.get_rect()

        position.left = self.b_width * (self.mat_shape[1] - 4) - 25
        position.top = self.b_height * 4 - 25

        position2.left = self.b_height * 4 - 25
        position2.top = self.b_width * (self.mat_shape[1] - 4) - 25

        self.screen.blit(qz, position)
        self.screen.blit(qz2, position2)

        font_0 = pygame.font.Font(None, 50)
        self.screen.blit(font_0.render(str('jokker'), True, (0, 0, 0)), (100, 100))  # 渲染

    def get_brick_from_mat(self):
        """从矩阵中获取砖块"""
        for each_value in self.color_map:
            for each_point in np.argwhere(self.mat == each_value).tolist():
                x, y = each_point
                color = self.color_map[each_value]
                brick_temp = {'loc': (x * self.b_width, y * self.b_height), 'color': color}
                self.bricks.append(brick_temp)

    def get_one_brick(self, x, y, color):
        """增加一个砖块"""
        brick_temp = {'loc': (x * self.b_width, y * self.b_height), 'color': color}
        return brick_temp

    def draw_bricks(self):
        """绘制砖块"""
        # 将砖块全部可视化出来
        for each_brick in self.status_bricks + self.bricks:
            x, y = each_brick['loc']
            color = each_brick['color']
            pygame.draw.rect(self.screen, color, (x, y, self.b_height, self.b_width))  # 画一个矩阵

    def draw_all_feature(self):
        """画矩阵"""
        self.screen.fill(self.fill_color)  # 屏幕中填充颜色
        self.bricks = []  # 砖块清空
        self.get_brick_from_mat()  # 从矩阵中获取砖块
        self.draw_bricks()  # 绘制砖块
        self.draw_grid()  # 画网格线
        pygame.display.update()  # 更新画面
        self.clock.tick(60)  #

    def run(self):
        """执行"""
        self.color_map = {1:(255, 0, 0), 2:(0, 255, 255), 3:(0, 0, 255)}
        pygame.display.set_caption(u'五子棋')

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 当按下关闭按键
                    pygame.quit()
                    sys.exit()  # 接收到退出事件
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    self.mat.fill(0)
                    self.focus_point_x += 1
                    self.mat[self.focus_point_x, self.focus_point_y] = 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    self.mat.fill(0)
                    self.focus_point_x -= 1
                    self.mat[self.focus_point_x, self.focus_point_y] = 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    self.mat.fill(0)
                    self.focus_point_y -= 1
                    self.mat[self.focus_point_x, self.focus_point_y] = 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    self.mat.fill(0)
                    self.focus_point_y += 1
                    self.mat[self.focus_point_x, self.focus_point_y] = 1

                if event.type == pygame.KEYDOWN and event.key == 13:
                    one_brick = self.get_one_brick(self.focus_point_x, self.focus_point_y, self.color_map[2])
                    self.status_bricks.append(one_brick)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                    x, y = pygame.mouse.get_pos()
                    x = int(x / self.b_width)  # 鼠标所在方格位置
                    y = int(y / self.b_height)

                    one_brick = self.get_one_brick(x, y, self.color_map[3])
                    self.status_bricks.append(one_brick)

            self.draw_all_feature()


if __name__ == '__main__':

    a = Frame((16, 16), 35, 35)
    # a = Frame((26, 26), 30, 30)
    a.run()


