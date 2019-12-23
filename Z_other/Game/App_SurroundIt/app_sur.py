# -*- coding: utf-8  -*-
# -*- author: jokker -*-

# FIXME 以这个游戏为突破口，将逻辑完善到不能再去完善
# FIXME 旁边有区域显示需要的信息
# FIXME 忽略边框的区域
# TODO 棋子可以改为贴图

import sys
import pygame
import logging
# from pygame.locals import *
from Z_other.Game import SurroundIt


class AppSurroundIt(object):

    def __init__(self, mat_shape, width, height, my_clone_num=20):
        pygame.init()
        self.is_my_turn = False
        self.b_height = height
        self.b_width = width
        self.b_line_num, self.b_col_num = mat_shape  # show how many bricks in line and column
        self.bricks = []
        self.color_map = {}
        self.screen = pygame.display.set_mode((self.b_line_num * self.b_height, self.b_col_num * self.b_width))
        self.clock = pygame.time.Clock()
        self.grid_line_color = (0, 0, 0)
        self.background_color = (230, 230, 130)
        self.my_clone_num = my_clone_num

    def draw_vector(self):
        self.screen.fill(self.background_color)
        self.draw_grid()
        self.draw_bricks()

        font_0 = pygame.font.Font(None, 250)
        self.screen.blit(font_0.render(str('it lose'), True, (0, 0, 0)), (200, 200))

    def draw_lose(self):
        self.screen.fill(self.background_color)
        self.draw_grid()
        self.draw_bricks()

        font_0 = pygame.font.Font(None, 250)
        self.screen.blit(font_0.render(str('my lose'), True, (0, 0, 0)), (200, 200))

    def draw_normal(self):
        self.screen.fill(self.background_color)
        self.draw_grid()
        self.draw_bricks()

        # show whose turn now
        font_0 = pygame.font.Font(None, 30)
        if self.is_my_turn:
            self.screen.blit(font_0.render(str('my turn'), True, (0, 0, 0)),
                             (int((self.b_col_num * self.b_width) / 2), 10))
        else:
            self.screen.blit(font_0.render(str('it turn'), True, (0, 0, 0)),
                             (int((self.b_col_num * self.b_width) / 2), 10))

    def draw_bricks(self):
        for each_brick in self.bricks:
            x, y = each_brick['loc']
            color_temp = each_brick['color']
            r = int(self.b_height / 2) - 1
            pygame.draw.circle(self.screen, color_temp, (x, y), r)

    def draw_grid(self):
        # line
        for i in range(1, self.b_line_num):
            pygame.draw.line(self.screen, self.grid_line_color, (self.b_width, i * self.b_height),
                             (self.b_width * (self.b_line_num - 1), i * self.b_height), 1)
        # column
        for i in range(1, self.b_col_num):
            pygame.draw.line(self.screen, self.grid_line_color, (i * self.b_width, self.b_height),
                             (i * self.b_width, self.b_height * (self.b_col_num - 1)), 1)

        # border
        pygame.draw.line(self.screen, self.grid_line_color, (self.b_width, self.b_height),
                         (self.b_width, self.b_height * (self.b_col_num - 1)), 3)

        pygame.draw.line(self.screen, self.grid_line_color, ((self.b_col_num - 1) * self.b_width, self.b_height),
                         ((self.b_col_num - 1) * self.b_width, self.b_height * (self.b_col_num - 1)), 3)

        pygame.draw.line(self.screen, self.grid_line_color, (self.b_width, self.b_height),
                         (self.b_width * (self.b_line_num - 1), self.b_height), 3)

        pygame.draw.line(self.screen, self.grid_line_color, (self.b_width, (self.b_line_num - 1) * self.b_height),
                         (self.b_width * (self.b_line_num - 1), (self.b_line_num - 1) * self.b_height), 3)

        # four point
        pygame.draw.circle(self.screen, self.grid_line_color, (self.b_width * 4, self.b_height * 4), 4)
        pygame.draw.circle(self.screen, self.grid_line_color, (self.b_width * (self.b_col_num - 4),
                                                               self.b_height * 4), 4)
        pygame.draw.circle(self.screen, self.grid_line_color, (self.b_width * 4,
                                                               self.b_height * (self.b_line_num - 4)), 4)
        pygame.draw.circle(self.screen, self.grid_line_color, (self.b_width * (self.b_col_num - 4),
                                                               self.b_height * (self.b_line_num - 4)), 4)

    def get_brick_from_brick_info(self, brick_info):
        brick_it = brick_info['it']
        brick_my = brick_info['my']
        brick_clone = brick_info['my_clone']

        # draw my clone
        for each_brick in brick_clone:
            self.bricks.append(
                {'loc': (each_brick[0] * self.b_width, each_brick[1] * self.b_height), 'color': self.color_map[3]})

        # draw it
        self.bricks.append(
            {'loc': (brick_it[0] * self.b_width, brick_it[1] * self.b_height), 'color': self.color_map[1]})

        # draw my
        if brick_my is not None:
            self.bricks.append(
                {'loc': (brick_my[0] * self.b_width, brick_my[1] * self.b_height), 'color': self.color_map[2]})

    def run(self):
        pygame.display.set_caption('Surround It')
        surround_it = SurroundIt(line_num=self.b_line_num, column_num=self.b_col_num,
                                 my_clone_num=self.my_clone_num)

        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if not self.is_my_turn:
                        if event.key == pygame.K_d:
                            move_vector = (1, 0)
                        elif event.key == pygame.K_a:
                            move_vector = (-1, 0)
                        elif event.key == pygame.K_w:
                            move_vector = (0, -1)
                        elif event.key == pygame.K_s:
                            move_vector = (0, 1)
                        elif event.key == pygame.K_q:
                            move_vector = (-1, -1)
                        elif event.key == pygame.K_e:
                            move_vector = (1, -1)
                        elif event.key == pygame.K_z:
                            move_vector = (-1, 1)
                        elif event.key == pygame.K_x:
                            move_vector = (1, 1)
                        else:
                            logging.error("only support : w，a，d，s，q，e，z，x")
                            continue

                        if surround_it.move_it(move_vector[0], move_vector[1]):
                            self.is_my_turn = True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.is_my_turn:
                        if event.button == pygame.BUTTON_LEFT:
                            x, y = pygame.mouse.get_pos()
                            r = int(self.b_width / 2)
                            if surround_it.add_one_clone(int((x + r) / self.b_width), int((y + r) / self.b_height)):
                                self.is_my_turn = False

            # get brick_info from surround_it instance
            brick_info = surround_it.refresh()
            self.get_brick_from_brick_info(brick_info)

            # draw feature by if it have be trapped
            if surround_it.is_it_be_trapped():
                self.draw_vector()
            elif surround_it.is_my_clone_use_up():
                self.draw_lose()
            else:
                self.draw_normal()

            # refresh
            pygame.display.update()
            self.bricks = []
            self.clock.tick(60)


if __name__ == "__main__":
    a = AppSurroundIt((22, 22), 40, 40, 15)
    # a = AppSurroundIt((40, 40), 20, 20, 15)
    a.color_map = {1: (255, 255, 255), 3: (0, 0, 0), 2: (125, 125, 125)}
    a.run()
