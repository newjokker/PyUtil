# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import gdal
import os
import numpy as np
from PIL import Image, ImageEnhance
import matplotlib.pylab as plt


class ImgMatTiff(object):
    """tiff，mat，image 之间的转化 """

    # ------------------------- 四个基础变换 --------------------------
    @staticmethod
    def tiff_to_mat(path):
        """tiff 转为矩阵"""
        # 参数类型检查
        if isinstance(path, str):
            dataset = gdal.Open(path)
        elif isinstance(path, gdal.Dataset):
            dataset = path
        else:
            raise TypeError('path can only be string，unicode or dataset')

        if dataset:
            im_width = dataset.RasterXSize  # 栅格矩阵的列数
            im_height = dataset.RasterYSize  # 栅格矩阵的行数
            im_bands = dataset.RasterCount  # 波段数
            im_data = dataset.ReadAsArray(0, 0, im_width, im_height)  # 获取数据
            return im_data, im_bands

    @staticmethod
    def img_to_mat(img_path, assign_3_band=True):
        """图像转为矩阵"""

        if isinstance(img_path, str):
            img = Image.open(img_path)
        elif isinstance(img_path, Image.Image):
            img = img_path
        else:
            return

        # 读取图像矩阵
        image_mat = np.asarray(img, dtype='uint8')
        # 图像转换为可写
        image_mat.flags.writeable = True

        if len(image_mat.shape) == 2:
            # 二维矩阵
            bands = 1
            return_mat = np.array([image_mat, image_mat, image_mat], dtype=np.uint8)
        elif len(image_mat.shape) == 3:
            # 三维矩阵
            bands = image_mat.shape[2]
            # 强制转为三维矩阵
            if assign_3_band:
                return_mat = image_mat[:, :, :3]
            else:
                return_mat = image_mat
        else:
            return

        return return_mat, bands

    @staticmethod
    def mat_to_img(mat, assign_size=None, save_path=None):
        """矩阵转为图像"""

        # 规范类型
        mat_format = mat.astype(np.uint8)
        # 转为图片
        img = Image.fromarray(mat_format)

        # 改变大小
        if assign_size and mat.shape != assign_size:
            img = img.resize(assign_size)

        if save_path:
            # 当存在阿尔法图层
            if save_path[-4:].lower() == '.png' and mat.shape[2] == 4:
                print('输出图片存在 α 图层，用的是同一个 save 接口')
                img.save(save_path)
            else:
                img.save(save_path)
        else:
            return img

    @staticmethod
    def mat_to_tiff(im_data, im_width, im_height, im_bands, im_geotrans, im_proj, out_path=None,
                    no_data_value=None, return_mode='TIFF'):

        """
        写dataset（需要一个更好的名字）
        :param im_data: 输入的矩阵
        :param im_width: 宽
        :param im_height: 高
        :param im_bands: 波段数
        :param im_geotrans: 仿射矩阵
        :param im_proj: 坐标系
        :param out_path: 输出路径，str，None
        :param no_data_value: 无效值 ；num_list ，num
        :param return_mode: TIFF : 保存为本地文件， MEMORY：保存为缓存
        :return: 当保存为缓存的时候，输出为 dataset
        """
        # 保存类型选择
        if 'int8' in im_data.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in im_data.dtype.name:
            datatype = gdal.GDT_UInt16
        elif 'bool' in im_data.dtype.name:
            datatype = gdal.GDT_Byte
        else:
            datatype = gdal.GDT_Float32
        # 矩阵波段识别
        if len(im_data.shape) == 3:
            im_bands, im_height, im_width = im_data.shape
        elif len(im_data.shape) == 2:
            # 统一处理为三维矩阵
            im_data = np.array([im_data])
        else:
            im_bands, (im_height, im_width) = 1, im_data.shape
        # 根据存储类型的不同，获取不同的驱动
        if out_path:
            dataset = gdal.GetDriverByName('GTiff').Create(out_path, im_width, im_height, im_bands, datatype)
        else:
            dataset = gdal.GetDriverByName('MEM').Create('', im_width, im_height, im_bands, datatype)
        # 写入数据
        if dataset is not None:
            dataset.SetGeoTransform(im_geotrans)
            dataset.SetProjection(im_proj)
        # 写入矩阵
        for i in range(im_bands):
            dataset.GetRasterBand(i + 1).WriteArray(im_data[i])
            # 写入无效值
            if no_data_value is not None:
                # 当每个图层有一个无效值的时候
                if isinstance(no_data_value, list) or isinstance(no_data_value, tuple):
                    if no_data_value[i] is not None:
                        dataset.GetRasterBand(i + 1).SetNoDataValue(no_data_value[i])
                else:
                    dataset.GetRasterBand(i + 1).SetNoDataValue(no_data_value)
        # 根据返回类型的不同，返回不同的值
        if return_mode.upper() == 'MEMORY':
            return dataset
        elif return_mode.upper == 'TIFF':
            del dataset

    # ------------------------- 基于基础变换的变换 --------------------------

    @staticmethod
    def tiff_to_img(tif_path, img_path=None, assign_size=None):
        """只是支持将第一波段输出为黑白图像"""
        # 1. tiff to mat
        mat, band = ImgMatTiff.tiff_to_mat(tif_path)
        # 2. 转换矩阵的类型
        if len(mat.shape) == 2:
            mat = np.rollaxis(np.tile(mat, (3, 1, 1)), 0, 3)  # 单波段，转为多波段
        elif len(mat.shape) == 3:
            mat = np.rollaxis(mat[[0, 1, 2], :, :], 0, 3) * 10
        # 3. mat to image
        ImgMatTiff.mat_to_img(mat, save_path=img_path, assign_size=assign_size)

    @staticmethod
    def img_to_tiff(img_path, im_width, im_height, im_bands, im_geotrans, im_proj, out_path=None, no_data_value=None,
                    return_mode='TIFF'):
        # img to mat
        mat, band = ImgMatTiff.img_to_mat(img_path)
        # mat to tiff
        ImgMatTiff.mat_to_tiff(mat, im_width, im_height, im_bands, im_geotrans, im_proj, out_path=out_path,
                               no_data_value=no_data_value, return_mode=return_mode)

    # ------------------------- 基于变换的操作 ------------------------------

    @staticmethod
    def tiff_to_img_rgb(tif_path, assign_band, img_path=None, assign_size=None, do_stretch=False):
        """指定 tif 的三个通道 作为 rgb 三个图层"""
        # 1. tiff to mat
        mat, band = ImgMatTiff.tiff_to_mat(tif_path)
        # 2. 数据转为 rgb 需要的那种格式
        if band == 1:
            mat_rgb = np.rollaxis(np.tile(mat, (3, 1, 1)), 0, 3)  # 单波段，转为多波段
        else:
            mat_rgb = np.rollaxis(mat[[assign_band[0], assign_band[1], assign_band[2]], :, :], 0, 3)  # 2. 多波段数据，转换矩阵的类型
        # 3. 数据进行拉伸
        if do_stretch:
            mat_rgb = ImgMatTiff.do_stretch_rgb(mat_rgb)
        # 4. mat to image
        ImgMatTiff.mat_to_img(mat_rgb, save_path=img_path, assign_size=assign_size)

    @staticmethod
    def mat_to_img_rgb(mat_r, mat_g, mat_b, assign_size=None, save_path=None):
        """矩阵转为图像，前三个图层指定 rgb"""

        mat = np.zeros((mat_r.shape[0], mat_r.shape[1], 3), dtype=np.uint8)
        # 插入 r g b 图层
        mat[:, :, 0] = mat_r
        mat[:, :, 1] = mat_g
        mat[:, :, 2] = mat_b

        # 规范类型
        mat_format = mat.astype(np.uint8)
        # 转为图片
        img = Image.fromarray(mat_format)

        # 改变大小
        if assign_size and mat.shape != assign_size:
            img = img.resize(assign_size)

        if save_path:
            # 当存在阿尔法图层
            if save_path[-4:].lower() == '.png' and mat.shape[2] == 4:
                img.save(save_path)
            else:
                img.save(save_path)
        else:
            return img

    # ------------------------- 辅助函数 ------------------------------

    @staticmethod
    def do_stretch_rgb(mat):
        """拉伸每一个波段"""
        for i in range(3):
            mat[:, :, i] = mat[:, :, i] * 255.0 / (np.max(mat[:, :, i]) - np.min(mat[:, :, i]))
        return mat


if __name__ == "__main__":
    # tif_path = r'D:\Data\002. 栅格数据\fy4A\20170725\FY4A-_AGRI--_N_DISK_1047E_L1-_FDI-_MULT_NOM_20170725030000_20170725031459_4000M_V0001.tif'
    tif_path = r'D:\Code\FireDetectionH8\algorithm\AuxData\Landuse\land_use.tif'
    img_path = r'C:\Users\Administrator\Desktop\13254.jpg'

    ImgMatTiff.tiff_to_img_rgb(tif_path, [1, 2, 3], img_path=img_path, do_stretch=True)
    ImgMatTiff.tiff_to_img_rgb(tif_path, [1, 2, 3], img_path=img_path)

    exit()

    # FIXME tif 或者 mat 转为 jpg 的时候可以指定一个映射表，每一个值对应一个颜色，可以是 xml 格式的映射表和 arcgis 中类似

    savePath = r'C:\Users\Administrator\Desktop\wb\123.png'

    r = r'C:\Users\Administrator\Desktop\wb\HS_H08_20181029_0400_B01_FLDK_R20.tif'
    g = r'C:\Users\Administrator\Desktop\wb\HS_H08_20181029_0400_B02_FLDK_R20.tif'
    b = r'C:\Users\Administrator\Desktop\wb\HS_H08_20181029_0400_B03_FLDK_R20.tif'

    im_data_r, im_bands1 = ImgMatTiff.tiff_to_mat(r)
    im_data_g, im_bands2 = ImgMatTiff.tiff_to_mat(g)
    im_data_b, im_bands3 = ImgMatTiff.tiff_to_mat(b)

    ImgMatTiff.mat_to_img_rgb(im_data_r, im_data_g, im_data_b, save_path=savePath)

    # fy4 = r'D:\Data\002. 栅格数据\fy4A\20170721\FY4A-_AGRI--_N_DISK_1047E_L1-_FDI-_MULT_NOM_20170721004500_20170721005959_4000M_V0001.tif'
    #
    # ImgMatTiff.tiff_to_img_rgb(fy4, [6,7,12], img_path=save_path, assign_size=None)
    # ImgMatTiff.tiff_to_img(fy4, img_path=save_path, assign_size=None)

"""
1. img.save(img), img 有四个波段，第四个就认为是透明图层

"""
