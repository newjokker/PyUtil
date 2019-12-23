# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import gdal
import numpy as np
import os
from Report.DecoratorUtil import DecoratorUtil


class TestBlock(object):

    @staticmethod
    def get_block(tiff_path, assign_length, return_point_loc=False):
        """使用生成器来解决切片的问题"""
        dataset = gdal.Open(tiff_path)
        im_width = dataset.RasterXSize
        im_height = dataset.RasterYSize
        # 遍历每一个 block
        for i in range(0, im_width, assign_length):
            for j in range(0, im_height, assign_length):
                use_x = im_width - i if i + assign_length > im_width else assign_length
                use_y = im_height - j if j + assign_length > im_height else assign_length
                im_data = dataset.ReadAsArray(i, j, use_x, use_y)
                # print('cal   --> {0}{1}'.format(str(i).ljust(6, ' '), str(j).ljust(6, ' ')))
                if return_point_loc:
                    yield im_data, i, j
                else:
                    yield im_data

    @staticmethod
    @DecoratorUtil.time_this
    def get_block_test_with_for(tiff_path, block_length=1000):
        """使用 for 测试"""
        for each_block in TestBlock.get_block(tiff_path, block_length):
            # block 中 0 - 9 元素的个数
            print(list(map(lambda x: np.sum(each_block == x), range(10))))

    @staticmethod
    @DecoratorUtil.time_this
    def get_block_test_with_next(tiff_path, block_length=1000):
        """使用 next 关键字"""
        try:
            block_generator = TestBlock.get_block(tiff_path, block_length)
            while True:
                each_block = next(block_generator)
                print(list(map(lambda x: np.sum(each_block == x), range(10))))
        except StopIteration:
            pass

    @staticmethod
    @DecoratorUtil.time_this
    def read_and_write_tiff_use_block(tiff_path, temp_folder, block_length=1000):
        """ 读写 tiff """
        ds = gdal.Open(tiff_path)
        im_width, im_height = ds.RasterXSize, ds.RasterYSize
        im_proj, im_geotrans = ds.GetProjection(), ds.GetGeoTransform()
        del ds
        # --------------------------------------------------------------------------------------------------------------
        # 生成一个大的空 tiff
        out_path_before = os.path.join(temp_folder, 'tiff_merge_type.tif')
        dataset = gdal.GetDriverByName('GTiff').Create(out_path_before, im_width, im_height, 1, gdal.GDT_Byte)
        dataset.SetGeoTransform(im_geotrans)
        dataset.SetProjection(im_proj)
        dataset.GetRasterBand(1).SetNoDataValue(0)
        # 逐个切片处理
        block_before = TestBlock.get_block(tiff_path, block_length, return_point_loc=True)  # todo 这边可以设置返回切片的开始位置，同时已知切片的长宽
        for each_block, xoff, yoff in block_before:
            # 读取一个块，处理完之后，写入一个块
            each_block = (each_block/100).astype(np.uint8)
            each_block[each_block > 8] = 8
            dataset.GetRasterBand(1).WriteArray(each_block, xoff=xoff, yoff=yoff)
        del dataset


if __name__ == "__main__":

    """
    * 生成器的相关知识，和如何用于当前问题的解决
    * 读取单个 block
        * next 关键字，适用于同时切片多个 tiff 
        * for 关键字，只能同时切片一个 tiff 
    * 写入单个 block
    * 有没有更加优雅的写入方式，帮我解决这个问题
    * 分块读取的优劣
        * 优: （1）内存压力小，可以处理比内存大得多的数据（2）从测试结果来看，合理的分块大小能增加效率（3）能更快的发现程序中的问题
        * 缺：（1）不合理的分块影响程序执行效率（2）增加代码量，增加出错机会
                    
    """

    # todo 生成一个 20 G 左右的测试文件

    # tiff_path_001 = r'D:\Data\JiangSu\测试数据\生态系统格局数据\江苏eco2005.tif'
    tiff_path_001 = r'C:\Users\Administrator\Desktop\del\del\test_block\tiff_merge_type_mul_3.tif'

    # # todo 测试 for 关键字
    TestBlock.get_block_test_with_for(tiff_path_001, block_length=5000)
    TestBlock.get_block_test_with_for(tiff_path_001, block_length=30000)
    # #
    # # # todo 测试 next 关键字
    # TestBlock.get_block_test_with_next(tiff_path_001, block_length=20000)

    # # todo 测试读写
    # temp_folder = r'C:\Users\Administrator\Desktop\del\del\test_block'
    # TestBlock.read_and_write_tiff_use_block(tiff_path_001, temp_folder, block_length=20000)













