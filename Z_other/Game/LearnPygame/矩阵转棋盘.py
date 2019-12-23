# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import pygame
import sys
import random
import numpy as np

def run():
    clock = pygame.time.Clock()  # 定时器
    screen = pygame.display.set_mode([600, 600])

    x, y = (0, 0)
    heigt, width = (15, 15)

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

        # 将矩阵转为砖块列表，对砖块列表进行可视化
        mat = np.zeros((40, 40))
        mat[12, 12] = 1
        mat[1, 1] = 1

        # 可视化矩阵中的各个元素
        bricks = []
        for each_point in np.argwhere(mat == 0).tolist():
            x, y = each_point
            color = (255, 255, 255)
            brick_temp = {'loc': (x*15, y*15), 'height': heigt, 'width': width, 'color': color}
            bricks.append(brick_temp)

        # 可视化矩阵中的各个元素
        for each_point in np.argwhere(mat == 1).tolist():
            x, y = each_point
            color = (255, 0, 255)
            brick_temp = {'loc': (x*15, y*15), 'height': heigt, 'width': width, 'color': color}
            bricks.append(brick_temp)

        # 将砖块全部可视化出来
        for each_brick in bricks:
            x, y = each_brick['loc']
            height, width = each_brick['height'], each_brick['width']
            color = each_brick['color']
            pygame.draw.rect(screen, color, (x, y, heigt, width))  # 画一个矩阵

        # 画出要看的线
        for i in range(40):
            pygame.draw.line(screen, (125, 125, 125), (0, i*15), (600, i*15), 1)
            pygame.draw.line(screen, (125, 125, 125), (i*15, 0), (i*15, 600), 1)

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':

    """输入矩阵，根据屏幕的大小，返回对应的砖块和对应的线"""



    run()
