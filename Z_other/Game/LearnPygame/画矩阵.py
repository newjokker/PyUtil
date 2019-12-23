# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import pygame
import sys
from pygame.locals import *


def run():

    pygame.init()

    clock = pygame.time.Clock()  # 定时器
    screen = pygame.display.set_mode((500, 500))

    x, y = (0, 0)
    heigt, width = (10, 10)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 当按下关闭按键
                pygame.quit()
                sys.exit()  # 接收到退出事件后退出程序
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                x += 5
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                x -= 5
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                y -= 5
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                y += 5

        screen.fill((0, 0, 0))  # 屏幕中填充颜色

        pygame.draw.rect(screen, (255, 255, 255), (x, y, heigt, width))  # 画一个矩阵
        pygame.draw.line(screen, (125, 125, 125), (10, 10), (65, 85), 2)  # 画一条线

        pygame.draw.circle(screen, (120, 12, 0), (25, 25), 35, 2)

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':

    run()
