# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from ImageUtil import ImageUtil, DrawPic
import datetime
import numpy as np
from Function.GdalUtil import GdalBase


class Example(object):
    save_path = r'C:\Users\74722\Desktop'

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
    def tiff_to_image_mat(tiff_path):
        """tiff转为标准格式"""
        # 读取 tiff 的 color_info 信息
        color_info = GdalBase.get_dataset_color_info(tiff_path)
        # 读取 tiff 的矩阵信息
        tiff_mat = GdalBase.read_tiff(tiff_path)[0]
        # tiff_mat 转为标准格式的 Image_mat
        image_mat_r = np.zeros_like(tiff_mat)
        image_mat_g = np.zeros_like(tiff_mat)
        image_mat_b = np.zeros_like(tiff_mat)
        image_mat_a = np.ones_like(tiff_mat) * 255
        # 矩阵上色
        for i in color_info[1]:
            if color_info[1][i] != (0, 0, 0, 255):
                image_mat_r[tiff_mat == i] = color_info[1][i][0]
                image_mat_g[tiff_mat == i] = color_info[1][i][1]
                image_mat_b[tiff_mat == i] = color_info[1][i][2]
        # 矩阵操作
        image_mat = np.array([image_mat_r, image_mat_g, image_mat_b, image_mat_a])  # 二维组合成三维
        image_mat = np.rollaxis(image_mat, 0, 3)  # 调换波段顺序
        return image_mat

        # # 保存
        # ImaeUtil.save_to_image(image_mat, r'C:\Users\74722\Desktop\123.png')

    # ----------------------------------------
    @staticmethod
    def draw_elements():
        """画需要的元素"""

        assign_col_num = 1500

        # 得到矩阵
        # image_mat = Example.tiff_to_image_mat(r'C:\Users\74722\Desktop\依赖注入\color_tiff.tif')
        image_mat = Example.tiff_to_image_mat(
            r'C:\Users\Administrator\Desktop\del\temp\2b4d0821-8e4f-11e9-8bd8-6c4b905b11db\PRE_ano_clip_border.tif')
        image_mat = ImageUtil.to_assign_shape(image_mat, (1500, 1500))

        # ------------------- 图例 --------------------------------------
        legend_info = [
            {'color': ImageUtil.get_rand_color(), 'data': u'第一级别'},
            {'color': ImageUtil.get_rand_color(), 'data': u'第二级别'},
            {'color': ImageUtil.get_rand_color(), 'data': u'级别三'},
            {'color': ImageUtil.get_rand_color(), 'data': u'jokker'},
            {'color': ImageUtil.get_rand_color(), 'data': u'五个级别'}, ]
        # legend = DrawPic.get_legend_001(legend_info, 4, 40)
        legend = DrawPic.get_legend(legend_info, 4, word_size=40, cols_num=2)
        # ------------------- 指北针 --------------------------------------
        compass = DrawPic.get_compass(assign_col_num=int(assign_col_num / 20))
        # ------------------- 时间 --------------------------------------
        date_title = DrawPic.get_date_title(datetime.datetime.now(), assign_col_num=1500, assign_word_size=50)
        # ------------------- 标题 --------------------------------------
        title_mat = DrawPic.get_title(u'河北的卫星监测活动的专题图', 1500, 80)
        title_mat = ImageUtil.extend_to_range(title_mat, (0, 0, 50, 30))
        # ---------------------------------------------------------------

        # 加上指北针
        image_mat = ImageUtil.draw(image_mat, compass, assign_angle=1,
                                   assign_loc=(int(assign_col_num / 25), int(assign_col_num / 25)))
        # 增加边框线
        image_mat = ImageUtil.add_border_line(image_mat, 1, line_color=(0, 0, 0), line_inside=False)
        # 增加范围,下边的增加和图例的大小有关
        image_mat = ImageUtil.extend_to_range(image_mat, (0, 0, legend.shape[0], 30))

        # 增加时间标签
        image_mat = ImageUtil.cat(image_mat, date_title, 3)
        image_mat = ImageUtil.extend_to_range(image_mat, (0, 0, 0, 30))  # 扩展范围
        # 增加标题
        image_mat = ImageUtil.cat(image_mat, title_mat, 3)

        # draw 图例
        image_mat = ImageUtil.draw(image_mat, legend, assign_angle=2)

        # 扩展范围、加线、扩展范围
        a = 50
        image_mat = ImageUtil.extend_to_range(image_mat, (a, a, 0, a))  # 扩展范围
        image_mat = ImageUtil.add_border_line(image_mat, 2)
        image_mat = ImageUtil.extend_to_range(image_mat, (a, a, a, a))  # 扩展范围

        ImageUtil.save_to_image(image_mat, r'C:\Users\Administrator\Desktop\a.png')


if __name__ == '__main__':
    Example.draw_elements()
