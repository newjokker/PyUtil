# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import gdal


def get_block(tiff_path, assign_length):
    """使用生成器来解决切片的问题"""
    dataset = gdal.Open(tiff_path)
    im_width = dataset.RasterXSize
    im_height = dataset.RasterYSize

    for i in range(0, im_width, assign_length):
        for j in range(0, im_height, assign_length):
            use_x = im_width - i if i + assign_length > im_width else assign_length
            use_y = im_height - j if j + assign_length > im_height else assign_length
            im_data = dataset.ReadAsArray(i, j, use_x, use_y)
            print('cal   --> {0}{1}'.format(str(i).ljust(6, ' '), str(j).ljust(6, ' ')))
            yield im_data


if __name__ == '__main__':

    # tiff_path = r'C:\Users\Administrator\Desktop\del\JiangSu\landuse_js.tif'
    tiff_path = r'D:\Data\JiangSu\测试数据\生态系统格局数据\江苏eco2005.tif'
    tiff_path_2 = r'D:\Data\JiangSu\测试数据\生态系统格局数据\江苏eco2000.img'

    try:
        a = get_block(tiff_path, 1000)
        b = get_block(tiff_path_2, 1000)
        while True:
            next(a)
            next(b)
    except StopIteration:
        pass

    # for i in get_block(tiff_path, 1000):
    #     print(i)















