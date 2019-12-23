# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import pygame


# 读取图像得到 surface 对象
qz = pygame.image.load(r'./AuxData/qz.jpg')
# 图像旋转


# 设置帧率
clock = pygame.time.Clock()
clock.tick(60)

# 更新画面 FIXME 不知道下面两个的区别
pygame.display.update()
pygame.display.flip()

# 文字
# pygame 不能在 surface 上面直接写文字，可以使用 render 方法将文字渲染成 surface 对象
# 需要和 init 函数配合使用
pygame.init()
screen = pygame.display.set_mode((200, 200))
font = pygame.font.Font(None, 20)
screen(font.render(str('jokker'), True, (0,255,0)), (100, 100))  # 渲染

# ------------------------------------------------------------------------------
# 提高图像的颜值
# pygame.display.set_mode(size=00, flags=0, depth=0, display=0)
# 全屏 : flag = True , 将 size 设置为当前屏幕的分辨率， pygame.display.list_modes()  # 返回当前显示器支持的分辨率, 在我的电脑上弄不了，不知道为什么
# 窗口可变：flags = RESIZABLE

# ------------------------------------------------------------------------------
# 图像变换
# pygame 的 transform 模块 对 surface 进行变换，返回变换后的 surface 对象
# pygame.transform
# （1）flip ：上下左右翻转图像
# （2）scale : 缩放图像（快速）
# （3）roate ：旋转图像
# （4）rotozoom : 缩放并旋转图像
# （5）scale2x : 快速放大一倍
# （6）smoothscale : 平滑缩放图像（精准）
# （7）chop ：裁剪图像
# ------------------------------------------------------------------------------
# 变透明

# ------------------------------------------------------------------------------
# 动画精灵

























