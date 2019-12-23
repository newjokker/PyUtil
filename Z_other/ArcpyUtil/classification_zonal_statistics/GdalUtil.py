# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import os
import ogr
import osr
import gdal
import scipy
import logging
import numpy as np
import json


class GdalAssist(object):
    """辅助 gdal 的小功能"""

    @staticmethod
    def format_detection(check_input, *args):
        """类型检查，只能是字符串和dataset"""

        check_result = False

        # 检查传入的几个格式
        for each_type in args:
            if isinstance(check_input, each_type):
                check_result = True

        return check_result


class GdalBase(object):

    @staticmethod
    def read_tiff(path):
        """
        读取 TIFF 文件
        :param path: str，unicode，dataset
        :return:
        """
        # 参数类型检查
        if isinstance(path, gdal.Dataset):
            dataset = path
        else:
            dataset = gdal.Open(path)

        if dataset:
            im_width = dataset.RasterXSize  # 栅格矩阵的列数
            im_height = dataset.RasterYSize  # 栅格矩阵的行数
            im_bands = dataset.RasterCount  # 波段数
            im_proj = dataset.GetProjection()  # 获取投影信息
            im_geotrans = dataset.GetGeoTransform()  # 获取仿射矩阵信息
            im_data = dataset.ReadAsArray(0, 0, im_width, im_height)  # 获取数据
            logging.info('read tiff success')
            return im_data, im_width, im_height, im_bands, im_geotrans, im_proj
        else:
            logging.error('error in read tiff')

    @staticmethod
    def write_tiff(im_data, im_width, im_height, im_bands, im_geotrans, im_proj, out_path=None,
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

        # FIXME  no_data_value 要注意类型

        # 保存类型选择
        if 'int8'in im_data.dtype.name or 'bool'in im_data.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in im_data.dtype.name:
            datatype = gdal.GDT_UInt16
        else:
            datatype = gdal.GDT_Float32
        # 矩阵波段识别
        if len(im_data.shape) == 3:
            im_bands, im_height, im_width = im_data.shape
        elif len(im_data.shape) == 2:
            # 统一处理为三维矩阵
            im_data = np.array([im_data], dtype=im_data.dtype)
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

    @staticmethod
    def read_tiff_with_nodata(path):
        """
        读取 TIFF 文件，读取到 nodata 信息，因为很多地方要用到，所以多加这么一个函数
        :param path: str，unicode，dataset
        :return:
        """
        # 参数类型检查
        if isinstance(path, gdal.Dataset):
            dataset = path
        else:
            dataset = gdal.Open(path)

        if dataset:
            im_width = dataset.RasterXSize  # 栅格矩阵的列数
            im_height = dataset.RasterYSize  # 栅格矩阵的行数
            im_bands = dataset.RasterCount  # 波段数
            im_proj = dataset.GetProjection()  # 获取投影信息
            im_geotrans = dataset.GetGeoTransform()  # 获取仿射矩阵信息
            im_data = dataset.ReadAsArray(0, 0, im_width, im_height)  # 获取数据
            no_data_value = GdalBase.get_no_data_value(path)
            logging.info('read tiff success')
            return im_data, im_width, im_height, im_bands, im_geotrans, im_proj, no_data_value
        else:
            logging.error('error in read tiff')

    @staticmethod
    def write_tiff_with_no_data(im_data, im_width, im_height, im_bands, im_geotrans, im_proj, no_data_value,
                                out_path=None, return_mode='TIFF'):
        """
        写dataset（需要一个更好的名字）,跟read_tiff_with_nodata进行配套
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

        # FIXME  no_data_value 要注意类型

        # 保存类型选择
        if 'int8' in im_data.dtype.name or 'bool' in im_data.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in im_data.dtype.name:
            datatype = gdal.GDT_UInt16
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

    @staticmethod
    def get_no_data_value(tif_path):
        """获取无效值"""
        # 检查输入类型
        if isinstance(tif_path, gdal.Dataset):
            ds = tif_path
        else:
            ds = gdal.Open(tif_path)
        # 遍历获取无效值
        no_data_values = []
        for i in range(1, ds.RasterCount+1):
            band_temp = ds.GetRasterBand(i)
            no_data_values.append(band_temp.GetNoDataValue())
        del ds
        return no_data_values

    @staticmethod
    def get_geotransform_info(tif_path):
        """
        获取仿射矩阵信息，返回常用的几个参数
        :param tif_path: tif 路径；str
        :return:
        """
        # 参数类型检查
        if isinstance(tif_path, gdal.Dataset):
            ds = tif_path
        else:
            ds = gdal.Open(tif_path)

        transform = ds.GetGeoTransform()
        pixel_width, pixel_height = transform[1], transform[5]  # pixel_height是负值（important）
        lon, lat = transform[0], transform[3]
        del ds
        return pixel_width, pixel_height, lon, lat

    @staticmethod
    def get_envelope(tif_path):
        """
        获取包络矩形
        :param tif_path:
        :return: 左上角经度，纬度 右下角经度，纬度
        """
        # 参数类型检查
        if isinstance(tif_path, gdal.Dataset):
            ds = tif_path
        else:
            ds = gdal.Open(tif_path)

        transform = ds.GetGeoTransform()
        rows, cols = ds.RasterYSize, ds.RasterXSize
        left, top = transform[0], transform[3]
        pixel_width, pixel_height = transform[1], transform[5]
        # 获取右下角角点经纬度
        right = left - pixel_height * cols
        bottom = top - pixel_width * rows
        del ds
        return left, top, right, bottom

    @staticmethod
    def resample(in_tif_path, cell_size, out_tif_path=None, return_mode='TIFF'):
        """
        tif 数据重采样，目前只支持 单波段影像，以后要支持多波段的
        :param in_tif_path: 输入的 tif 路径
        :param out_tif_path: 输出的 tif 路径
        :param return_mode: TIFF 保存为本地文件，MEMORY：保存为内存
        :param cell_size: 重采样之后的栅格单元的大小，单位和之前的单位保持一致，之前是用 度 现在还是用 度， 之前是 m 现在是 m
        :return: None
        """
        # FIXME 需要支持多种重采样的方式
        # TODO 可以使用 scipy.ndimage.interpolation 方法重采样（×）
        # TODO 可以使用 rasterIo 方法重采样（√）
        # TODO 可以使用 GDALwarp 方法重采样（×）
        # TODO 支持各种采样的方法（×）
        if isinstance(in_tif_path, gdal.Dataset):
            ds = in_tif_path
        else:
            ds = gdal.Open(in_tif_path)

        # 栅格单元长宽
        im_geotrans = ds.GetGeoTransform()
        pixel_width, pixel_height = im_geotrans[1], im_geotrans[5]
        # 长宽变化的倍数，5 代表 扩大五倍， 那么读取的行列要变为之前的 五分之一
        width_times = abs(cell_size / pixel_width)
        height_times = abs(cell_size / pixel_height)
        # 图像的长宽
        im_width = ds.RasterXSize  # 栅格矩阵的列数
        im_height = ds.RasterYSize  # 栅格矩阵的行数
        # 计算读取的图像的长宽栅格数目
        new_im_width = int(im_width / width_times)
        new_im_height = int(im_height / height_times)
        # 获取重采样之后的数据
        im_data = []
        for i in range(1, ds.RasterCount+1):
            band_i = ds.GetRasterBand(i)
            data_i = band_i.ReadAsArray(buf_xsize=new_im_width, buf_ysize=new_im_height)
            im_data.append(data_i)
        # 多波段数据和单波段数据分开处理
        if len(im_data) == 1:
            im_data = np.array(im_data[0])
        else:
            im_data = np.array(im_data)
        # 获得新的 tif 的各个参数 GetGeoTransform
        new_im_geotrans = list(im_geotrans)
        new_im_geotrans[1] = cell_size
        new_im_geotrans[5] = -cell_size
        im_bands = ds.RasterCount
        im_proj = ds.GetProjection()  # 获取投影信息
        # 保存数据
        no_data_value = GdalBase.get_no_data_value(ds)  # 获取原数据中的无效值
        if return_mode.upper() == 'TIFF' and out_tif_path:
            GdalBase.write_tiff(im_data, new_im_width, new_im_height, im_bands, new_im_geotrans, im_proj,
                                out_tif_path, no_data_value=no_data_value)
        elif return_mode.upper() == 'MEMORY':
            return GdalBase.write_tiff(im_data, new_im_width, new_im_height, im_bands, new_im_geotrans, im_proj,
                                       out_tif_path, return_mode='MEMORY', no_data_value=no_data_value)
        else:
            return

    @staticmethod
    def get_proj(proj_str='WGS_84'):
        """返回栅格坐标系"""
        osrobj = osr.SpatialReference()
        osrobj.SetWellKnownGeogCS(proj_str)
        return str(osrobj)

    @staticmethod
    def tiff_to_shp(tiff_path, shp_path):
        """栅格转矢量"""
        # 袁小棋贡献
        # 参数类型检查
        if isinstance(tiff_path, gdal.Dataset):
            dataset = tiff_path
        else:
            dataset = gdal.Open(tiff_path)
        # -------------------------------------------------------
        input_band = dataset.GetRasterBand(1)
        #  create output datasource
        shp_driver = ogr.GetDriverByName("ESRI Shapefile")
        proj = OgrBase.get_proj("WGS84")
        # create output file name
        output_shapefile = shp_driver.CreateDataSource(shp_path)
        new_shapefile = output_shapefile.CreateLayer(shp_path[:-4], proj)
        gdal.Polygonize(input_band, None, new_shapefile, -1, [], callback=None)
        # 当输入格式是 float 需要用下面一个函数
        # gdal.FPolygonize(input_band, None, new_shapefile, -1, [], callback=None, )
        new_shapefile.SyncToDisk()
        logging.info('tiff_to_shp success')

    @staticmethod
    def get_rect_domain(tiff_path, rect_domain_path, proj=None, domain_type='polygon'):
        """获得矩形的边界, 根据角点坐标运算得来（需要考虑图像的旋转？）"""
        left, top, right, bottom = GdalBase.get_envelope(tiff_path)
        if proj is None:
            proj = OgrBase.get_proj('WGS84')
        shape_info = [{'points': [(left, bottom), (left, top), (right, top), (right, bottom), (left, bottom)]}]
        # 绘制多边形
        if domain_type == 'polygon':
            CreateOgr.create_polygon_from_dict(shape_info, rect_domain_path, proj)
        elif domain_type == 'polyline':
            CreateOgr.create_polyline_from_dict(shape_info, rect_domain_path, proj)

    @staticmethod
    def band_combination(multiband_data, out_path=None, assign_band_index=0):
        """波段提取，提取指定的波段（default = 0）"""
        # 读取数据
        im_data, im_width, im_height, im_bands, im_geotrans, im_proj = GdalBase.read_tiff(multiband_data)
        # 无效值
        no_data_value = GdalBase.get_no_data_value(multiband_data)[assign_band_index]
        # 输出类型
        if out_path:
            return_mode = 'TIFF'
        else:
            return_mode = 'MEMORY'
        #
        return GdalBase.write_tiff(im_data[assign_band_index, :, :], im_width, im_height, 1,
                                   im_geotrans, im_proj, out_path, return_mode=return_mode, no_data_value=no_data_value)

    @staticmethod
    def layer_stacking_from_multiband(multiband_data, use_band, save_path=None):
        """从多波段栅格进行，波段合成，从输入的多波段数据中挑选数据，或者将输入的几个单波段数据进行融合"""
        # 参数类型检查
        if isinstance(multiband_data, gdal.Dataset):
            dataset = multiband_data
        else:
            dataset = gdal.Open(multiband_data)
        # ----------------------------------------------------------------------------
        if dataset:
            im_width = dataset.RasterXSize  # 栅格矩阵的列数
            im_height = dataset.RasterYSize  # 栅格矩阵的行数
            im_proj = dataset.GetProjection()  # 获取投影信息
            im_geotrans = dataset.GetGeoTransform()  # 获取仿射矩阵信息
            # ----------------------------------------------------------------------------
            if save_path:
                dataset_new = gdal.GetDriverByName('GTiff').Create(save_path, im_width, im_height, len(use_band))
            else:
                dataset_new = gdal.GetDriverByName('MEM').Create(save_path, im_width, im_height, len(use_band))
            # ----------------------------------------------------------------------------
            dataset_new.SetGeoTransform(im_geotrans)
            dataset_new.SetProjection(im_proj)
            # ----------------------------------------------------------------------------
            for band_index, each_band in enumerate(use_band):
                band_array = dataset.GetRasterBand(use_band[band_index]).ReadAsArray(0, 0, im_width, im_height)
                dataset_new.GetRasterBand(band_index+1).WriteArray(band_array)
                print('get band {0}'.format(each_band))
                del band_array

            if not save_path:
                return dataset_new

    @staticmethod
    def layer_stacking_from_singleband(save_path=None, *args):
        """从多个单波段栅格进行波段合成"""
        im_data = []
        no_data_value = []

        if len(args) >= 1:
            im_width, im_height, im_bands, im_geotrans, im_proj = GdalBase.read_tiff(args[0])[1:]
        else:
            raise EOFError('need at least one band')

        # 遍历输入的数据
        for each_band in args:
            im_data_temp, im_width, im_height, im_bands, im_geotrans, im_proj = GdalBase.read_tiff(each_band)
            # 检查数据是否为单波段数据
            if not im_bands == 1:
                raise EOFError('need singleband data')
            im_data.append(im_data_temp)
            no_data_value.extend(GdalBase.get_no_data_value(each_band))

        # 输出类型
        if save_path:
            return_mode = 'TIFF'
        else:
            return_mode = 'MEMORY'

        if im_data:
            return GdalBase.write_tiff(np.array(im_data), im_width, im_height, im_bands, im_geotrans, im_proj,
                                       save_path, return_mode=return_mode, no_data_value=no_data_value)

    # -------------------- need to perfect -------------
    @staticmethod
    def get_domain(tiff_path, return_shp_path):
        """得到栅格范围"""
        # TODO 可以使用设置无效值，然后栅格转面

        tiff_path = r'C:\Users\74722\Desktop\del\test.tif'

        im_data, im_width, im_height, im_bands, im_geotrans, im_proj = GdalBase.read_tiff(tiff_path)

        no_data_value = GdalBase.get_no_data_value(tiff_path)[0]

        im_data[im_data != no_data_value] = 1
        im_data = im_data.astype(np.int)

        new_tiff = GdalBase.write_tiff(im_data, im_width, im_height, im_bands, im_geotrans, im_proj ,
                                       no_data_value=[no_data_value], return_mode='MEMORY')

        # 矢量转栅格的函数是有问题的，导致出的结果不对，但是我的思路是没有问题的
        GdalBase.tiff_to_shp(new_tiff, r'C:\Users\74722\Desktop\del\hehe7.shp')

    @staticmethod
    def map_algebra(tiff_path, func, save_path=None, return_mode='TIFF'):
        """单波段 database 简单运算, 传入一个函数，用这个函数对数据进行运算"""
        # FIXME 暂不支持处理无效值数据
        # 读取 dataset
        im_data, im_width, im_height, im_bands, im_geotrans, im_proj, no_data_value = GdalBase.read_tiff_with_nodata(tiff_path)
        # -------------------------------------------------------
        # 波段运算
        im_data = func(im_data)
        # 写数据
        return GdalBase.write_tiff_with_no_data(im_data, im_width, im_height, im_bands, im_geotrans, im_proj, no_data_value,
                                         out_path=save_path, return_mode=return_mode)

    @staticmethod
    def add_color_map_to_dataset(input_path, color_info, save_path=None):
        """
        将颜色表写入dataset
        :param input_path:
        :param color_info: 每一个波段的颜色表 {1:{1:(123, 123, 0), 2:(255, 255, 0)}, 2:{}}， 注意是 从 1 开始的
        :param save_path:
        :return: dataset
        """
        # FIXME 多波段 tif 数据没有测试

        # 参数类型检查
        if isinstance(input_path, gdal.Dataset):
            dataset = input_path
        else:
            dataset = gdal.Open(input_path)

        # 波段数
        im_bands = dataset.RasterCount

        if save_path:
            # 获取基本信息
            im_data, im_width, im_height, im_bands, im_geotrans, im_proj = GdalBase.read_tiff(input_path)
            # 获取 NoData 信息
            no_data_value = GdalBase.get_no_data_value(input_path)
            # 只能保存为 Byte 类型，其他的类型默认无法设置 color_info 信息
            datatype = gdal.GDT_Byte

            # 矩阵波段识别
            if len(im_data.shape) == 3:
                im_bands, im_height, im_width = im_data.shape
            elif len(im_data.shape) == 2:
                im_data = np.array([im_data])
            else:
                im_bands, (im_height, im_width) = 1, im_data.shape

            # 获取驱动
            dataset = gdal.GetDriverByName('GTiff').Create(save_path, im_width, im_height, im_bands, datatype)

            if dataset is not None:
                dataset.SetGeoTransform(im_geotrans)
                dataset.SetProjection(im_proj)
            else:
                logging.error('error in get drive')
                return

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

        # 写入 color_info
        # 遍历波段
        for i in range(1, im_bands + 1):
            # 如果当前波段有颜色表
            if i in color_info:
                # 新建颜色表
                color_table = gdal.ColorTable(gdal.GPI_RGB)
                # 遍历所有的颜色等级
                for each_class in color_info[i]:
                    color_table.SetColorEntry(each_class, color_info[i][each_class])
                dataset.GetRasterBand(i).SetColorTable(color_table)

        if not save_path:
            return dataset

    @staticmethod
    def save_dataset_to_local(dataset, save_path):
        """将 dataset 保存到本地"""

        # FIXME 然道保存数据到本地必须从drive新建dataset 然后，一个一个波段的写？
        # 读取数据信息
        im_data, im_width, im_height, im_bands, im_geotrans, im_proj = GdalBase.read_tiff(dataset)
        # 写入本地文件
        GdalBase.write_tiff(im_data, im_width, im_height, im_bands, im_geotrans, im_proj, out_path=save_path)

    @staticmethod
    def get_dataset_color_info(input_path):
        """将dataset中的color信息读取到字典中去"""

        # 返回的颜色字典信息
        color_info = {}
        #
        dataset = gdal.Open(input_path)

        if isinstance(dataset, gdal.Dataset):
            # 波段数
            im_bands = dataset.RasterCount
            #
            for band_index in range(1, im_bands + 1):

                band = dataset.GetRasterBand(1).GetColorTable()

                color_info_one_band = {}

                for i in range(256):
                    # 获取颜色
                    color_entry = band.GetColorEntry(i)
                    # 给颜色字典
                    color_info_one_band[i] = color_entry

                # 更新信息
                color_info[band_index] = color_info_one_band

        return color_info

    @staticmethod
    def as_type(tif_path):
        """改变 tif 的数据类型"""

        # 可能用到 band 中的 GetRasterDataType

        pass

    @staticmethod
    def cut_no_value_side():
        """裁剪掉 nan 的四边"""
        pass


class GdalTools(object):
    """基于 gdal, gdalBase 写的小工具"""

    @staticmethod
    def extension_tif(tif_path, out_tif_path=None, extenction_range=(0, 0, 0, 0), return_mode='TIFF'):
        """
        扩展栅格，将栅格往上下左右进行扩展，以栅格数为单位
        :param return_mode: 输出模式，TIFF: 输出本地文件，'MAT':返回矩阵 , 'MEMORY': 返回 dataset
        :param tif_path: tif 路径
        :param out_tif_path: 输出 tif 路径
        :param extenction_range: 扩展范围（上下左右），正数为增加栅格，负数为减少栅格，0为不改变
        :return: None
        """

        # 当输出模式为 图层，但是没有 out_tif_path 的时候
        if not out_tif_path and return_mode.upper() == 'TIFF':
            return

        # 1. 读取数据
        im_data, im_width, im_height, im_bands, im_geotrans, im_proj = GdalBase.read_tiff(tif_path)
        # 参数类型检查
        if isinstance(tif_path, gdal.Dataset):
            ds = tif_path
        else:
            ds = gdal.Open(tif_path)

        # 获取 dataset 的基础信息
        no_data_value = GdalBase.get_no_data_value(ds)
        transform = ds.GetGeoTransform()
        rows, cols, band = ds.RasterYSize, ds.RasterXSize, ds.RasterCount
        lon, lat = transform[0], transform[3]
        pixel_width, pixel_height = transform[1], transform[5]  # pixel_height是负值（important）
        # 2. 改变左上角角点的位置
        after_move_lon = lon + pixel_height * extenction_range[2]  # 移动的经度
        after_move_lat = lat + pixel_width * extenction_range[0]  # 移动的纬度
        # 重写 im_geotrans 文件
        new_geotrans = list(im_geotrans)
        new_geotrans[0] = after_move_lon
        new_geotrans[3] = after_move_lat
        new_geotrans = tuple(new_geotrans)
        # 3. 生成新的矩阵
        top, bottom, left, right = extenction_range
        new_rows = rows + top + bottom
        new_cols = cols + left + right
        # 4. 根据无效值，调整需要的矩阵
        if band == 1:
            if no_data_value[0] is None:
                no_data_value[0] = np.nan
                result_mat = np.ones((new_rows, new_cols), dtype=np.float16) * np.nan
            else:
                result_mat = np.ones((new_rows, new_cols), dtype=np.float16) * no_data_value[0]
        else:
            result_mat = []
            for each_band in range(band):
                if no_data_value[each_band] is None:
                    temp_no_data = np.nan
                    no_data_value[each_band] = np.nan
                else:
                    temp_no_data = no_data_value[each_band]
                mat_temp = np.ones((new_rows, new_cols)) * temp_no_data
                result_mat.append(mat_temp)
            result_mat = np.array(result_mat)
        result_mat.astype(im_data.dtype)
        # 赋值新矩阵
        a, b, c, d = 0, rows, 0, cols
        # 规范 im_data 值的范围, 注意：是从 top:bottom , left:right
        if top < 0:
            a = abs(top)
        if bottom < 0:
            b = bottom
        if left < 0:
            c = abs(left)
        if right < 0:
            d = right
        # 规范新矩阵范围
        a2, b2, c2, d2 = top, rows + top, left, cols + left
        if top < 0:
            a2 = 0
        if left < 0:
            c2 = 0
        # 矩阵之间赋值
        if band == 1:
            result_mat[a2:b2, c2:d2] = im_data[a:b, c:d]
        else:
            result_mat[:, a2:b2, c2:d2] = im_data[:, a:b, c:d]

        if return_mode.upper() == 'TIFF':
            # 4. 生成新的 tif
            GdalBase.write_tiff(result_mat, new_cols, new_rows, im_bands, new_geotrans,
                                im_proj, out_tif_path, no_data_value=no_data_value)

        elif return_mode.upper() == 'MAT':
            return result_mat

        elif return_mode.upper() == 'MEMORY':
            return GdalBase.write_tiff(result_mat, new_cols, new_rows, im_bands, new_geotrans,
                                       im_proj, None, no_data_value=no_data_value, return_mode='MEMORY')

    @staticmethod
    def mean_synthesis(tif_paths, result_com_path, nan_symbol, value_min, value_max):
        """
        均值合成
        :param result_com_path: 合成文件路径
        :param tif_paths:    tif路径列表  [tifPath1, tifPath1, ...]
        :param nan_symbol:   无效值(数值)
        :param value_min:    值域最小值（数值）
        :param value_max:    值域最大值（数值）
        :return:
        """

        # 获取 tif 属性
        im_width, im_height, im_bands, im_geotrans, im_proj = GdalBase.read_tiff(tif_paths[0])[1:]
        # 计数器
        com_index = np.zeros((im_height, im_width))
        # 总和
        com_result_temp = np.zeros((im_height, im_width))
        # 无值区
        nan_data_temp = np.zeros((im_height, im_width))

        for eachTifPath in tif_paths:
            # 读取 tif 矩阵
            data_mat = GdalBase.read_tiff(eachTifPath)[0]
            # 将无效值改为固定的数字
            data_mat[np.isnan(data_mat)] = nan_symbol
            # 将值域外的数据设为无效值
            data_mat[data_mat < value_min] = nan_symbol
            data_mat[data_mat > value_max] = nan_symbol
            # 当不等于无效值的时候，计数器加一
            com_index += data_mat != nan_symbol
            # 将无效值赋值为0，并更新总和矩阵（因为加0等于没有加，所以将无效值设为0）
            data_mat[data_mat == nan_symbol] = 0
            com_result_temp += data_mat

        # 设置无值区 index 为 0 的区域为无值区，为了防止除数为1，对index中为0的区域设置为1
        nan_data_temp[com_index == 0] = 1
        com_index[com_index == 0] = 1
        # 得到均值，计数器需转为 float 型数据
        com_result = com_result_temp / com_index.astype(np.float)
        # 将设置无效值范围，之前的无效值区域值为 0
        com_result[nan_data_temp == 1] = nan_symbol
        # 保存均值合成之后的数据
        GdalBase.write_tiff(com_result, im_width, im_height, im_bands, im_geotrans, im_proj, result_com_path)
        logging.info('mean_synthesis success')

    @staticmethod
    def mean_synthesis_pro(tif_paths, result_com_path, nan_symbol, value_min, value_max):
        """
        均值合成，不限定 tif 的范围是否一致，但是 tif 的栅格大小一定是一致的
        :param result_com_path: 合成文件路径
        :param tif_paths:    tif路径列表  [tifPath1, tifPath1, ...]
        :param nan_symbol:   无效值(数值)
        :param value_min:    值域最小值（数值）
        :param value_max:    值域最大值（数值）
        :return: None
        """
        # FIXME 这个版本已经无效，需要用心的方式处理无效值

        # FIXME 可以制定 数据的范围，将所有的数据扩展到那个范围即可

        # 获取 tif_list 列表中所有 tif 的范围的并集
        result_tif_region = GdalTools.merge_region(tif_paths)
        # 获取 tif 属性
        im_width, im_height, im_bands, im_geotrans, im_proj = GdalBase.read_tiff(tif_paths[0])[1:]
        # 更新仿射矩阵信息
        im_geotrans_temp = list(im_geotrans)
        im_geotrans_temp[0] = result_tif_region[0]
        im_geotrans_temp[3] = result_tif_region[1]
        im_geotrans = tuple(im_geotrans_temp)
        # 更新矩阵行列信息
        tif_temp = gdal.Open(tif_paths[0])
        transform = tif_temp.GetGeoTransform()
        pixel_width, pixel_height = transform[1], transform[5]  # pixel_height是负值（important）
        im_width = int(round((abs(result_tif_region[0] - result_tif_region[2])) / abs(pixel_width)))
        im_height = int(round((abs(result_tif_region[1] - result_tif_region[3])) / abs(pixel_height)))
        # 计数器
        com_index = np.zeros((im_height, im_width))
        # 总和
        com_result_temp = np.zeros((im_height, im_width))
        # 无值区
        nan_data_temp = np.zeros((im_height, im_width))

        for eachTifPath in tif_paths:
            # 获取扩展后的 tif 矩阵，仅返回矩阵
            data_mat = GdalTools.extent_tif_to_range(eachTifPath, result_tif_region,
                                                     return_mode='MAT', assign_size=(im_height, im_width))
            # 将无效值改为固定的数字
            data_mat[np.isnan(data_mat)] = nan_symbol
            # 将值域外的数据设为无效值
            data_mat[data_mat < value_min] = nan_symbol
            data_mat[data_mat > value_max] = nan_symbol
            # 当不等于无效值的时候，计数器加一
            com_index += data_mat != nan_symbol
            # 将无效值赋值为0，并更新总和矩阵（因为加0等于没有加，所以将无效值设为0）
            data_mat[data_mat == nan_symbol] = 0
            com_result_temp += data_mat

        # 设置无值区 index 为 0 的区域为无值区，为了防止除数为1，对index中为0的区域设置为1
        nan_data_temp[com_index == 0] = 1
        com_index[com_index == 0] = 1
        # 得到均值，计数器需转为 float 型数据
        com_result = com_result_temp / com_index.astype(np.float)
        # 将设置无效值范围，之前的无效值区域值为 0
        com_result[nan_data_temp == 1] = nan_symbol
        # 保存均值合成之后的数据
        GdalBase.write_tiff(com_result, im_width, im_height, im_bands, im_geotrans, im_proj, result_com_path)
        logging.info('mean_synthesis_pro success')

    @staticmethod
    def mm_synthesis(tif_paths, result_com_path, nan_symbol, mode, value_min, value_max):
        """
        最大值，最小值合成
        :param mode: 合成模式，最大值合成 or 最小值合成
        :param result_com_path: 合成结果输出路径
        :param tif_paths:    tif路径列表  [tifPath1, tifPath1, ...]
        :param nan_symbol:   无效值(数值)
        :param value_min:    值域最小值（数值）
        :param value_max:    值域最大值（数值）
        :return:
        """

        # 获取 tif 属性
        im_width, im_height, im_bands, im_geotrans, im_proj = GdalBase.read_tiff(tif_paths[0])[1:]
        # 无值区
        nan_data = np.ones((im_height, im_width))
        # 输出结果
        if mode.lower() == "min":
            mm_result = np.ones((im_height, im_width)) * value_max + 1
        elif mode.lower() == "max":
            mm_result = np.ones((im_height, im_width)) * value_min - 1
        else:
            logging.error('mm_synthesis , mode can only be min or max')
            return

        for eachTifPath in tif_paths:
            # 读取 tif 矩阵
            data_mat = GdalBase.read_tiff(eachTifPath)[0]
            # 将无效值改为固定的数字
            data_mat[np.isnan(data_mat)] = nan_symbol
            # 将值域外的数据设为无效值
            data_mat[data_mat < value_min] = nan_symbol
            data_mat[data_mat > value_max] = nan_symbol
            # 获取感兴趣区（roi），计算最大值
            roi = data_mat != nan_symbol
            # 更新有值区
            nan_data[roi] = 0
            # 最值替换
            if mode.lower() == "max":
                mm_result[roi] = scipy.fmax(data_mat[roi], mm_result[roi])
            elif mode.lower() == "min":
                mm_result[roi] = scipy.fmin(data_mat[roi], mm_result[roi])

        # 将无值区进行替换
        mm_result[nan_data == 1] = nan_symbol
        # 保存均值合成之后的数据
        GdalBase.write_tiff(mm_result, im_width, im_height, im_bands, im_geotrans, im_proj, result_com_path)
        logging.info('mm_synthesis success')

    @staticmethod
    def mean_filter(file_path, result_path, nan_symbol):
        """
        均值滤波
        :param file_path:    tif数据
        :param result_path:  输出路径
        :param nan_symbol:   无效值
        :return:
        """

        # FIXME 这个实现的比较 low 可以直接用卷积运算进行替换

        def mean_windows(data_windows, nan_symbol_temp):
            """
             3*3 单窗口处理
            :param data_windows: 单一窗口得到的矩阵
            :param nan_symbol_temp: 忽略值
            :return:
            """
            # 设置中间的值为 nan
            data_windows[1, 1] = nan_symbol_temp
            # 除了 nan 值之外，计算均值
            window_result = np.mean(data_windows[data_windows != nan_symbol_temp])
            # 如果均值为 nan 返回 nanSymbolTemp
            if np.isnan(window_result):
                return nan_symbol_temp
            else:
                return window_result

        # 1. 获取 tif 数据
        tif_mat, im_width, im_height, im_bands, im_geotrans, im_proj = GdalBase.read_tiff(file_path)
        # 2. 初始化结果矩阵
        result = np.zeros((im_height, im_width))
        # 初始化遍历矩阵，在矩阵外加框，用以解决边界的情况
        data_temp = np.ones((im_height + 2, im_width + 2)) * nan_symbol
        data_temp[1:im_height + 1, 1:im_width + 1] = tif_mat

        # 3. 窗口遍历
        for i in range(im_height):
            for j in range(im_width):
                temp_window = data_temp[i:i + 3, j:j + 3]
                result[i, j] = mean_windows(temp_window, nan_symbol)

        # 4. 保存结果
        GdalBase.write_tiff(result, im_width, im_height, im_bands, im_geotrans, im_proj, result_path)
        print("* 完成中值滤波")

    @staticmethod
    def extent_tif_to_range(in_tif, temp_range, save_path=None, return_mode='TIFF', assign_size=None):
        """
        扩展 tif 到指定的范围，四舍五入
        :param in_tif: tif 路径；str
        :param temp_range: 需要扩展到的范围，tuple；(左上角经度，左上角纬度，右下角经度，右下角纬度)
        :param save_path: 扩展后的 tif 保存路径
        :param return_mode: TIFF：保存扩展后的 tif 为文件，MAT：返回扩展后的 tif 的 矩阵, MEMORY：返回 dataset
        :param assign_size: 指定行列数，有时候对扩展后的行列数有要求，所以可以在此处指定
        :return: mode = 0 时，返回None ，保存为本地文件，mode = 1 时，返回扩展后的 tif 矩阵，
        """
        # FIXME 指定左上角坐标（或者左上角坐标就是传入的范围的左上角，不然会对应不起来）
        # FIXME 拉伸到底是以之前的图片为原点进行拉伸，还是拉伸后左上角角点和拉伸范围的角点重合
        # 获取 tif 的范围
        tif_range = GdalBase.get_envelope(in_tif)
        # 计算 tif 的范围和设定的范围之间的差值，分为 上下左右，四个边进行处理
        # 参数类型检查

        if isinstance(in_tif, gdal.Dataset):
            tif_temp = in_tif
        else:
            tif_temp = gdal.Open(in_tif)

        transform = tif_temp.GetGeoTransform()
        # 获取栅格长和高
        rows, cols = tif_temp.RasterYSize, tif_temp.RasterXSize
        pixel_width, pixel_height = transform[1], transform[5]  # pixel_height是负值（important）
        # 上下左右扩展栅格数目
        shang_extent = (temp_range[1] - tif_range[1]) / abs(pixel_height)
        xia_extent = (tif_range[3] - temp_range[3]) / abs(pixel_height)
        zuo_extent = (tif_range[0] - temp_range[0]) / abs(pixel_width)
        you_extent = (temp_range[2] - tif_range[2]) / abs(pixel_width)
        # 当已经指定了输出行列的时候，按照指定的行列进行输出
        if assign_size:
            assign_row, assign_cols = assign_size[0], assign_size[1]
            # 当指定行列小于当前行列的时候，直接去掉右边，下边的数据
            cha_rows = rows + shang_extent + xia_extent - assign_row
            cha_cols = cols + zuo_extent + you_extent - assign_cols
            # 扩展可以设置为整数和负数
            xia_extent -= cha_rows
            you_extent -= cha_cols
        # 获取上下左右扩展多少栅格单位长度
        shang_extent, xia_extent, zuo_extent, you_extent = \
            int(round(shang_extent)), int(round(xia_extent)), int(round(zuo_extent)), int(round(you_extent))

        # 根据保存的模式进行保存
        extent = (shang_extent, xia_extent, zuo_extent, you_extent)
        return GdalTools.extension_tif(in_tif, save_path, extent, return_mode=return_mode.upper())

    @staticmethod
    def merge_region(tif_list):
        """
        获取 tif_list 中所有 tif 的范围的并集
        :param tif_list: tif 路径列表；[tif_path1, tif_path2, tif_path3, ...]
        :return: (左上角经度，左上角纬度，右下角经度，右下角纬度)
        """

        # FIXME 对于矢量，使用标准的方法（内置），栅格也要变为矢量的方式

        result_region = [np.inf, -np.inf, -np.inf, np.inf]
        # 遍历 tif
        for each_tif in tif_list:
            # 读取每一个 tif 的范围
            x_min, y_max, x_max, y_min = GdalBase.get_envelope(each_tif)
            # 更新 tif 范围
            result_region[0] = min(x_min, result_region[0])
            result_region[1] = max(y_max, result_region[1])
            result_region[2] = max(x_max, result_region[2])
            result_region[3] = min(y_min, result_region[3])
        logging.info('merge_region success')
        return tuple(result_region)

    @staticmethod
    def intersect_region(tif_list):
        """
        获取 tif_list 中所有 tif 的范围的交集
        :param tif_list: tif_list: tif 路径列表；[tif_path1, tif_path2, tif_path3, ...]
        :return: (左上角经度，左上角纬度，右下角经度，右下角纬度)
        """
        result_region = [-np.inf, np.inf, np.inf, -np.inf]
        # 遍历 tif
        for each_tif in tif_list:
            # 读取每一个 tif 的范围
            # x_min, y_max, x_max, y_min = GdalBase.get_region(each_tif)
            x_min, y_max, x_max, y_min = GdalBase.get_envelope(each_tif)
            # 更新 tif 范围
            result_region[0] = max(x_min, result_region[0])
            result_region[1] = min(y_max, result_region[1])
            result_region[2] = min(x_max, result_region[2])
            result_region[3] = max(y_min, result_region[3])

        # 当交集为一条直线或者没有交集的时候，返回 None
        if result_region[0] >= result_region[2] or result_region[1] <= result_region[3]:
            return None
        logging.info('intersect_region success')
        return tuple(result_region)

    @staticmethod
    def extract_by_mask(shp_path, tif_path, out_path=None, return_mode='TIFF'):
        """
        掩膜提取, 得到的结果的栅格大小和地图的栅格大小一致
        :param shp_path: 掩膜矢量；str
        :param tif_path: tif 底图；str
        :param out_path: 输出文件名；str
        :param return_mode: 输出类型，TIFF：本地 tiff 文件，MAT：矩阵，MEMORY：dataset
        :return:
        """
        # FIXME 有一个小 bug 需要进行修改，就是如何矢量和栅格之间没有重合的区域就会报错，这个应该直接返回一个全部是无效值的栅格就好了

        # TODO 掩膜可以是矩阵或者是dataset
        # 读取需要裁剪的 tif 文件
        im_data, im_width, im_height, im_bands, im_geotrans, im_proj = GdalBase.read_tiff(tif_path)
        cell_size = im_geotrans[1]
        # 矢量转栅格
        temp_tif_path = OgrBase.shp_to_tif(shp_path, None, cell_size, return_mode='MEMORY')
        # 获取 shp 和 tif 的交集
        intersect_region = GdalTools.intersect_region([temp_tif_path, tif_path])
        # 根据栅格大小和交集范围，计算行列数
        lie = round((intersect_region[2] - intersect_region[0]) / cell_size)
        hang = round((intersect_region[1] - intersect_region[3]) / cell_size)
        # 返回交集范围内的矩阵信息
        mask = GdalTools.extent_tif_to_range(temp_tif_path, intersect_region,
                                             return_mode='MAT', assign_size=[hang, lie])

        tif_in_new_region = GdalTools.extent_tif_to_range(tif_path, intersect_region, return_mode='MAT',
                                                          assign_size=[hang, lie])
        # 属性数据转换为掩膜数据
        mask_data = mask > 0
        # 设定无效值
        no_data_value = GdalBase.get_no_data_value(tif_path)
        if im_bands > 1:
            for band_index in range(im_bands):
                if no_data_value[band_index] is None:
                    tif_in_new_region[band_index, :, :][~mask_data] = np.nan
                    no_data_value[band_index] = np.nan
                else:
                    tif_in_new_region[band_index, :, :][~mask_data] = no_data_value[band_index]
        else:
            if no_data_value[0] is None:
                tif_in_new_region[~mask_data] = np.nan
                no_data_value[0] = np.nan
            else:
                tif_in_new_region[~mask_data] = no_data_value[0]
        # 获取新的仿射矩阵
        new_geotrans = list(im_geotrans)
        new_geotrans[0] = intersect_region[0]
        new_geotrans[3] = intersect_region[1]
        # 写数据
        if return_mode == 'MAT':
            return tif_in_new_region
        else:
            return GdalBase.write_tiff(tif_in_new_region, int(lie), int(hang), int(im_bands), new_geotrans,
                                im_proj, out_path, no_data_value=no_data_value, return_mode=return_mode)

    # -------------------- need to perfect -------------
    @staticmethod
    def extract_loc_xy_in_tiff(tif_path, points_loc_lonlat):
        """
        获取点在tif中对应位置的值
        :param tif_path: tif 文件路径，单波段
        :param points_loc_lonlat: 点坐标
        :return: float OR int
        """
        # FIXME 这个函数设计有问题，需要好好的修改
        # --------------------------------------------------------------------------------------------------------------
        im_data, im_width, im_height, im_bands, im_geotrans, im_proj = GdalBase.read_tiff(tif_path)
        pixel_width, pixel_height = im_geotrans[1], im_geotrans[5]
        lon1, lat1, lon2, lat2 = GdalBase.get_envelope(tif_path)
        # --------------------------------------------------------------------------------------------------------------
        point_loc_xy = []
        for each_point in points_loc_lonlat:
            # 拿到经纬度
            point_lon, point_lat = each_point
            # 判断点是否在范围内部
            if not (lon1 <= point_lon <= lon2 and lat2 <= point_lat <= lat1):
                # logging.error('point isnot in assign region')
                point_loc_xy.append((None, None))
                continue
            # 获取点所在栅格行列，返回栅格值
            offset_lon = point_lon - lon1
            offset_lat = point_lat - lat1
            offset_lon_cell = int(offset_lon / pixel_width)
            offset_lat_cell = int(offset_lat / pixel_height)
            # 返回栅格值在字典中的数据类型
            point_loc_xy.append((offset_lat_cell, offset_lon_cell))
        return point_loc_xy

    @staticmethod
    def mm_synthesis_pro():
        """最大最小值合成，不需要值是同一长宽，同一范围，有两个模式，计算无数据的范围，不计算无数据的范围"""
        pass

    @staticmethod
    def mosaic(tif_1, tif_2, mosaic_tif, mode='first'):
        """
        镶嵌，将 tif_list 里的 tif 镶嵌到 mosaic_tif 中，mode 选择镶嵌的类型，使用 extent_tif_to_range 里面的方法
        :param mode: 镶嵌的类型，照着 Arcgis 里面的写
        :param tif_2: str_list，需要镶嵌的 tif 列表
        :param tif_1: str_list，需要镶嵌的 tif 列表
        :param mosaic_tif: 镶嵌结果，tif
        :return: None
        """

        # FIXME 需要栅格大小一致

        # 找到两个 tif 的合并范围
        # 新建矩阵
        # 对两个矩阵进行扩展 使用 extent_tif_to_range
        # 写入偏移后的矩阵 1，2，矩阵的是否偏移无所谓，就是忽略矩阵的轻微位移

    @staticmethod
    def zonal_statistics(tif_path, mask_path, attribute=None, stastic_mode='MEAN', return_mode='DICT'):
        """
        分区统计
        :param tif_path: 要统计的 tif ；dataset or str
        :param mask_path: 掩膜， ndarry or dataset or str, 如果输入的是 str 的话就不能直接判断是 dataset 还是 datasourse 了
        :param stastic_mode: 统计的类型 MAX、MIN、MEAN; str
        :param attribute: 统计的属性，当输入不为 shp 时，此变量不起作用
        :param return_mode: 返回类型，'DICT' or 'TIF' or 'MAT' ; 字典，tiff 文件 或者 矩阵，str
        :return:
        """

        if isinstance(tif_path, gdal.Dataset):
            input_raster = tif_path
        else:
            input_raster = gdal.Open(tif_path)

        geotrans = input_raster.GetGeoTransform()
        cell_size = geotrans[1]
        # 分区文件转为 tif
        if isinstance(mask_path, gdal.Dataset):
            zonal_tif = mask_path
        elif isinstance(mask_path, str):
            if mask_path.endswith('.tif'):
                zonal_tif = gdal.Open(mask_path)
            elif mask_path.endswith('.shp'):
                # FIXME 这边 shp 转 tif 之后值就变了，看看怎么回事
                zonal_tif = OgrBase.shp_to_tif(mask_path, None, cell_size, shp_attribute=attribute,
                                               return_mode='MEMORY')
            else:
                return
        else:
            return

        # 如果 cell_size 不一致，需要重采样
        zonal_tif = GdalBase.resample(zonal_tif, cell_size, out_tif_path=None, return_mode='MEMORY')
        # 范围交集
        interset_region = GdalTools.intersect_region([zonal_tif, tif_path])
        # 被统计的栅格
        input_raster_extent = GdalTools.extent_tif_to_range(tif_path, interset_region, None, 'MAT')
        # 提取需要的属性
        im_width, im_height, im_bands = GdalBase.read_tiff(tif_path)[1:4]
        # 统计的区域
        zone_raster = GdalTools.extent_tif_to_range(zonal_tif, interset_region, None, 'MAT',
                                                    assign_size=[im_height, im_width])

        # 当有多个图层时，只取第一个图层
        if im_bands > 1:
            input_raster_extent = input_raster_extent[0, :, :]

        # 获取 NoData 值，将 NoData 值区域赋值为 nan
        no_data = input_raster.GetRasterBand(1).GetNoDataValue()
        input_raster_extent[input_raster_extent == no_data] = np.nan
        # 得到统计结果
        result = {}
        for i in np.unique(zone_raster):

            if stastic_mode == 'MEAN':
                stastic_temp = np.nanmean(input_raster_extent[zone_raster == i])
            elif stastic_mode == 'MAX':
                stastic_temp = np.nanmax(input_raster_extent[zone_raster == i])
            elif stastic_mode == 'MIN':
                stastic_temp = np.nanmin(input_raster_extent[zone_raster == i])
            elif stastic_mode == 'COUNT':
                stastic_temp = np.sum(zone_raster == i) - np.sum(np.isnan(input_raster_extent[zone_raster == i]))
            else:
                return

            result[i] = stastic_temp

        # 根据返回类型，输出返回值
        if return_mode == 'DICT':
            return result
        elif return_mode == 'TIF':
            result_tif = np.ones(input_raster_extent) * np.nan
            for i in np.unique(zone_raster):
                result_tif[zone_raster == i] = result[i]
            return result_tif
        elif return_mode == 'MAT':
            result_mat = np.ones(input_raster_extent.shape) * np.nan
            for i in np.unique(zone_raster):
                result_mat[zone_raster == i] = result[i]

            # FIXME 这一步在后面的改进中可能显得重复
            result_mat[np.isnan(input_raster_extent)] = np.nan
            return result_mat

    @staticmethod
    def interpolation():
        """InterPolation，这个困扰我很长时间了，gdal是有插值的，但是在Python里面找不到，应该是没有"""

    # TODO 不同坐标系统之间不能进行运算


class OgrBase(object):
    """基础的矢量操作"""

    @staticmethod
    def get_spatial_ref(shp_path):
        """返回坐标文件"""
        ds = ogr.Open(shp_path)
        lyr = ds.GetLayer(0)
        spatial_ref = lyr.GetSpatialRef()
        ds.Destroy()
        return spatial_ref

    @staticmethod
    def get_field(shp_path, field_names='*', need_line=None):
        """
        获取 shp 属性表字段
        :param shp_path: shp 的路径，或者一个 datasourse； path, datasourse
        :param field_names: 需要获取的属性的名称; [str, str]
        :param need_line: 需要的行
        :return: [[]] , 二维的列表 or None
        """

        # gdal.SetConfigOption("SHAPE_ENCODING", "GBK")
        gdal.SetConfigOption("SHAPE_ENCODING", "")

        if isinstance(shp_path, ogr.DataSource):
            ds = shp_path
        else:
            ds = ogr.Open(shp_path)

        # 获取 layer
        lyr = ds.GetLayer()
        if not isinstance(lyr, ogr.Layer):
            return

        # 遍历图层中的 feature
        result = []
        if need_line: need_line = set(need_line)
        for fea_index, fea in enumerate(lyr):
            # 过滤掉不需要的行列
            if need_line:
                if fea_index not in need_line:
                    continue

            temp_result = []
            # 输出全部属性
            if field_names == "*" or field_names == ['*']:
                for each_name in fea.keys():
                    temp_result.append(fea.GetField(each_name))
            # 输出指定属性
            else:
                for each_name in field_names:
                    temp_result.append(fea.GetField(each_name))
            # 一组询记录插入到结果中
            result.append(temp_result)
        return result

    @staticmethod
    def shp_to_tif(shp_path, tif_path, cell_size, shp_attribute=None, return_mode='TIFF'):
        """
        矢量转栅格
        :param shp_path: 矢量路径
        :param tif_path: 栅格路径 or dataset
        :param cell_size: 栅格单元大小
        :param shp_attribute: 使用的矢量属性
        :param return_mode: 返回类型，return_mode = tif 生成 tif 文件， returen_mode = memory , 结果放在内存中
        :return: None or dataset
        """
        # FIXME 对于无效值是如何处理的？,现在的方法出来的无效值会被转为一定大小的值，这个很难弄
        ds = ogr.Open(shp_path, 0)
        lyr = ds.GetLayer(0)
        # 角点坐标
        lon, lat = lyr.GetExtent()[0], lyr.GetExtent()[3]
        # 自定义栅格的单位长宽
        pixel_width, pixel_height = cell_size, -cell_size
        # 获得仿射矩阵信息
        im_geotrans = [lon, pixel_width, 0.0, lat, 0.0, pixel_height]
        # 获得矢量的坐标系
        im_proj = str(lyr.GetSpatialRef())
        # 设置初始化矩阵
        im_width = abs(int((lyr.GetExtent()[1] - lyr.GetExtent()[0]) / pixel_width)) + 1
        im_height = abs(int((lyr.GetExtent()[3] - lyr.GetExtent()[2]) / pixel_height)) + 1
        # TODO 先读取属性类型，再初始化 dataset 格式，如果无属性 设置为 gdal.GDT_Byte
        if return_mode.upper() == 'TIFF':
            target_ds = gdal.GetDriverByName('GTiff').Create(tif_path, im_width, im_height, 1, gdal.GDT_Float32)
        elif return_mode.upper() == 'MEMORY':
            target_ds = gdal.GetDriverByName('MEM').Create('', im_width, im_height, 1, gdal.GDT_Float32)
        else:
            return
        # GeoTransform
        target_ds.SetGeoTransform(im_geotrans)
        # 设置坐标系
        target_ds.SetProjection(im_proj)
        # 获取第一个波段
        band = target_ds.GetRasterBand(1)
        # 保存数据
        band.FlushCache()
        # 矢量转栅格
        if shp_attribute:
            gdal.RasterizeLayer(target_ds, [1], lyr, options=["ATTRIBUTE={0}".format(str(shp_attribute))])
        else:
            gdal.RasterizeLayer(target_ds, [1], lyr)
        # 输出为 Memory
        if return_mode.upper() == 'MEMORY' and isinstance(target_ds, gdal.Dataset):
            return target_ds

    @staticmethod
    def get_envelope(shp_path, layer_index=0):
        """获取矢量的范围"""
        ds = ogr.Open(shp_path)
        lyr = ds.GetLayer(layer_index)
        left, right, bottom, top = lyr.GetExtent()
        return left, top, right, bottom

    @staticmethod
    def get_proj(proj_str="WGS84"):
        """返回需要的坐标系"""
        osrobj = osr.SpatialReference()
        osrobj.SetWellKnownGeogCS(proj_str)
        return osrobj

    # -----------------  测试用函数 ------------------
    @staticmethod
    def get_base_info(shp_path):
        """获得一些基础信息，只能在测试的时候用，在写通用函数的时候就不要用了"""
        if isinstance(shp_path, ogr.DataSource):
            ds = shp_path
        else:
            ds = ogr.Open(shp_path)

        if not isinstance(ds, ogr.DataSource):
            return

        lyr = ds.GetLayer()
        if not isinstance(lyr, ogr.Layer):
            return

        lyr_extent = lyr.GetExtent()
        lyr_spatial_ref = lyr.GetSpatialRef()
        fea_count = lyr.GetFeatureCount()

        result = {'lyr_extent': lyr_extent, 'lyr_spatial_ref': lyr_spatial_ref, 'fea_count': fea_count}

        return result

    @staticmethod
    def write_shp(feature, shp_type=ogr.wkbPolygon, im_proj=None, out_path=None):
        """写一个矢量"""
        # FIXME 完善矢量属性的写入

        drive = ogr.GetDriverByName("ESRI Shapefile")
        if not isinstance(drive, ogr.Driver):
            return

        # FIXME 第一个参数的名字在哪里是可以用到的？
        ds = drive.CreateDataSource(out_path)
        if not isinstance(ds, ogr.DataSource):
            return

        lyr = ds.CreateLayer('jokker', im_proj, shp_type)
        if not isinstance(lyr, ogr.Layer):
            return

        # lyr.SetFeature(feature)
        # FIXME 这边为什么不用 set 而是用 create
        lyr.CreateFeature(feature)

        # geom = ogr.CreateGeometryFromWkt("POLYGON ((1 2, 32 43, 5.4 65, 17 2.8,123 20, 1 2))")
        # if not isinstance(geom, ogr.Geometry):
        #     return

        # feat = ogr.Feature(lyr.GetLayerDefn())
        # if not isinstance(feat, ogr.Feature):
        #     return
        # feat.SetGeometry(geom)
        # lyr.CreateFeature(feat)
        ds.Destroy()


class OgrTools(object):

    @staticmethod
    def split(shp_path, attribute='fid', save_folder=None, return_mode='SHP'):
        """将 shp 按照属性进行 split"""
        ds = ogr.Open(shp_path)
        lyr = ds.GetLayer(0)
        im_proj = lyr.GetSpatialRef()
        # FIXME 需要支持点和线,需要先识别输入的 feature 的类型
        shp_type = ogr.wkbPolygon
        # 遍历 feature
        result = []
        for i in range(lyr.GetFeatureCount()):
            feature_temp = lyr.GetFeature(i)
            if attribute == 'fid':
                name = i
            else:
                name = str(feature_temp.GetField(attribute))

            if return_mode.upper() == 'SHP':
                out_path_temp = os.path.join(save_folder.strip('\\'), '{0}.shp'.format(name))
                driver_temp = ogr.GetDriverByName("ESRI Shapefile")
                ds_temp = driver_temp.CreateDataSource(out_path_temp)
                lyr_temp = ds_temp.CreateLayer('jokker', im_proj, shp_type)
                lyr_temp.CreateFeature(feature_temp)
                ds_temp.Destroy()
            elif return_mode.upper() == "MEMORY":
                driver_temp = ogr.GetDriverByName("Memory")
                ds_temp = driver_temp.CreateDataSource('')
                lyr_temp = ds_temp.CreateLayer('jokker', im_proj, shp_type)
                lyr_temp.CreateFeature(feature_temp)
                result.append(ds_temp)
            else:
                return
        logging.info('split success')
        # 返回结果
        if return_mode.upper() == 'MEMORY':
            return result

    @staticmethod
    def extract_points_values_in_tiff(tif_path, point_shp, info_field=None):
        """
        获取点在tif中对应位置的值
        :param tif_path: tif 文件路径，单波段
        :param point_shp: 点图层，
        :param info_field : 用于区分每个值对应的点
        :return: float OR int
        """
        # FIXME 这个函数设计有问题，需要好好的修改
        # --------------------------------------------------------------------------------------------------------------
        im_data, im_width, im_height, im_bands, im_geotrans, im_proj = GdalBase.read_tiff(tif_path)
        pixel_width, pixel_height = im_geotrans[1], im_geotrans[5]
        lon1, lat1, lon2, lat2 = GdalBase.get_envelope(tif_path)
        # --------------------------------------------------------------------------------------------------------------
        points_info = CreateOgr.convert_point_to_dict(point_shp)  # 解析点数据，得到点的坐标
        # 拿到点的坐标和区分各个点的信息
        points_info_need = map(lambda x: {'lon': x['lon'], 'lat': x['lat'], 'info_field': x[info_field]}, points_info)
        # --------------------------------------------------------------------------------------------------------------
        for each_point in points_info_need:
            # 拿到经纬度
            point_lon, point_lat = each_point['lon'], each_point['lat']
            # 判断点是否在范围内部
            if not (lon1 <= point_lon <= lon2 and lat2 <= point_lat <= lat1):
                logging.error('point isnot in assign region')
                each_point['value'] = None
                continue
            # 获取点所在栅格行列，返回栅格值
            offset_lon = point_lon - lon1
            offset_lat = point_lat - lat1
            offset_lon_cell = int(offset_lon / pixel_width)
            offset_lat_cell = int(offset_lat / pixel_height)
            # 返回栅格值在字典中的数据类型
            each_point['value'] = im_data[offset_lat_cell, offset_lon_cell]
        return points_info_need

    # -------------------------- need to perfect --------------------------------

    @staticmethod
    def point_buffer():
        """点的缓冲区"""
        pass

    @staticmethod
    def clip():
        """裁剪"""

        # FIXME 可用求并集的方式得到裁剪结果

    @staticmethod
    def union():
        """合并操作"""

    @staticmethod
    def intersection():
        """得到交集"""

        # 参考：http://pcjericks.github.io/py-gdalogr-cookbook/geometry.html#calculate-intersection-between-two-geometries

        from osgeo import ogr

        wkt1 = "POLYGON ((1208064.271243039 624154.6783778917, 1208064.271243039 601260.9785661874, 1231345.9998651114 601260.9785661874, 1231345.9998651114 624154.6783778917, 1208064.271243039 624154.6783778917))"
        wkt2 = "POLYGON ((1199915.6662253144 633079.3410163528, 1199915.6662253144 614453.958118695, 1219317.1067437078 614453.958118695, 1219317.1067437078 633079.3410163528, 1199915.6662253144 633079.3410163528)))"

        poly1 = ogr.CreateGeometryFromWkt(wkt1)
        poly2 = ogr.CreateGeometryFromWkt(wkt2)

        Intersection = poly1.Intersection(poly2)

        # print poly1
        # print poly2
        # print Intersection.ExportToWkt()

    @staticmethod
    def get_center_of_rect():
        """得到外接矩形的中心，如果中心不在多边形内部就返回内部的随机一个点"""
        pass


class CreateOgr(object):

    # FIXME 用标准的 GeoJson 进行转换，不过以我觉得好的数据结构作为中间数据结构，这样看着清晰一些

    @staticmethod
    def create_points_from_dict(point_info, save_path, proj_path=None, attr_type=None, lon_string='lon', lat_string='lat'):
        """
        从字典创建点数据"
        :param lat_string: 纬度所用的字符串
        :param lon_string: 经度所用的字符串
        :param point_info:  火点信息字典，其中 lon 和 lat 字段用于火点的坐标。和其他字段一起作为火点的属性， 用列表里面装字典比较合适
                                                        point_info = [{'lon': 123, 'lat': 12, 'area': 11, 'date': 'jokk'}]
        :param save_path:  保存的 shp 路径
        :param proj_path:  坐标文件路径
        :param attr_type:  指定文件的数据类型， dict,{'lon': 'int', 'date': 'string'}
        :return: None
        """

        # TODO 对数据进行过滤，改变输入的 字典的内容

        # 读取坐标系信息
        if proj_path is None:
            proj = OgrBase.get_proj("WGS84")
        elif isinstance(proj_path, str):
            ds = ogr.Open(proj_path)
            lyr = ds.GetLayer(0)
            proj = lyr.GetSpatialRef()
        elif isinstance(proj_path, osr.SpatialReference):
            proj = proj_path
        else:
            logging.error('has something wrong in proj_path')
            return

        # 试图解决中文的问题
        gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
        # gdal.SetConfigOption("SHAPE_ENCODING", "GBK")
        # 新建 驱动
        driver = ogr.GetDriverByName("ESRI Shapefile")
        # 新建 DataSourse
        newds = driver.CreateDataSource(save_path)
        # 新建 Layer ,我终于知道了，当传经来的是 folder 的时候 那个 'jokker' 就发挥作用了，作为文件名了
        layernew = newds.CreateLayer('fire_point', proj, ogr.wkbPoint)
        # 找到 title
        title = point_info[0].keys()
        # 定义所有的属性
        if attr_type:
            for each_attr in title:
                if each_attr not in attr_type:
                    fieldf = ogr.FieldDefn(each_attr, ogr.OFTString)
                elif attr_type[each_attr] == 'int':
                    fieldf = ogr.FieldDefn(each_attr, ogr.OFSTInt16)
                elif attr_type[each_attr] == 'string':
                    fieldf = ogr.FieldDefn(each_attr, ogr.OFTString)
                else:
                    raise TypeError
                layernew.CreateField(fieldf)

        else:
            for each_attr in title:
                fieldf = ogr.FieldDefn(each_attr, ogr.OFTString)
                layernew.CreateField(fieldf)

        # 新建点
        for point_index, point in enumerate(point_info):
            # 新建形状
            geom = ogr.Geometry(ogr.wkbPoint)
            # 获取经纬度信息
            lon = point[lon_string]
            lat = point[lat_string]
            geom.AddPoint(float(lon), float(lat))
            # 新建要素
            feat = ogr.Feature(layernew.GetLayerDefn())
            # 赋值属性
            for attr_index, each_attr in enumerate(title):
                feat.SetField(attr_index, point[each_attr])
            # 设置形状
            feat.SetGeometry(geom)
            # 设置要素
            layernew.CreateFeature(feat)

        # 释放内存，保存数据到本地
        newds.Destroy()
        logging.info('create_points_from_dict success')
        # 删除驱动，不然可能会报错，后来发现报错是因为覆盖了之前的矢量图层
        del driver

    @staticmethod
    def create_polyline_from_dict(line_info, save_path, proj_path=None, attr_type=None, lon_lat=True):
        """
        从字典创建线数据"
        :param line_info:  火点信息字典，其中 lon 和 lat 字段用于火点的坐标。和其他字段一起作为火点的属性， 用列表里面装字典比较合适
                                                        point_info = [{'points':(lon, lat), 'area': 11, 'date': 'jokk'}]
        :param save_path:  保存的 shp 路径
        :param proj_path:  坐标文件路径
        :param attr_type:  指定文件的数据类型， dict,{'lon': 'int', 'date': 'string'}
        :param lon_lat: 坐标点的顺序是指定先 lon 后 lat 则为 True，反之为 False
        :return: None
        """


        # 读取坐标系信息
        if proj_path is None:
            proj = OgrBase.get_proj("WGS84")
        elif isinstance(proj_path, str):
            ds = ogr.Open(proj_path)
            lyr = ds.GetLayer(0)
            proj = lyr.GetSpatialRef()
        elif isinstance(proj_path, osr.SpatialReference):
            proj = proj_path
        else:
            logging.error('has something wrong in proj_path')
            return

        # 新建 驱动
        driver = ogr.GetDriverByName("ESRI Shapefile")
        # 新建 DataSourse
        newds = driver.CreateDataSource(save_path)
        # 新建 Layer ,我终于知道了，当传经来的是 folder 的时候 那个 'jokker' 就发挥作用了，作为文件名了
        layernew = newds.CreateLayer('line', proj, ogr.wkbLineString)
        # 找到 title
        title = line_info[0].keys()
        # 定义所有的属性
        if attr_type:
            for each_attr in title:
                if each_attr not in attr_type:
                    fieldf = ogr.FieldDefn(each_attr, ogr.OFTString)
                elif attr_type[each_attr] == 'int':
                    fieldf = ogr.FieldDefn(each_attr, ogr.OFSTInt16)
                elif attr_type[each_attr] == 'string':
                    fieldf = ogr.FieldDefn(each_attr, ogr.OFTString)
                else:
                    raise TypeError
                layernew.CreateField(fieldf)

        else:

            for each_attr in title:
                if each_attr == u'points' or each_attr == 'points':
                    continue
                fieldf = ogr.FieldDefn(each_attr, ogr.OFTString)
                layernew.CreateField(fieldf)

        # 新建线图层
        for line_index, polyline in enumerate(line_info):
            # 新建形状
            geom = ogr.Geometry(ogr.wkbLineString)
            # 遍历里面每个点
            for each_point in polyline['points']:
                if lon_lat:
                    geom.AddPoint(float(each_point[0]), float(each_point[1]))
                else:
                    geom.AddPoint(float(each_point[1]), float(each_point[0]))

            # 新建要素
            feat = ogr.Feature(layernew.GetLayerDefn())
            # 赋值属性
            attr_index = 0
            for each_attr in title:
                # FIXME point 属性指定为存放线中点的位置
                if each_attr == u'points' or each_attr == 'points':
                    continue
                feat.SetField(attr_index, polyline[each_attr])
                attr_index += 1
            # 设置形状
            feat.SetGeometry(geom)
            # 设置要素
            layernew.CreateFeature(feat)

        # 释放内存，保存数据到本地
        logging.info('create_polyline_from_dict success')
        newds.Destroy()
        del driver

    @staticmethod
    def create_polygon_from_dict(line_info, save_path, proj_path=None, attr_type=None, lon_lat=True):
        """
        从字典创建面数据"
        :param line_info:  火点信息字典，其中 lon 和 lat 字段用于火点的坐标。和其他字段一起作为火点的属性， 用列表里面装字典比较合适
                                                        point_info = [{'points':(lon, lat), 'area': 11, 'date': 'jokk'}]
        :param save_path:  保存的 shp 路径
        :param proj_path:  坐标文件路径
        :param attr_type:  指定文件的数据类型， dict,{'lon': 'int', 'date': 'string'}
        :param lon_lat: 坐标点的顺序是指定先 lon 后 lat 则为 True，反之为 False
        :return: None
        """

        # 读取坐标系信息
        if proj_path is None:
            proj = OgrBase.get_proj("WGS84")
        elif isinstance(proj_path, str):
            ds = ogr.Open(proj_path)
            lyr = ds.GetLayer(0)
            proj = lyr.GetSpatialRef()
        elif isinstance(proj_path, osr.SpatialReference):
            proj = proj_path
        else:
            logging.error('has something wrong in proj_path')
            return

        # 新建 驱动
        driver = ogr.GetDriverByName("ESRI Shapefile")
        # 新建 DataSourse
        newds = driver.CreateDataSource(save_path)
        # 新建 Layer ,我终于知道了，当传经来的是 folder 的时候 那个 'jokker' 就发挥作用了，作为文件名了
        layernew = newds.CreateLayer('polygon', proj, ogr.wkbMultiPolygon)
        # 找到 title
        title = line_info[0].keys()
        # 定义所有的属性
        if attr_type:
            for each_attr in title:
                if each_attr not in attr_type:
                    fieldf = ogr.FieldDefn(each_attr, ogr.OFTString)
                elif attr_type[each_attr] == 'int':
                    fieldf = ogr.FieldDefn(each_attr, ogr.OFSTInt16)
                elif attr_type[each_attr] == 'string':
                    fieldf = ogr.FieldDefn(each_attr, ogr.OFTString)
                else:
                    raise TypeError
                layernew.CreateField(fieldf)

        else:

            for each_attr in title:
                if each_attr == u'points' or each_attr == 'points':
                    continue
                fieldf = ogr.FieldDefn(each_attr, ogr.OFTString)
                layernew.CreateField(fieldf)

        # 新建线图层
        for line_index, polyline in enumerate(line_info):
            # 新建形状
            ring = ogr.Geometry(ogr.wkbLinearRing)
            # 遍历里面每个点
            for each_point in polyline['points']:
                if lon_lat:
                    ring.AddPoint(float(each_point[0]), float(each_point[1]))
                else:
                    ring.AddPoint(float(each_point[1]), float(each_point[0]))
            geom = ogr.Geometry(ogr.wkbPolygon)
            geom.AddGeometry(ring)
            # 新建要素
            feat = ogr.Feature(layernew.GetLayerDefn())
            # 赋值属性
            attr_index = 0
            for each_attr in title:
                # FIXME point 属性指定为存放线中点的位置
                if each_attr == u'points' or each_attr == 'points':
                    continue
                feat.SetField(attr_index, polyline[each_attr])
                attr_index += 1
            # 设置形状
            feat.SetGeometry(geom)
            # 设置要素
            layernew.CreateFeature(feat)

        # 释放内存，保存数据到本地
        logging.info('create_polygon_from_dict')
        newds.Destroy()
        del driver

    @staticmethod
    def convert_point_to_dict(point_shp):
        """将点转为属性字典"""

        gdal.SetConfigOption("SHAPE_ENCODING", "CP936")

        # TODO 指定需要提取的属性

        point_info = []
        ds = ogr.Open(point_shp)
        lyr = ds.GetLayer(0)

        for fea_index, fea in enumerate(lyr):
            attr_dict = {}
            geo = fea.GetGeometryRef()
            attr_dict['lon'] = geo.GetX()
            attr_dict['lat'] = geo.GetY()
            # 遍历属性
            for each_attr in fea.keys():
                attr_dict[str(each_attr)] = fea.GetField(each_attr)

            point_info.append(attr_dict)
        logging.info('convert_point_to_dict success')
        return point_info

    # -------------------------------- 从要素创建要素 ------------------------------------------------------------

    @staticmethod
    def convert_polyline_to_dict(polyline_shp):
        """将线矢量转为字典"""

        gdal.SetConfigOption("SHAPE_ENCODING", "CP936")

        polyline_info = []
        ds = ogr.Open(polyline_shp)
        lyr = ds.GetLayer(0)

        for fea_index, fea in enumerate(lyr):
            attr_dict = {}
            # 读取形态信息
            geo = fea.GetGeometryRef()
            attr_dict['points'] = geo.GetPoints()
            # 读取属性信息
            for each_attr in fea.keys():
                attr_dict[str(each_attr)] = fea.GetField(each_attr)
            polyline_info.append(attr_dict)

        return polyline_info

    @staticmethod
    def convert_polygon_to_dict(polygon_shp):
        """将矢量面转为字典"""
        gdal.SetConfigOption("SHAPE_ENCODING", "CP936")

        polygon_info = []
        ds = ogr.Open(polygon_shp)
        lyr = ds.GetLayer(0)

        for fea_index, fea in enumerate(lyr):
            attr_dict = {}
            # 读取形态信息
            geo = fea.GetGeometryRef()
            # FIXME 这边提取的第一个是第一个图层还是什么？
            # FIXME 用下面的方法拿出来的数据是不规则的，有的是三个嵌套有的是两个，这个需要好好看看 polygon 的格式标准
            # attr_dict['points'] = json.loads(geo.ExportToJson())['coordinates'][0]
            attr_dict['points'] = geo.GetGeometryRef(0).GetPoints()
            # 读取属性信息
            for each_attr in fea.keys():
                attr_dict[str(each_attr)] = fea.GetField(each_attr)
            polygon_info.append(attr_dict)
        return polygon_info

    @staticmethod
    def convert_point_to_df():
        """将点转为 DataFrame"""
        pass

    @staticmethod
    def create_point_from_df():
        """从 DataFrame 创建点"""
        pass

    @staticmethod
    def merge_point():
        """多个点图层进行合并"""
        pass

    @staticmethod
    def merge_feature():
        """合并要素"""


class Others(object):

    @staticmethod
    def reclassify(input_mat, grade):
        """
        根据等级数据进行重分类，适用于级别比较少的情况，大于等于 grade 第一个元素是 第一级别，小于 grade 第一个元素是第 0 级别
        :param input_mat: 输入矩阵，np.ndarray
        :param grade: 分类等级，list
        :return: np.ndarray / None
        """
        # FIXME 对于级别比较多的情况，需要重新写一个算法，因为每一次判断就是一次遍历
        # 数据是否符合类型
        if not (isinstance(input_mat, np.ndarray) and isinstance(grade, list)):
            return
        # 排序等级信息
        grade.sort()
        # 初始等级都为 0 级
        result_mat = np.zeros(input_mat.shape).astype(np.int64)
        for now_calss, value_temp in enumerate(grade):
            result_mat[input_mat >= value_temp] = now_calss + 1
        return result_mat

    @staticmethod
    def distance_between_points():
        """计算点和点之间的距离"""
        # FIXME 使用 Python 数据科学手册 P81 里面的方法，看看能不能赶上 Arcpy 中的方法

    @staticmethod
    def point_inorout_polygon(nvert, vertx, verty, testx, testy):
        """点是否在多边形内部"""
        i, j, crossings = 0, nvert-1, 0
        for i in range(nvert):
            if ((vertx[i] > testx) != (vertx[j] > testx)) and (testx > (vertx[j]-vertx[i]) * (testy - verty[i]) / (verty[j] - verty[i]) + vertx[i]):
                crossings += 1
            j += 1
        return crossings % 2 != 0

    @staticmethod
    def mm_synthesis_diff_extent(tif_dirs, result_com_path, nan_symbol, mode, value_min, value_max):
        """忽略范围的最大最小值合成"""
        tif_list = map(lambda x: os.path.join(tif_dirs, x), os.listdir(tif_dirs))
        # 得到所有文件的范围并集
        merge_region = GdalTools.merge_region(tif_list)
        # 将所有文件拉伸到并集范围
        tif_extent_paths = []
        for each_tif in tif_list:
            tif_extent_paths.append(GdalTools.extent_tif_to_range(each_tif, merge_region,
                                                       save_path=None, return_mode='MEMORY', assign_size=(2685,1800)))
        # 合成
        GdalTools.mm_synthesis(tif_extent_paths, result_com_path, nan_symbol, mode, value_min, value_max)


if __name__ == '__main__':

    # grib_path = r'C:\Users\Administrator\Desktop\依赖注入\9bc215de_7b7c_11e9_b011_005056af2564U_Wind.tif'
    grib_path = r'C:\Users\Administrator\Desktop\del\Z_NWGD_C_BEXN_20190518051428_P_RFFC_SPCC-EDA10_201905180800_24003.GRB2'

    a = gdal.Open(grib_path)

    im_data, im_width, im_height, im_bands, im_geotrans, im_proj = GdalBase.read_tiff(grib_path)

    print(a)

