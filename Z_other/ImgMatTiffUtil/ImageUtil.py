# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
图片相关的代码
"""

import numpy as np
import matplotlib.pyplot as plt
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import datetime
import math
# from Function.GdalUtil import GdalBase


class ImageUtil(object):

    @staticmethod
    def draw(image_mat_a, image_mat_b, loc=(0, 0)):
        """
        shape_b贴在shape_a上，只要指定一个左上角的位置即可,超出的部分可以自己增长，设置默认的无效值即可
        :param image_mat_a:
        :param image_mat_b:
        :param loc: (row_index, column_index);(高向下移动，宽向左移动)
        :return: image_mat
        """
        # 左上角坐标
        x, y = loc[0], loc[1]
        # 贴图
        row_num_b, col_num_b = image_mat_b.shape[:2]  # 获得被贴图片的长宽
        row_num_a, col_num_a = image_mat_a.shape[:2]  # 获得画布的长宽
        # 判断画布是否不够
        if x >= row_num_a or y >= col_num_a:
            raise TypeError('贴图位置超出画布范围')
        elif x + row_num_b > row_num_a or y + col_num_b > col_num_a:
            y_max = min(y + col_num_b, col_num_a)
            x_max = min(x + row_num_b, row_num_a)
            # TODO 得到重叠的影像
            image_mat_a[x:x_max, y:y_max, :] = image_mat_b[:x_max - x, :y_max - y, :]
        else:
            # TODO 得到重叠的影像
            image_mat_a[x:x + row_num_b, y:y + col_num_b, :] = image_mat_b

        # FIXME 这边考虑一下是不是要用深拷贝
        return image_mat_a

    @staticmethod
    def __get_com_color(image_mat_a, image_mat_b):
        """在有透明度的情况下，得到重叠的颜色"""
        #  参考 https://www.baidu.com/link?url=FwnJAkG_TZpC1YnFNsTDj6_oVADGfZBG4IMliNLstm1Itix33MbbnGZnSKk-vP4WLJa5Ef-UmXsPF-coHY1d-c1F-K5zB7pEB3VB8WQtaFS&wd=&eqid=e8c48848000477d8000000055d04b866

        # 画布是 image_mat_b

        # FIXME 里面矩阵运算部分可以简化，暂时没想到什么好的方法，矩阵乘法那一块不是很熟

        alpha_a = (image_mat_a[:, :, 3] / 255.0).astype(np.float16)
        alpha_b = (image_mat_b[:, :, 3] / 255.0).astype(np.float16)

        rgb_a = image_mat_a[:, :, :3].astype(np.float) / 255
        rgb_b = image_mat_b[:, :, :3].astype(np.float) / 255

        com_alpha = (((alpha_a + alpha_b) - alpha_a * alpha_b) * 255).astype(np.uint8)  # 混合后的透明度

        com_rgb_a_r = rgb_a[:, :, 0] * alpha_a * ((1 - alpha_b) / (alpha_a + alpha_b - alpha_a * alpha_b))  # a 贡献的
        com_rgb_b_r = rgb_b[:, :, 0] * (alpha_b / (alpha_a + alpha_b - alpha_a * alpha_b))  # a 贡献的

        com_rgb_a_g = rgb_a[:, :, 1] * alpha_a * ((1 - alpha_b) / (alpha_a + alpha_b - alpha_a * alpha_b))  # a 贡献的
        com_rgb_b_g = rgb_b[:, :, 1] * (alpha_b / (alpha_a + alpha_b - alpha_a * alpha_b))  # a 贡献的

        com_rgb_a_b = rgb_a[:, :, 2] * alpha_a * ((1 - alpha_b) / (alpha_a + alpha_b - alpha_a * alpha_b))  # a 贡献的
        com_rgb_b_b = rgb_b[:, :, 2] * (alpha_b / (alpha_a + alpha_b - alpha_a * alpha_b))  # a 贡献的

        image_mat = np.zeros((image_mat_a.shape[0], image_mat_a.shape[1], 4), dtype=np.uint8)
        image_mat[:, :, 0] = ((com_rgb_a_r + com_rgb_b_r) * 255).astype(np.uint8)
        image_mat[:, :, 1] = ((com_rgb_a_g + com_rgb_b_g) * 255).astype(np.uint8)
        image_mat[:, :, 2] = ((com_rgb_a_b + com_rgb_b_b) * 255).astype(np.uint8)
        image_mat[:, :, 3] = com_alpha

        return image_mat

    @staticmethod
    def draw_new(image_mat_a, image_mat_b, assign_loc=(0, 0), assign_angle=0):
        """
        shape_b贴在shape_a上，只要指定一个左上角的位置即可,超出的部分可以自己增长，设置默认的无效值即可
        :param image_mat_a:
        :param image_mat_b:
        :param assign_loc: (row_index, column_index);(高向下移动，宽向左移动)
        :param assign_angle: 指定相对位置的叫，0：被粘贴图到粘贴图左上角的相对距离，1:右上角，2：左下角，3：右下角
        :return: image_mat
        """

        # FIXME 支持两种模式，替换模式和粘贴模式，一种不需要计算透明度的叠加，一种需要计算透明度的叠加

        # 使用矩阵镜像，可以操作四个角
        if assign_angle in [0, '0']:
            # 左上角
            pass
        elif assign_angle in [1, '1']:
            # 右上角
            image_mat_a = np.fliplr(image_mat_a)
            image_mat_b = np.fliplr(image_mat_b)
        elif assign_angle in [2, '2']:
            # 左下角
            image_mat_a = np.flipud(image_mat_a)
            image_mat_b = np.flipud(image_mat_b)
        elif assign_angle in [3, '3']:
            # 右下角
            image_mat_a = np.fliplr(np.flipud(image_mat_a))
            image_mat_b = np.fliplr(np.flipud(image_mat_b))
        else:
            raise TypeError('assign angle can only in [0,1,2,3, "0","1","2","3"]')

        # 左上角坐标
        x, y = assign_loc[0], assign_loc[1]
        # 贴图
        row_num_b, col_num_b = image_mat_b.shape[:2]  # 获得被贴图片的长宽
        row_num_a, col_num_a = image_mat_a.shape[:2]  # 获得画布的长宽
        # 判断画布是否不够
        if x >= row_num_a or y >= col_num_a:
            raise TypeError('贴图位置超出画布范围')
        elif x + row_num_b > row_num_a or y + col_num_b > col_num_a:
            y_max = min(y + col_num_b, col_num_a)
            x_max = min(x + row_num_b, row_num_a)
            image_mat_a[x:x_max, y:y_max, :] = ImageUtil.__get_com_color(image_mat_a[x:x_max, y:y_max, :],
                                                                         image_mat_b[:x_max - x, :y_max - y, :])
        else:
            image_mat_a[x:x + row_num_b, y:y + col_num_b, :] = ImageUtil.__get_com_color(
                image_mat_a[x:x + row_num_b, y:y + col_num_b, :], image_mat_b)

        # 抵消之前的矩阵操作
        if assign_angle in [0, '0']:
            # 左上角
            pass
        elif assign_angle in [1, '1']:
            # 右上角
            image_mat_a = np.fliplr(image_mat_a)
        elif assign_angle in [2, '2']:
            # 左下角
            image_mat_a = np.flipud(image_mat_a)
        elif assign_angle in [3, '3']:
            # 右下角
            image_mat_a = np.fliplr(np.flipud(image_mat_a))

        # FIXME 这边考虑一下是不是要用深拷贝

        return image_mat_a

    @staticmethod
    def cat_together(image_mat_a, image_mat_b, direction=0):
        """
        将 b 添加到 a 的 dir 方向"
        :param image_mat_a:
        :param image_mat_b:
        :param direction: 0,1,2,3 ; 左，右，下，上
        :return:
        """
        # TODO 支持不变比例的添加，可以选在要素左对齐，右对齐，还有中间对齐

        # 长宽
        row_num, col_num = image_mat_b.shape[:2]
        # 对应 a 的长宽
        if direction in [0, 1, '0', '1']:
            # 左右
            assign_row_num = image_mat_a.shape[0]
            assign_col_num = int((float(col_num) / row_num) * assign_row_num)
        else:
            # 上下
            assign_col_num = image_mat_a.shape[1]
            assign_row_num = int((float(row_num) / col_num) * assign_col_num)

        # 指定长宽
        image_mat_b = ImageUtil.to_assign_shape(image_mat_b, (assign_col_num, assign_row_num))
        # 指定排序
        if direction in [0, '0']:
            new_image_mat = np.hstack((image_mat_b, image_mat_a))
        elif direction in [1, '1']:
            new_image_mat = np.hstack((image_mat_a, image_mat_b))
        elif direction in [2, '2']:
            new_image_mat = np.vstack((image_mat_a, image_mat_b))
        elif direction in [3, '3']:
            new_image_mat = np.vstack((image_mat_b, image_mat_a))
        else:
            raise TypeError('direction can only in [0, 1, 2, 3, "0", "1", "2", "3"]')
        return new_image_mat

    @staticmethod
    def image_to_image_mat(image_path):
        """
        图片转为图片矩阵
        :param image_path: 图片路径，str
        :return: image_mat
        """
        img = Image.open(image_path)
        image_mat = np.asarray(img, dtype='uint8')
        # 矩阵维度
        if image_mat.ndim == 2:
            alpha_mat = np.ones_like(image_mat) * 255
            # return np.array([image_mat.copy(), image_mat.copy(), image_mat.copy(), alpha_mat], dtype=np.uint8)
            image_mat = np.rollaxis(np.tile(image_mat, (4, 1, 1)), 0, 3)  # 单波段，转为多波段
            image_mat[:, :, 3] = alpha_mat
            return image_mat
        else:
            # 不存在 alpha 图层
            if image_mat.shape[2] == 3:
                alpha_mat = np.ones_like(image_mat[:, :, 1]) * 255
                image_mat = np.array(
                    [image_mat[:, :, 0].copy(), image_mat[:, :, 1].copy(), image_mat[:, :, 2].copy(), alpha_mat],
                    dtype=np.uint8)  # 变为 (4,x,y)
                image_mat = np.rollaxis(image_mat[[0, 1, 2, 3], :, :], 0, 3)  # 变为 (x,y,4)
                return image_mat
            elif image_mat.shape[2] == 4:
                return image_mat

    @staticmethod
    def create_shape_rect(row_num, col_num, fill_color=(255, 255, 255)):
        """新增矩形"""
        # 创建画布矩阵
        rect_shape = np.ones((row_num, col_num, 4), dtype=np.uint8) * 255
        # 设置颜色
        rect_shape[:, :, 0] = fill_color[0]
        rect_shape[:, :, 1] = fill_color[1]
        rect_shape[:, :, 2] = fill_color[2]
        # 设置透明图层
        if fill_color is None:
            rect_shape[:, :, 3] = 0
        else:
            rect_shape[:, :, 3] = 255
        return rect_shape

    @staticmethod
    def create_shape_circle(radius, fill_color=(255, 255, 255)):
        """画圆"""
        # FIXME 这个因为只有一个颜色，所以画出的圆很粗糙，重新使用 Image 自带的画图画圆

        # FIXME 根据距离的大小设置颜色（颜色的纯度）

        # 创建画布矩阵
        circle_shape = np.ones((radius * 2, radius * 2, 4), dtype=np.uint8) * 255
        # 得到计算需要的行列矩阵，排序矩阵的计算并变形？
        range_mat = np.array(range((radius * 2) ** 2)).reshape((radius * 2, radius * 2))
        row_mat = range_mat / (radius * 2)
        col_mat = range_mat % (radius * 2)
        # 计算得到圆掩膜（mask）
        mask = (row_mat - radius) ** 2 + (col_mat - radius) ** 2 < radius ** 2
        # 根据掩膜得到需要的shape, 加上底色
        circle_shape[mask, 0] = fill_color[0]
        circle_shape[mask, 1] = fill_color[1]
        circle_shape[mask, 2] = fill_color[2]
        circle_shape[~mask, 3] = 0  # 将圆以外的区域设置为透明
        return circle_shape

    @staticmethod
    def create_shape_ellipse(row_r, col_r, fill_color=(255, 255, 255), background_color=(255, 255, 255)):
        """画椭圆"""
        # 从矩阵创建
        if background_color is None:
            ellipse = Image.fromarray(ImageUtil.create_canvas(row_r, col_r))
        else:
            ellipse = Image.fromarray(ImageUtil.create_shape_rect(row_r, col_r, fill_color=background_color))
        draw = ImageDraw.Draw(ellipse)
        # 画椭圆
        draw.ellipse((0, 0, row_r, col_r), fill=fill_color)
        #
        return np.array(ellipse)

    @staticmethod
    def create_shape_polygon(point_list, fill_color=(100, 100, 100), background_color=(255, 255, 255)):
        """画多边形"""
        # 从矩阵创建
        x, y = zip(*point_list)
        if background_color is None:
            polygon = Image.fromarray(ImageUtil.create_canvas(max(y), max(x)))
        else:
            polygon = Image.fromarray(ImageUtil.create_shape_rect(max(y), max(x), fill_color=background_color))
        # 画图
        draw = ImageDraw.Draw(polygon)
        draw.polygon(point_list, fill=fill_color)
        return np.array(polygon)

    @staticmethod
    def create_canvas(row_num, col_num, fill_color=(255, 255, 255)):
        """新建画布, y,x"""
        # 新建一个矩形
        rect_shape = ImageUtil.create_shape_rect(row_num, col_num, fill_color=fill_color)
        # 将矩形范围透明度设置为 0
        rect_shape[:, :, 3] = 0
        return rect_shape

    @staticmethod
    def save_to_image(image_mat, save_path):
        """保存为图像"""
        img = Image.fromarray(image_mat)
        img.save(save_path)

    @staticmethod
    def get_rand_color(mode='RGB'):
        """得到随机的颜色"""
        if mode.upper() == 'RGB':
            return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        elif mode.upper() == 'GRAY':
            value_uint8 = random.randint(0, 255)
            return value_uint8, value_uint8, value_uint8

    @staticmethod
    def get_mask(image, reverse=False):
        """得到当前画布有值区域的掩膜，有取反选项，得到布尔矩阵"""
        # 拿到 alpha 图层
        alpha = image[:, :, 3]
        # 是否取反
        if reverse:
            return ~alpha
        else:
            return alpha

    @staticmethod
    def extend_to_range(image_mat, extend_range, fill_color=(255, 255, 255)):
        """
        扩展大小，正数是扩展，0是不变，不能有负数
        :param image_mat: 图像矩阵
        :param extend_range: 左，右，下，上
        :param fill_color: 填充色
        :return: image_mat
        """
        row_num, col_num = image_mat.shape[:2]
        image_mat_new = np.zeros(
            (row_num + extend_range[2] + extend_range[3], col_num + extend_range[0] + extend_range[1], 4),
            dtype=np.uint8)
        # 填充色
        if fill_color is None:
            image_mat_new[:, :, :] = 0
        else:
            image_mat_new[:, :, 0] = fill_color[0]
            image_mat_new[:, :, 1] = fill_color[1]
            image_mat_new[:, :, 2] = fill_color[2]
            image_mat_new[:, :, 3] = 255

        # 贴上原矩阵
        row_num, col_num = image_mat_new.shape[:2]
        image_mat_new[extend_range[3]:row_num - extend_range[2], extend_range[0]:col_num - extend_range[1],
        :] = image_mat
        return image_mat_new

    @staticmethod
    def extend_by_ratio(image_mat, extend_ratio, fill_color=(255, 255, 255)):
        """根据比例对要素进行扩展,左增加row_num的倍数，右，下增加col_num的倍数"""
        row_num, col_num = image_mat.shape[:2]
        # 上下左右增加的数目
        left_extend = int(col_num * extend_ratio[0])
        right_extend = int(col_num * extend_ratio[1])
        bottom_extend = int(row_num * extend_ratio[2])
        top_extend = int(row_num * extend_ratio[3])
        # 新的画布
        extend_rows = row_num + bottom_extend + top_extend  #
        extend_cols = col_num + left_extend + right_extend  #
        image_mat_new = np.zeros((extend_rows, extend_cols, 4), dtype=np.uint8)
        # 填充色
        if fill_color is None:
            image_mat_new[:, :, :] = 0
        else:
            image_mat_new[:, :, 0] = fill_color[0]
            image_mat_new[:, :, 1] = fill_color[1]
            image_mat_new[:, :, 2] = fill_color[2]
            image_mat_new[:, :, 3] = 255

        # 贴上原矩阵
        row_num, col_num = image_mat_new.shape[:2]
        image_mat_new[top_extend:extend_rows - bottom_extend, left_extend:col_num - right_extend, :] = image_mat
        return image_mat_new

    @staticmethod
    def cut_border(image_mat, border_color=(255, 255, 255)):
        """
        去掉指定边框，可以指定边框颜色
        :param image_mat:
        :param border_color:
        :return: image_mat
        """
        # 找到 image_mat 中值不为指定边框色的区域
        mask = np.logical_and(np.logical_and(image_mat[:, :, 0] == border_color[0],
                                             image_mat[:, :, 1] == border_color[1]),
                              image_mat[:, :, 2] == border_color[2])
        # 找到区域的上下左右边界
        x, y = zip(*np.argwhere(mask == False))
        return image_mat[min(x):max(x) + 1, min(y):max(y) + 1]

    @staticmethod
    def to_assign_shape(image_mat, assign_size):
        """图像缩放至指定的长宽，调用 Image 中的 resize 函数"""
        # 转为 image
        img = Image.fromarray(image_mat)
        # 改变长宽
        img = img.resize(assign_size)
        # 转为矩阵
        return np.array(img)

    @staticmethod
    def add_border_line(image_mat, line_weight=1, line_color=(1, 1, 1), line_inside=True):
        """
        在图像周围增加边线，边界线的宽度和位置有多种选择
        :param line_color: 线的颜色
        :param image_mat: 增加线的矩阵
        :param line_weight: 线的宽度
        :param line_inside: 先在矩阵范围内，为false，现在矩阵范围外
        :return: array
        """
        row_num, col_num = image_mat.shape[:2]
        # 线在矩阵内，扩展就矩阵
        if not line_inside:
            image_mat_new = np.zeros((image_mat.shape[0] + line_weight * 2, image_mat.shape[1] + line_weight * 2, 4),
                                     dtype=np.uint8)
            image_mat_new[line_weight:row_num + line_weight, line_weight:col_num + line_weight, :] = image_mat
            image_mat = image_mat_new
        # 线框掩膜
        row_num, col_num = image_mat.shape[:2]
        mask = np.zeros(image_mat.shape[:2], dtype=np.bool)
        mask[:line_weight, :] = True  # 上
        mask[:, :line_weight] = True  # 左
        mask[row_num - line_weight:row_num, :] = True  # 下
        mask[:, col_num - line_weight:col_num] = True  # 右
        # ------------------------------------
        image_mat[mask, 0] = line_color[0]
        image_mat[mask, 1] = line_color[1]
        image_mat[mask, 2] = line_color[2]
        image_mat[mask, 3] = 255
        # 返回矩阵
        return image_mat

    @staticmethod
    def get_word_img(word, word_color=(0, 0, 0), word_size=100, font_type='simfang.ttf',
                     background_color=(255, 255, 255), is_horizontal=True):
        """得到文字，这个很麻烦，很多的机器上解决不了，尝试解决"""
        # ------------------------------
        # 如果水平排列
        if is_horizontal:
            image_shape = (word_size, len(word) * word_size)
        else:
            image_shape = (len(word) * word_size, word_size)
            word = '\n'.join(word)

        word_loc = (0, 0)  # 文字起始位置
        # ------------------------------
        row_num, col_num = image_shape
        # 设置所使用的字体
        font = ImageFont.truetype(r"C:\Windows\Fonts\{0}".format(font_type), word_size)
        # 创建画布
        if background_color is None:
            img = Image.fromarray(ImageUtil.create_canvas(row_num, col_num))
        else:
            img = Image.fromarray(ImageUtil.create_shape_rect(row_num, col_num, fill_color=background_color))
        # 画图
        draw = ImageDraw.Draw(img)
        draw.text(word_loc, word, word_color, font=font)  # 设置文字位置/内容/颜色/字体
        # draw = ImageDraw.Draw(im1)  # Just draw it!
        image_mat = np.array(img)  # 得到矩阵
        # 去掉矩阵外面一圈边框
        if background_color is None:
            image_mat = ImageUtil.cut_border(image_mat, border_color=(255, 255, 255))
        else:
            image_mat = ImageUtil.cut_border(image_mat, border_color=background_color)
        return image_mat

    def vector(self):
        """矢量形状相关"""
        pass


class DrawPic(object):
    """画元素"""

    @staticmethod
    def __get_one_legend_rect(each_legend_info, word_length=3, row_num=20):
        """
        得到图例的一个方块
        :param each_legend_info: {'color':(0,0,0), 'data':u'标题'}
        :return: image_mat
        """
        #
        legend_word = each_legend_info['data']
        legend_color = each_legend_info['color']
        #
        rect = ImageUtil.create_shape_rect(row_num, int(2.5 * row_num), fill_color=legend_color)  # 新建矩形
        rect = ImageUtil.add_border_line(rect, 1, (0, 0, 0))  # 加边框
        word = ImageUtil.get_word_img(legend_word, word_size=row_num, background_color=None)  # 新建文字
        word = ImageUtil.extend_to_range(word, (int(row_num * 0.5), 0, 0, 0), fill_color=None)  # 文字加边框

        word_canvas = ImageUtil.create_canvas(row_num, row_num * word_length + int(row_num * 0.5))  # 新建文字画板
        # data = ImaeUtil.draw_new(word_canvas, data)  # 文字画入画板
        word = ImageUtil.draw(word_canvas, word)  # 文字画入画板
        rect = ImageUtil.cat_together(word, rect, direction=0)  # 加边框
        rect = ImageUtil.extend_to_range(rect, [int(row_num / 4)] * 4, fill_color=None)
        return rect

    @staticmethod
    def get_legend_001(legend_info, length, word_size=50):
        """画图例"""
        # FIXME 调整一下图例字体的大小，想一个可以自动调整的办法

        # FIXME 因为中文英文宽度不一样，所以不能简单的根据 data 中的字符数来决定设置多宽，而是需要根据实际情况进行指定

        # 得到色块
        legend = DrawPic.__get_one_legend_rect(legend_info[0], length, word_size)
        for index in range(len(legend_info) - 1):
            new_rect = DrawPic.__get_one_legend_rect(legend_info[index + 1], length, word_size)
            legend = ImageUtil.cat_together(legend, new_rect, 2)
        # 得到标题
        tuli = ImageUtil.get_word_img(u'图例', word_color=(0, 0, 0), word_size=int(word_size * 1.5),
                                      font_type='simhei.ttf', background_color=None)
        col_num_add = int((legend.shape[1] - tuli.shape[1]) / 2)
        tuli = ImageUtil.extend_to_range(tuli, (col_num_add, col_num_add, int(word_size / 2), int(word_size / 2)),
                                         fill_color=None)
        # 添加标题
        legend = ImageUtil.cat_together(legend, tuli, 3)
        return legend

    @staticmethod
    def get_legend(legend_info, length, word_size=50, cols_num=1):
        """画图例，支持多排的图例"""
        # 得到第一行色块
        legend = DrawPic.__get_one_legend_rect(legend_info[0], length, word_size)
        # 根据第一个色块计算需要的画布的大小
        row_num = int(math.ceil(len(legend_info) / float(cols_num)))
        canvas = ImageUtil.create_shape_rect(legend.shape[0] * row_num, legend.shape[1] * cols_num,
                                             fill_color=(255, 255, 255))
        # -------------- 绘制所有的色块 ---------------------
        for index, each_legend_info in enumerate(legend_info):
            legend_temp = DrawPic.__get_one_legend_rect(each_legend_info, length, word_size)
            # 当前图标所在行列号
            row_index = index / cols_num
            col_index = index % cols_num
            # 绘制图标
            canvas = ImageUtil.draw(canvas, legend_temp, loc=(legend.shape[0] * row_index, legend.shape[1] * col_index))
        # --------------- 图例上下留有空白 -----------------
        canvas = ImageUtil.extend_to_range(canvas, (0, 0, int(word_size * 0.5), int(word_size * 0.5)))
        # FIXME 加上图例两个字
        return canvas

    @staticmethod
    def get_compass(assign_col_num):
        """画指北针"""
        # -------------- 指北针形状 --------------------
        x, y = assign_col_num, int(1.4 * assign_col_num)
        point_list = [(x / 2, 0), (0, y), (x / 2, x), (x, y)]
        compass = ImageUtil.create_shape_polygon(point_list, (0, 0, 0), background_color=None)
        # -------------- 指北针文字 --------------------
        word = ImageUtil.get_word_img('N', word_size=int(assign_col_num), background_color=None)
        word = ImageUtil.extend_by_ratio(word, (0.6, 0.6, 0.2, 0.2), fill_color=None)
        # 合并
        compass = ImageUtil.cat_together(compass, word, 3)
        # 保存
        # ImaeUtil.save_to_image(compass, r'C:\Users\74722\Desktop\compass.png')
        return compass

    @staticmethod
    def get_date_title(assign_date, assign_col_num=1000, assign_word_size=50):
        """日期标签"""
        # 检查输入类型
        if not isinstance(assign_date, datetime.datetime):
            return

        # 新建画布
        canvas = ImageUtil.create_shape_rect(assign_word_size, assign_col_num)
        #

        # 获取时间
        year, month, day, hour, minute = assign_date.year, assign_date.month, \
                                         assign_date.day, assign_date.hour, assign_date.minute
        date_str = u'— {0}年{1}月{2}日{3}时{4}分'.format(year, month, day, hour, minute)
        date_mat = ImageUtil.get_word_img(date_str, word_color=(0, 0, 0), word_size=assign_word_size)
        # date_mat = ImaeUtil.extend_to_range(date_mat, (10,10,10,10))

        #
        image_mat = ImageUtil.draw_new(canvas, date_mat, assign_angle=1)

        return image_mat

    @staticmethod
    def get_title(title_str, assign_col_num, assign_word_size):
        """画标题"""
        # 增加画板
        canvas = ImageUtil.create_shape_rect(assign_word_size, assign_col_num)
        # 文字
        title = ImageUtil.get_word_img(title_str, word_color=(0, 0, 0), background_color=(255, 255, 255),
                                       word_size=assign_word_size, font_type='simhei.ttf')
        # 增加边框
        # title = ImaeUtil.extend_to_range(title, (assign_word_size*3, assign_word_size*3,30,30), fill_color=(255,255,255))

        # title  放在画布的中间
        loc_x = int((assign_col_num - title.shape[1]) / 2)

        title_mat = ImageUtil.draw_new(canvas, title, (0, loc_x))

        return title_mat

    @staticmethod
    def add_graticules():
        """绘制经纬网"""
        # 输入图像矩阵、仿射矩阵和经纬网的密度，得到经纬网

        pass


class ImageMapping(object):
    """出各种类型的专题图"""

    @staticmethod
    def tiff_to_pic():
        """tiff 转图片"""
        # FIXME 先不考虑裁剪边界的问题

        tiff_path = r'C:\Users\74722\Desktop\del\slope_reclass.tif'
        save_path = r'C:\Users\74722\Desktop\del\color_tiff.tif'
        color_info = {1: {}}

        for i in [1, 2, 3, 4, 5, 6, 51, 52, 53, 54]:
            color_info[1][i] = ImageUtil.get_rand_color()

        GdalBase.add_color_map_to_dataset(tiff_path, color_info, save_path=save_path)

        color_info = GdalBase.get_dataset_color_info(save_path)

        print(color_info)

    @staticmethod
    def tiff_to_image_mat(tiff_path, legend_info):
        """tiff转为标准格式，设置无值区为白色"""
        tiff_mat = GdalBase.read_tiff(tiff_path)[0]
        tiff_mat = tiff_mat.astype(np.uint8)
        # tiff_mat 转为标准格式的 Image_mat
        image_mat_r = np.ones_like(tiff_mat) * 255
        image_mat_g = np.ones_like(tiff_mat) * 255
        image_mat_b = np.ones_like(tiff_mat) * 255
        image_mat_a = np.ones_like(tiff_mat) * 255
        # 矩阵上色
        for each_legend_info in legend_info:
            print(each_legend_info)
            color_temp = each_legend_info['color']
            value_temp = each_legend_info['value']
            image_mat_r[tiff_mat == value_temp] = color_temp[0]
            image_mat_g[tiff_mat == value_temp] = color_temp[1]
            image_mat_b[tiff_mat == value_temp] = color_temp[2]
        # 矩阵操作
        image_mat = np.array([image_mat_r, image_mat_g, image_mat_b, image_mat_a])  # 二维组合成三维
        image_mat = np.rollaxis(image_mat, 0, 3)  # 调换波段顺序
        return image_mat

    @staticmethod
    def tiff_to_image_mat_SM(tiff_path):
        """tiff转为标准格式，设置无值区为白色"""
        tiff_mat = GdalBase.read_tiff(tiff_path)[0]
        # tiff_mat = tiff_mat.astype(np.uint8)
        # tiff_mat 转为标准格式的 Image_mat
        image_mat_r = tiff_mat[0, :, :]
        image_mat_g = tiff_mat[1, :, :]
        image_mat_b = tiff_mat[2, :, :]
        # image_mat_a = tiff_mat[3,:,:]
        image_mat_a = np.ones_like(tiff_mat[3, :, :])
        # 矩阵操作
        image_mat = np.array([image_mat_r, image_mat_g, image_mat_b, image_mat_a])  # 二维组合成三维
        image_mat = np.rollaxis(image_mat, 0, 3)  # 调换波段顺序
        return image_mat

    @staticmethod
    def classification(tiff_path, legend_info, legend_col_num=1, legend_word_size=40, legend_word_length=4,
                       title_str=u'标题'):
        """画需要的元素"""

        # FIXME  不需要将要调整到的数据都传入，设计标准样式，固定下来就行

        assign_col_num = 1500

        # 得到矩阵
        image_mat = ImageMapping.tiff_to_image_mat(tiff_path, legend_info)
        image_mat = ImageUtil.to_assign_shape(image_mat,
                                              (1500, int(1500 * (image_mat.shape[0] / float(image_mat.shape[1])))))
        # ------------------- 图例 --------------------------------------
        legend = DrawPic.get_legend(legend_info, legend_word_length, word_size=legend_word_size,
                                    cols_num=legend_col_num)
        # ------------------- 指北针 --------------------------------------
        compass = DrawPic.get_compass(assign_col_num=int(assign_col_num / 20))
        # ------------------- 时间 --------------------------------------
        date_title = DrawPic.get_date_title(datetime.datetime.now(), assign_col_num=1500, assign_word_size=50)
        # ------------------- 标题 --------------------------------------
        title_mat = DrawPic.get_title(title_str, 1500, 70)
        title_mat = ImageUtil.extend_to_range(title_mat, (0, 0, 50, 30))
        # ---------------------------------------------------------------
        # 增加范围
        image_mat = ImageUtil.extend_to_range(image_mat, (100, 100, 100, 100))

        # 加上指北针
        image_mat = ImageUtil.draw_new(image_mat, compass, assign_angle=1,
                                       assign_loc=(int(assign_col_num / 25), int(assign_col_num / 25)))

        # 增加边框线
        image_mat = ImageUtil.add_border_line(image_mat, 1, line_color=(0, 0, 0), line_inside=False)
        # 增加范围,下边的增加和图例的大小有关
        image_mat = ImageUtil.extend_to_range(image_mat, (0, 0, legend.shape[0], 30))

        # 增加时间标签
        image_mat = ImageUtil.cat_together(image_mat, date_title, 3)
        image_mat = ImageUtil.extend_to_range(image_mat, (0, 0, 0, 30))  # 扩展范围
        # 增加标题
        image_mat = ImageUtil.cat_together(image_mat, title_mat, 3)

        # draw 图例
        image_mat = ImageUtil.draw_new(image_mat, legend, assign_angle=2)

        # 扩展范围、加线、扩展范围
        a = 50
        image_mat = ImageUtil.extend_to_range(image_mat, (a, a, 0, a))  # 扩展范围
        image_mat = ImageUtil.add_border_line(image_mat, 2)
        image_mat = ImageUtil.extend_to_range(image_mat, (a, a, a, a))  # 扩展范围

        ImageUtil.save_to_image(image_mat, r'C:\Users\Administrator\Desktop\a.png')


if __name__ == '__main__':
    tif_path = r'C:\Users\Administrator\Desktop\file(1).tif'
    a = ImageMapping.tiff_to_image_mat_SM(tif_path) * 255

    a = a.astype(np.uint8)

    ImageUtil.save_to_image(a, save_path=r'C:\Users\Administrator\Desktop\file2.png')

    # tiffPath = r'C:\Users\Administrator\Desktop\依赖注入\temp\2b4d0821-8e4f-11e9-8bd8-6c4b905b11db\PRE_ano_clip_border.tif'
    # # tiffPath = r'C:\Users\Administrator\Desktop\依赖注入\temp\2b4d0821-8e4f-11e9-8bd8-6c4b905b11db\PRE_xun_clip_border.tif'
    #
    # legendInfo = [
    #     {'color': ImageUtil.get_rand_color(), 'data': u'一级别', 'value':1},
    #     {'color': ImageUtil.get_rand_color(), 'data': u'二级别', 'value':2},
    #     {'color': ImageUtil.get_rand_color(), 'data': u'三级别', 'value':3},
    #     {'color': ImageUtil.get_rand_color(), 'data': u'四级别', 'value':4},
    #     {'color': ImageUtil.get_rand_color(), 'data': u'五级别', 'value':5},
    #     {'color': ImageUtil.get_rand_color(), 'data': u'六级别', 'value':6},
    #     {'color': ImageUtil.get_rand_color(), 'data': u'七级别', 'value':51},
    #     {'color': ImageUtil.get_rand_color(), 'data': u'八级别', 'value':52},
    #     {'color': ImageUtil.get_rand_color(), 'data': u'九级别', 'value':53},
    #     {'color': ImageUtil.get_rand_color(), 'data': u'十级别', 'value':54},]
    #
    #
    # ImageMapping.classification(tiffPath, legendInfo, legend_col_num=3, legend_word_size=40, legend_word_length=3,
    #                             title_str=u'青海省农牧区2019年06月中旬干旱预测图')
    #

    # plt.imshow(a)
    # plt.show()
