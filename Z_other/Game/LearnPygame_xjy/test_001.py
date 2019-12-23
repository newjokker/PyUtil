# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import pygame
import sys

# pygame 的功能

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((800, 800))  # 创建指定大小的窗口

pygame.display.set_caption('jokker_test')  # 设置标题

back_ground = pygame.image.load(r'./aux_data/test.jpg')  # 加载图片
position = back_ground.get_rect()  # 获取图像的位置矩形 FIXME 使用 position 结构会好很多

pygame.draw.rect(screen, (0, 0, 0), (0, 0, 50, 50), 0)

while True:
    for event in pygame.event.get():

        print(event.type)

        if event.type == pygame.QUIT:
            sys.exit()

        # F11 设置为全屏

    position.left += 1
    position.top += 1

    screen.fill((255, 255, 255))
    screen.blit(back_ground, position)  # 一个图像画到另外一个图像上去
    pygame.display.flip()  # 更新界面

    clock.tick(30)  # 设置帧率
