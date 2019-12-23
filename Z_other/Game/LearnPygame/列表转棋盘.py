# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import pygame
import sys
import random

def run():
    clock = pygame.time.Clock()  # 定时器
    screen = pygame.display.set_mode([320, 400])

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


        # 创建随机砖块
        bricks = []
        for i in range(100):
            x, y = random.randrange(1, 30), random.randrange(1, 40)
            color = (random.randrange(1, 255), random.randrange(1, 255), random.randrange(1, 255))
            brick_temp = {'loc': (x*10, y*10), 'height': 10, 'width': 10, 'color': color}
            bricks.append(brick_temp)

        # 将砖块全部可视化出来
        for each_brick in bricks:
            x, y = each_brick['loc']
            height, width = each_brick['height'], each_brick['width']
            color = each_brick['color']
            pygame.draw.rect(screen, color, (x, y, heigt, width))  # 画一个矩阵

        pygame.display.update()
        clock.tick(15)


if __name__ == '__main__':

    run()