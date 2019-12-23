# -*- coding: utf-8  -*-
# -*- author: jokker -*-

# FIXME 坐标转换，这个之前还没实现，现在的处理都是基于 WGS84 等度为单位的投影来做的，其他的做不了
# FIXME 学习 gdal 中 sql 语句的使用
# FIXME 将各种实现的方案整理一下，写好各个方案的优缺点，
# FIXME 将 gdal 版本的各个函数里面的各个参数的意思翻译一遍，整理一个文档
# FIXME 完善文件管理，比较好的删除和整理 tiff 和 shp 文件，用 gdal 的文件管理器比较好
# FIXME 重要的是基础函数
# FIXME 在工作中不需要考虑到多波段的文件的处理，所以多有的函数可以选择不支持多波段文件的操作


import gdal
import ogr
import osr
import numpy as np
import logging
import uuid
import os
import shutil
from Report.ArcpyOsgeoUtil import ArcpyOsgeoUtil
from collections import Counter
from Algo.BFS.GetPlaque import GetPlaque
from skimage import measure


class ArcpyGdalUtil(object):

    def __init__(self, temp_dir):
        # 临时文件夹
        self.temp_dir = temp_dir
        # 输出范围
        self.output_bounds = None
        # 分辨率
        self.cell_size = None

    @staticmethod
    def shp_to_raster(src_ds, out_tiff_path: str = '', output_bounds=None, no_data_value=None, attribute=None,
                      cell_size: (list, tuple) = None, output_type=gdal.GDT_Unknown, res_format='GTiff'):
        """
        矢量转栅格
        :param src_ds: shp 路径
        :param out_tiff_path:  输出的 tiff 路径, 输入 '' 就是不需要输出路径
        :param output_bounds:  输出范围,[ulx, uly, lrx, lry], 左下角点经纬度，右上角点经纬度
        :param no_data_value:  无效值设置
        :param attribute:  栅格化时使用的矢量字段，需要是数值类型字段
        :param cell_size:  单元格大小
        :param output_type:
        :param res_format: 输出的模式， "GTiff"
        :return:
        """
        # FIXME 当输出为 MEM 类型时，无效值（no_data_value）的设置不起作用，看看是不是哪里想错了
        # ------------------------------------------------------------------------------------------------------------------
        if cell_size:
            x_res, y_res = cell_size[0], cell_size[1]
        else:
            raise ValueError('cell size is needed')
        # ------------------------------------------------------------------------------------------------------------------
        rasterize_options = gdal.RasterizeOptions(outputBounds=output_bounds, outputType=output_type,
                                                  noData=no_data_value, attribute=attribute, useZ=False, xRes=x_res,
                                                  yRes=y_res, format=res_format)

        return gdal.Rasterize(out_tiff_path, src_ds, options=rasterize_options)  # 转栅格

    # --------------------------------- 设置更新 -----------------------------
    @staticmethod
    def set_no_data_region_by_mask(tiff_path, mask: np.ndarray, assign_band_index: (list, tuple, str) = '*',
                                   out_tiff_path: str = None, assign_no_data_value: (int, float) = None):
        """
        设置无效值掩膜
        :param tiff_path:  输入数据
        :param mask:   使用的掩膜，0 代表需要被设置为无效值的区域，1代表保留原值
        :param assign_band_index:   指定的需要被设置的图层，* 所有的图层
        :param out_tiff_path:  不为空：不在当前文件上进行修改，为空，在当前文件上进行修改
        :param assign_no_data_value:  指定无效值
        :return:
        """
        # 这边的顺序不能变，因为获取无效值是以只读模式打开的文件
        if out_tiff_path:
            if assign_no_data_value is not None:
                ArcpyGdalUtil.set_no_data_value(tiff_path, assign_no_data_value,
                                                out_tiff_path=out_tiff_path)  # 当指定无效值，将原数据无效值进行改变
                ds = gdal.Open(out_tiff_path, gdal.GA_Update)
            else:
                gdal.GetDriverByName('Gtiff').CopyFiles(out_tiff_path, tiff_path)
                ds = gdal.Open(out_tiff_path, gdal.GA_Update)
        else:
            if assign_no_data_value is not None:
                ds = ArcpyGdalUtil.set_no_data_value(out_tiff_path, assign_no_data_value, res_format='MEM')
                ds = gdal.Open(ds, gdal.GA_Update)
            else:
                ds = gdal.Open(tiff_path, gdal.GA_Update)

        im_band = ds.RasterCount  # 获取波段数
        no_data_value = ArcpyGdalUtil.get_no_data_value(ds)  # 无效值
        im_width = ds.RasterXSize  # 列数
        im_height = ds.RasterYSize  # 行数
        array_data = ds.ReadAsArray(0, 0, im_width, im_height)

        if assign_band_index == '*':
            assign_band_index = list(range(im_band))  # 改变所有的波段

        if im_band == 1:
            if no_data_value[0] is None and assign_no_data_value is None:
                raise ValueError('when tiff dont have no data value, assign_no_data_value cant be empty')
            assign_no_data_value = no_data_value[0]
            array_data[mask == 0] = assign_no_data_value  # 第一个波段的无效值
            ds.GetRasterBand(1).WriteArray(array_data)
        else:
            for i in assign_band_index:
                array_data[mask == 0] = no_data_value[i]
                ds.GetRasterBand(1).WriteArray(array_data)

    @staticmethod
    def set_no_data_region_by_fun():
        """根据传入的方法设定无效值范围，方法的输入参数是 array，输出是布尔值的矩阵"""

    @staticmethod
    def set_no_data_value(tiff_path, no_data_value, res_format='GTiff', out_tiff_path: str = ''):
        """设置 tiff 的无效值, 原来的无效值还是无效值，同时设置新的无效值, 可以返回 dataset 或 改变保存至文件"""

        # FIXME 可以使用更新模式来做，这样就可以将变化更新到源文件上去

        warp_option = gdal.WarpOptions(format=res_format, dstNodata=no_data_value)
        return gdal.Warp(out_tiff_path, tiff_path, options=warp_option)

    @staticmethod
    def set_array_data(tiff_path, array_data: np.ndarray, assign_band_index: (list, tuple, str) = '*',
                       out_tiff_path: str = None):
        """
        更新值矩阵，可以指定波段，也可以更新全部波段
        :param tiff_path:  输入 tiff
        :param array_data: 更新的 矩阵
        :param assign_band_index:  指定更新的波段，设置为 * 更新全部波段
        :param out_tiff_path: 不为空：不在当前文件上进行修改，为空，在当前文件上进行修改
        :return:
        """
        if out_tiff_path:
            gdal.GetDriverByName('Gtiff').CopyFiles(out_tiff_path, tiff_path)
            ds = gdal.Open(out_tiff_path, gdal.GA_Update)  # 设置为更新模式，就能进行更新了，而不需要重新创建
        else:
            ds = gdal.Open(tiff_path, gdal.GA_Update)  # 设置为更新模式，就能进行更新了，而不需要重新创建

        im_band = ds.RasterCount  # 获取波段数

        if assign_band_index == '*':
            assign_band_index = list(range(im_band))  # 设置需要改变的是所有的波段

        if im_band == 1:
            ds.GetRasterBand(1).WriteArray(array_data)
        elif assign_band_index and im_band > 1:
            if array_data.ndim == 3:
                for i in assign_band_index:
                    ds.GetRasterBand(i + 1).WriteArray(array_data[i, :, :])
            elif array_data.ndim == 2:
                for i in assign_band_index:
                    ds.GetRasterBand(i + 1).WriteArray(array_data)
            else:
                raise ValueError('array ndim can only be 2 or 3')

    @staticmethod
    def set_array_data_use_assign_algo(tiff_path, func, assign_band_index: (list, tuple, str) = '*',
                                       out_tiff_path: str = None):
        """
        通过传入的方法体对 tiff 进行更新
        :param tiff_path:
        :param func:   传入的方法
        :param assign_band_index:  需要改变的图层，* 代表更新所有图层
        :param out_tiff_path:  不为空，输出为新文件，为空，更新传入的文件
        :return:
        """
        # FIXME 给方法提供默认的参数，cookbook 里面有介绍

        if out_tiff_path:
            gdal.GetDriverByName('Gtiff').CopyFiles(out_tiff_path, tiff_path)
            ds = gdal.Open(out_tiff_path, gdal.GA_Update)  # 设置为更新模式
        else:
            ds = gdal.Open(tiff_path, gdal.GA_Update)

        im_band = ds.RasterCount  # 波段数
        im_width = ds.RasterXSize  # 列数
        im_height = ds.RasterYSize  # 行数
        array_data = ds.ReadAsArray(0, 0, im_width, im_height)

        if assign_band_index == '*':
            assign_band_index = list(range(im_band))  # 改变所有的波段

        if im_band == 1:
            ds.GetRasterBand(1).WriteArray(func(array_data))
        else:
            for i in assign_band_index:
                ds.GetRasterBand(i + 1).WriteArray(func(array_data[i, :, :]))

    @staticmethod
    def set_data_type(tiff_path, tiff_out, out_type, res_format: str = 'GTiff'):
        """
        改变数据类型
        :param tiff_path:
        :param tiff_out:
        :param out_type:  输出数据类型，如 gdal.GDT_Float64
        :param res_format:   返回类型， GTiff 输出为文件， MEM 输出为临时文件
        :return:
        """
        translate_options = gdal.TranslateOptions(outputType=out_type, format=res_format)
        return gdal.Translate(tiff_out, tiff_path, options=translate_options)

    # ---------------------------------- tiff 范围 ----------------------------
    @staticmethod
    def get_tiff_envelope(tif_path, mode='output_bounds'):
        """
        获取包络矩形范围
        :param tif_path:
        :param mode: 返回范围的模式，不同的模式，返回的顺序不一样
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

        if mode == 'output_bounds':
            return left, bottom, right, top
        elif mode == 'lrbt':
            return left, right, bottom, top

        return left, bottom, right, top

    @staticmethod
    def get_shp_envelope(shp_path, layer_index=0, mode='output_bounds'):
        """
        获取矢量的范围
        :param shp_path:  shp 路径
        :param layer_index:  图层的序号
        :param mode:
        :return:
        """
        ds = ogr.Open(shp_path)
        lyr = ds.GetLayer(layer_index)
        left, right, bottom, top = lyr.GetExtent()

        if mode == 'output_bounds':
            return left, bottom, right, top
        elif mode == 'lrbt':
            return left, right, bottom, top

        return left, bottom, right, top

    @staticmethod
    def envelope_intersection(envelopes_list: (list, tuple), mode='output_bounds'):
        """
        获取范围的交集
        :param envelopes_list:  范围列表
        :param mode:
        :return:
        """
        left, right, bottom, top = -np.inf, np.inf, -np.inf, np.inf

        for each_envelope in envelopes_list:
            left = max(left, each_envelope[0])
            bottom = max(bottom, each_envelope[1])
            right = min(right, each_envelope[2])
            top = min(top, each_envelope[3])

        if mode == 'output_bounds':
            return left, bottom, right, top

        return left, bottom, right, top

    @staticmethod
    def envelope_union(envelopes_list, mode='output_bounds'):
        """
        获取范围的并集
        :param envelopes_list:  范围列表
        :param mode:
        :return:
        """
        left, right, bottom, top = np.inf, -np.inf, np.inf, -np.inf

        for each_envelope in envelopes_list:
            left = min(left, each_envelope[0])
            bottom = min(bottom, each_envelope[1])
            right = max(right, each_envelope[2])
            top = max(top, each_envelope[3])

        if mode == 'output_bounds':
            return left, bottom, right, top
        return left, bottom, right, top

    # ---------------------------------- 属性获取 ----------------------------
    @staticmethod
    def get_no_data_value(tiff_path: (str, gdal.Dataset)):
        """
        获取无效值
        :param tiff_path:
        :return: 无效值列表 [None, 1, 2]
        """
        # 检查输入类型
        if isinstance(tiff_path, gdal.Dataset):
            ds = tiff_path
        else:
            ds = gdal.Open(tiff_path)
        # 遍历获取无效值
        no_data_values = []
        for i in range(1, ds.RasterCount + 1):
            band_temp = ds.GetRasterBand(i)
            no_data_values.append(band_temp.GetNoDataValue())
        del ds
        return no_data_values

    @staticmethod
    def get_geotransform_info(tif_path: (str, gdal.Dataset)):
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
    def get_tiff_infomation(tiff_path: (str, gdal.Dataset), options: (list, tuple), return_mode: str = 'dict'):
        """
        获取数据信息，多种返回结构（字典，列表），只获取需要返回的值
        :param tiff_path:
        :param options: 需要获取的信息列表，['width', 'data']
        :param return_mode:  返回结果类型，字典或者列表
        :return:
        """
        info_dict = {}
        if options == '*':
            options = {'width', 'height', 'bands', 'proj', 'data', 'geotrans', 'pixel_width', 'pixel_height', 'lon',
                       'lat'}

        # 参数类型检查
        if isinstance(tiff_path, gdal.Dataset):
            dataset = tiff_path
        else:
            dataset = gdal.Open(tiff_path)

        if dataset:
            info_dict['width'] = dataset.RasterXSize  # 栅格矩阵的列数
            info_dict['height'] = dataset.RasterYSize  # 栅格矩阵的行数
            info_dict['bands'] = dataset.RasterCount  # 波段数
            info_dict['proj'] = dataset.GetProjection()  # 获取投影信息
            info_dict['geotrans'] = dataset.GetGeoTransform()  # 获取仿射矩阵信息
            info_dict['pixel_width'], info_dict['pixel_height'] = abs(info_dict['geotrans'][1]), abs(
                info_dict['geotrans'][5])  # pixel_height是负值（important）
            info_dict['lon'], info_dict['lat'] = info_dict['geotrans'][0], info_dict['geotrans'][3]
            if 'data' in options:
                info_dict['data'] = dataset.ReadAsArray(0, 0, info_dict['width'], info_dict['height'])  # 获取数据

        if return_mode == 'dict':
            res = {}
            for each_opt in options:
                res[each_opt] = info_dict[each_opt]
            return res
        elif return_mode == 'list':
            res = []
            for each_opt in options:
                res.append(info_dict[each_opt])
            return res

    @staticmethod
    def get_proj(proj_str='WGS84'):
        """
        返回栅格坐标系
        :param proj_str: 坐标系对应的名字
        :return:
        """
        osrobj = osr.SpatialReference()
        osrobj.SetWellKnownGeogCS(proj_str)
        return str(osrobj)

    @staticmethod
    def get_dataset_color_info(input_path):
        """
        将dataset中的color信息读取到字典中去
        :param input_path:
        :return:
        """

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
    def get_block(tiff_path, assign_length):
        """使用生成器来解决切片的问题
        # 两种调用方法
        # （1）for i in get_block()
        # （2）a = get_block() ; next(a); try 语句捕获异常
        """
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
                yield im_data
    # -------------------------------------------------------------------------
    @staticmethod
    def tiff_to_shp(tiff_path, shp_path, proj=None):
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
        # 获取坐标
        if proj is None:
            proj = osr.SpatialReference()
            proj.SetWellKnownGeogCS("WGS84")

        # create output file name
        output_shapefile = shp_driver.CreateDataSource(shp_path)
        new_shapefile = output_shapefile.CreateLayer(shp_path[:-4], proj)
        gdal.Polygonize(input_band, None, new_shapefile, -1, [], callback=None)
        # 当输入格式是 float 需要用下面一个函数
        # gdal.FPolygonize(input_band, None, new_shapefile, -1, [], callback=None, )
        new_shapefile.SyncToDisk()
        logging.info('tiff_to_shp success')

    @staticmethod
    def interpolation(shp_path, out_tiff_path, z_field='value', method='idw', cell_size=None, output_bounds=None,
                      algo_str=None, outputType=None, res_format: str = 'GTiff'):
        """
        插值，反距离加权（idw），最邻近（nearest），移动均值（average）
        :param shp_path: 用于插值的点 shp 路径
        :param out_tiff_path: 输出的 tiff 路径
        :param z_field:  插值使用的字段
        :param method:  插值方法
        :param cell_size:  插值后的 tiff 的分辨率
        :param output_bounds:  插值输出范围(x_min, y_min, x_max, y_max)
        :param algo_str: 算法参数设置
        :param outputType: 输出数据类型，如 gdal.GDT_Float64
        :param res_format: 返回类型， GTiff 输出为文件， MEM 输出为临时文件
        :return: None
        """
        # ------------------------------------------------------------------------------------------------------------------
        # 算法描述字符串
        if method == 'idw' and algo_str is None:
            algo_str = "invdist:power=2.0:smoothing=0.0:radius1=0.0:radius2=0.0:angle=0.0:" \
                       "max_points=0:min_points=0:nodata=0.0"
        elif method == 'average' and algo_str is None:
            # algo_str = "average:radius1=0.0:radius2=0.0:angle=0.0:min_points=0:nodata=0.0"
            raise TypeError('not support yet')
        elif method == 'nearest':
            # algo_str = "minimum={0}:maximum={1}:range={2}:count={3}:average_distance={4}:average_distance_pts={5}"
            raise TypeError('not support yet')
        elif method in ['idw', 'average', 'nearest']:
            algo_str = algo_str
        else:
            raise ValueError('method can only be : idw | average | nearest')
        # ------------------------------------------------------------------------------------------------------------------
        # 根据 cell_size 得到长宽
        if cell_size is None:
            width, height = None, None
        else:
            if output_bounds:
                x_min, y_min, x_max, y_max = output_bounds
                width, height = int((x_max - x_min) / float(cell_size)), int((y_max - y_min) / float(cell_size))
            else:
                # width, height = None, None   # 获取 point 的范围，得到当前点的范围
                raise ValueError('warning : 当未输入 outputBounds 时，cell_size 的设置无效')
        # ------------------------------------------------------------------------------------------------------------------
        grid_option = gdal.GridOptions(algorithm=algo_str, zfield=z_field, outputBounds=output_bounds, width=width,
                                       height=height, outputType=outputType, format=res_format)  # 设置算法和插值所用的字段

        gdal.Grid(out_tiff_path, shp_path, options=grid_option)  # 插值

    @staticmethod
    def extend_tiff_to_range(tiff_path, out_tiff_path, output_bounds, res_format='GTiff'):
        """
        将 tiff 扩展到需要的范围
        :param tiff_path:   输入 tiff
        :param out_tiff_path:  输出 tiff
        :param output_bounds:  输出的 tiff 范围
        :param res_format: 返回的形式， 'GTiff':'tiff' ， 'MEM': 内存
        :return:
        """
        warp_option = gdal.WarpOptions(outputBounds=output_bounds, format=res_format)
        return gdal.Warp(out_tiff_path, tiff_path, options=warp_option)

    @staticmethod
    def resample_tiff(tiff_path, out_tiff_path: str, cell_size: (int, float, list, tuple), resample_algo: str = 'near',
                      res_format: str = 'GTiff'):
        """
        重采样
        :param tiff_path: 输入 tiff
        :param out_tiff_path: 输出 tiff
        :param cell_size: 像元大小
        :param resample_algo: 重采样方法 near, cubic, bilinear 等
        :param res_format: 返回类型， GTiff 输出为文件， MEM 输出为临时文件
        :return:
        """

        if isinstance(cell_size, int) or isinstance(cell_size, float):
            xy_res = (cell_size, cell_size)
        else:
            xy_res = cell_size

        translate_option = gdal.TranslateOptions(xRes=xy_res[0], yRes=xy_res[1], resampleAlg=resample_algo,
                                                 format=res_format)
        return gdal.Translate(out_tiff_path, tiff_path, options=translate_option)

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
        im_width, im_height, im_bands, im_geotrans, im_proj = ArcpyGdalUtil.read_tiff(tif_paths[0])[1:]
        # 计数器
        com_index = np.zeros((im_height, im_width))
        # 总和
        com_result_temp = np.zeros((im_height, im_width))
        # 无值区
        nan_data_temp = np.zeros((im_height, im_width))

        for eachTifPath in tif_paths:
            # 读取 tif 矩阵
            data_mat = ArcpyGdalUtil.read_tiff(eachTifPath)[0]
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
        ArcpyGdalUtil.write_tiff(com_result, im_width, im_height, im_bands, im_geotrans, im_proj, result_com_path,
                                 no_data_value=nan_symbol)
        logging.info('mean_synthesis success')

    @staticmethod
    def extract_by_mask(in_tiff_path, shp_path: str, out_tiff_path: str = '', no_data_value: (int, float) = None,
                        crop_to_cutline: bool = True, res_format: str = 'GTiff'):
        """
        按掩膜提取
        :param in_tiff_path:  被掩膜的 tiff
        :param shp_path:  用于掩膜的 shp
        :param out_tiff_path: 输出路径，如果输出路径设置为 '' 则输出 MEM 模式（临时文件）
        :param no_data_value:  输出 dataset 的无效值，当 输入的 tiff 无无效值时，需要进行设置
        :param crop_to_cutline:  使用 shp 的范围作为输出 tiff 的范围，否则使用原 tiff 的范围作为输出范围（可以使用两者的交集范围，待完善）
        :param res_format:   返回类型， GTiff 输出为文件， MEM 输出为临时文件
        :return:
        """
        # FIXME 增加输出结果为 tiff 和 shp 范围的交集的功能

        warp_options = gdal.WarpOptions(cutlineDSName=shp_path, dstNodata=no_data_value, format=res_format,
                                        cropToCutline=crop_to_cutline)
        return gdal.Warp(out_tiff_path, in_tiff_path, options=warp_options)

    def zonal_stastic(self, tiff_path, shp_path, grade, field_name):
        """
        分区统计，分级分区统计
        :param tiff_path:
        :param shp_path:
        :param grade:  等级信息 [a, b, c, d] --> （a, b） (b, c) (c, d)
        :param field_name:  shp 中用于统计的字段名
        :return:
        """

        """
        解决的问题
        （1）一个区域完全是无效值报错
        （2）统计速度太慢
        """
        # TODO 需要对属性表中重复的区域进行合并，这个就需要设置得到统计值的时候有合并功能，而不是全部是替换
        # TODO 两个方案（1）将范围限制为 tiff 和 shp 的交集 （2）将范围限制为 shp 的范围

        # TODO 直接用 extract_by_mask 输出为 shp 范围即可，这样不会受到坐标系统的限制

        ArcpyOsgeoUtil.add_object_index(shp_path, 'obj_ID')  # 设置一个 和 FID 一直的 field 类型为 int
        obj_id_field_name_dict = dict(
            ArcpyOsgeoUtil.get_field(shp_path, ['obj_ID', field_name]))  # 获取需要统计的字段和 对象 ID 之间的映射关系
        # --------------------------------------------------------------------------------------------------------------
        # 获取 tiff 与 shp 范围交集
        cell_size = ArcpyGdalUtil.get_tiff_infomation(tiff_path, options=['pixel_width', 'pixel_height'],
                                                      return_mode='list')
        tiff_envelope = ArcpyGdalUtil.get_tiff_envelope(tiff_path)
        shp_envelope = ArcpyGdalUtil.get_shp_envelope(shp_path)
        # envelope = ArcpyGdalUtil.envelope_intersection([tiff_envelope, shp_envelope]) # 使用交集
        envelope = shp_envelope  # 使用 shp 范围

        tiff_clip2envelope = ArcpyGdalUtil.extend_tiff_to_range(tiff_path, '', output_bounds=envelope,
                                                                res_format='MEM')  # 裁剪被统计 tiff 至范围交集

        # FIXME 这边的无效值为什么突然没用了，使用临时文件模式，那么无效值就不能自定义，只有保存为文件，才能设置无效值，很奇怪
        tiff_from_shp = os.path.join(self.temp_dir, 'tiff_from_shp_{0}.tif'.format(str(uuid.uuid1())))
        ArcpyGdalUtil.shp_to_raster(shp_path, tiff_from_shp, cell_size=cell_size, attribute='obj_ID',
                                    output_type=gdal.GDT_UInt16, no_data_value=32767)  # res_format='MEM'

        # tiff_from_shp = ArcpyGdalUtil.shp_to_raster(shp_path, '', cell_size=cell_size, attribute='obj_ID',
        # output_type=gdal.GDT_UInt16, no_data_value=32767, res_format='MEM')  #

        shp_tiff_clip2envelope = ArcpyGdalUtil.extend_tiff_to_range(tiff_from_shp, '', output_bounds=envelope,
                                                                    res_format='MEM')  # 分区 tiff 裁剪至交集
        # --------------------------------------------------------------------------------------------------------------
        be_stastic_data = ArcpyGdalUtil.get_tiff_infomation(tiff_clip2envelope, ['data'], return_mode='dict')['data']
        region_data = ArcpyGdalUtil.get_tiff_infomation(shp_tiff_clip2envelope, ['data'], return_mode='dict')['data']

        res_region, res_region_class = {}, {}  # 分区统计结果和分区分级统计结果
        region_ids = list(np.unique(region_data))  # 各个等级
        # region_ids.remove(32767)
        if 32767 in region_ids: region_ids.remove(32767)  # 去掉无效值等级
        # --------------------------------------------------------------------------------------------------------------
        # 分区分级统计
        no_data_value = ArcpyGdalUtil.get_no_data_value(tiff_path)[0]  # 无效值
        # FIXME 先要将被统计的数据转为浮点型的数据再去统计，或者想办法去掉无效值的影响
        be_stastic_data = be_stastic_data.astype(np.float32)
        if no_data_value is not None:
            be_stastic_data[be_stastic_data == no_data_value] = np.nan
        # 分级分区面积统计
        for index in range(len(grade) - 1):
            region_count = Counter(region_data[(grade[index] < be_stastic_data) & (be_stastic_data < grade[index + 1])])
            res_region_class[index] = dict(zip(region_ids, list(map(lambda x: region_count[x], region_ids))))
        # 调整数据结构
        res_region_class_format = {}
        for class_index in res_region_class:
            class_res = res_region_class[class_index]
            for ele_index in class_res:
                ele_value = class_res[ele_index]
                ele_name = obj_id_field_name_dict[ele_index]
                if ele_name in res_region_class_format:
                    res_region_class_format[ele_name][class_index] = ele_value
                else:
                    res_region_class_format[ele_name] = {class_index: ele_value}
        # --------------------------------------------------------------------------------------------------------------
        # 分区统计
        for index in region_ids:
            region_value = be_stastic_data[region_data == index]  # 获取每个分区的范围对应的被统计的数据
            # 计算需要的统计量
            max_value = np.nanmax(region_value)
            min_value = np.nanmin(region_value)
            mean_value = np.nanmean(region_value)
            pix_count = len(region_value) - np.isnan(region_value).sum()  # 有效值的个数
            res_region[obj_id_field_name_dict[index]] = {'min': min_value, 'max': max_value, 'mean': mean_value,
                                                         'pix_count': pix_count}  # 统计信息汇总
        # --------------------------------------------------------------------------------------------------------------
        os.remove(tiff_from_shp)  # 删除临时文件
        return res_region, res_region_class_format

    # -------------------------------------- need test ---------------------------------------------------------------
    @staticmethod
    def get_plaque(tiff_path, out_tiff_path):
        """获取斑块，输入二值矩阵，返回对应的斑块，每一个序号对应一个斑块"""
        # 我看了一下对比官方算法，我写的算法慢一些，但是官方算法不提供每个斑块中值的具体位置，我的方法可以返回这个信息
        a = GetPlaque()
        # 拿到矩阵,转为 bool 类型
        im_data, im_width, im_height, im_bands, im_geotrans, im_proj = ArcpyGdalUtil.read_tiff(tiff_path)
        im_data = im_data.astype(np.bool)
        # 更新矩阵
        # [1] 我自己写的斑块获取方法
        # new_im_data = a.get_plaque(im_data)
        # [2] 这个是成熟的算法
        new_im_data = measure.label(im_data, connectivity=2)
        # 要更改数据类型为 int 最好不然反应不出来
        ArcpyGdalUtil.write_tiff(new_im_data, im_width, im_height, im_bands, im_geotrans, im_proj,
                                 out_path=out_tiff_path)

    # -------------------------------------- need repair ---------------------------------------------------------------
    @staticmethod
    def read_tiff(path):
        """
        读取 TIFF 文件
        :param path: str，dataset
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
    def write_tiff(im_data, im_width, im_height, im_bands, im_geotrans, im_proj, out_path=None, no_data_value=None,
                   return_mode='TIFF'):
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
        if 'int8' in im_data.dtype.name or 'bool' in im_data.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in im_data.dtype.name:
            datatype = gdal.GDT_Int16  # 这边之前改为无符号类型的 gdal.GDT_UInt16 导致 bug
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
    def get_info(file_path, band_index=0, options=None, return_mode='dict'):
        """
        获取信息
        :param file_path:  文件路径
        :param band_index:  波段 index
        :param options:   获取的信息列表，* 代表获取所有信息
        :param return_mode:  返回类型，返回列表或者字典
        :return: dict or list
        """
        info_options = gdal.InfoOptions(format='json', computeMinMax=True)  # 设置输出为字典结构
        info = gdal.Info(file_path, options=info_options)

        # 获取文件信息
        info_dict = {'size': info['size'],
                     'wgs84Extent': info['wgs84Extent'],
                     'geoTransform': info['geoTransform'],
                     'coordinateSystem': info['coordinateSystem']}

        # 获取波段
        band_info = info['bands'][band_index]  # 指定需要获取信息的波段
        info_dict['mean'] = band_info['mean']  # 均值
        info_dict['type'] = band_info['type']  # 类型
        info_dict['band'] = band_info['band']  # 波段数
        info_dict['max'] = band_info['computedMax']  # 计算最大值
        info_dict['min'] = band_info['computedMin']  # 计算最小值
        info_dict['noDataValue'] = band_info['noDataValue']  # 无效值

        # 需要拿的信息
        if options is None:
            options = ['geoTransform', 'coordinateSystem', 'size', 'mean', 'max', 'min', 'band', 'noDataValue',
                       'wgs84Extent']

        # 组织结果
        if return_mode == 'dict':
            res = {}
            for each_opt in options:
                res[each_opt] = info_dict[each_opt]
            return res
        elif return_mode == 'list':
            res = []
            for each_opt in options:
                res.append(info_dict[each_opt])
            return res
        else:
            raise ValueError('return mode is dict or list')

    @staticmethod
    def get_default_no_data_value(tiff_path):
        """获取当前数据结构的默认无效值"""
        # FIXME  需要完善，还没想好怎么弄
        data_type = gdal.Open(tiff_path).GetRasterBand(1).DataType  # 获取第一个波段的数据类型
        if data_type == 1:
            return 255
        elif data_type == 2:
            return 65535
        elif data_type == 3:
            return -32767

    @staticmethod
    def extract_by_mask_old(tiff_path, shp_path, save_path, res_format='GTiff',
                            assign_no_data_value: (int, float) = None):
        """按掩膜提取"""
        # FIXME  现在的逻辑，只支持一个图层进行掩膜提取
        # -------------------------------------------------------------------------------------------
        no_data_value = ArcpyGdalUtil.get_no_data_value(save_path)
        # 如果被裁剪的 tiff 并未设置无效值，需要提前设置，或者将无效值设置为当前值域的最大值
        if no_data_value[0] is None and no_data_value is None:
            raise ValueError('当前被裁剪图层无无效值，需要设置无效值，或填充 no_data_value 值字段')
        # -------------------------------------------------------------------------------------------
        tiff_envelope = ArcpyGdalUtil.get_tiff_envelope(tiff_path)  # tiff 的范围
        shp_envelope = ArcpyGdalUtil.get_shp_envelope(shp_path)  # shp 的范围
        envelope = ArcpyGdalUtil.envelope_intersection([tiff_envelope, shp_envelope])

        left, bottom, right, top = envelope  # envelope 的范围是否符合要求，不符合直接退出
        if right <= left or top <= bottom:
            print(u'shp 和 tiff 无有效的交集')
            return

        # 转为栅格
        cell_size = ArcpyGdalUtil.get_geotransform_info(tiff_path)[0]  # 获取 tiff 的分辨率
        tiff_from_shp = ArcpyGdalUtil.shp_to_raster(shp_path, '', output_bounds=envelope, cell_size=cell_size,
                                                    output_type=gdal.GDT_Byte, res_format='MEM',
                                                    no_data_value=no_data_value)
        ArcpyGdalUtil.extend_tiff_to_range(tiff_path, save_path, output_bounds=envelope)  # tiff 控制范围

        mask = ArcpyGdalUtil.read_tiff(tiff_from_shp)[0]  # 无效值掩膜，因为是 shp 转的 tiff 所以确定只有一个图层

        if res_format == 'GTiff' and save_path:
            if assign_no_data_value:
                # ArcpyGdalUtil.set_no_data_mask(save_path, mask, '*', assign_no_data_value=no_data_value)
                raise ValueError('目前不支持无效值设置')
            else:
                ArcpyGdalUtil.set_no_data_region_by_mask(save_path, mask, '*')
        else:
            raise ValueError('现在只支持保存为新的文件，看看有没有办法保存为 MEM')

    @staticmethod
    def band_combination(multiband_data, out_path=None, assign_band_index=0):
        """波段提取，提取指定的波段（default = 0）"""
        # 读取数据
        im_data, im_width, im_height, im_bands, im_geotrans, im_proj = ArcpyGdalUtil.read_tiff(multiband_data)
        # 无效值
        no_data_value = ArcpyGdalUtil.get_no_data_value(multiband_data)[assign_band_index]
        # 输出类型
        if out_path:
            return_mode = 'TIFF'
        else:
            return_mode = 'MEMORY'
        #
        return ArcpyGdalUtil.write_tiff(im_data[assign_band_index, :, :], im_width, im_height, 1,
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
                dataset_new.GetRasterBand(band_index + 1).WriteArray(band_array)
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
            im_width, im_height, im_bands, im_geotrans, im_proj = ArcpyGdalUtil.read_tiff(args[0])[1:]
        else:
            raise EOFError('need at least one band')

        # 遍历输入的数据
        for each_band in args:
            im_data_temp, im_width, im_height, im_bands, im_geotrans, im_proj = ArcpyGdalUtil.read_tiff(each_band)
            # 检查数据是否为单波段数据
            if not im_bands == 1:
                raise EOFError('need singleband data')
            im_data.append(im_data_temp)
            no_data_value.extend(ArcpyGdalUtil.get_no_data_value(each_band))

        # 输出类型
        if save_path:
            return_mode = 'TIFF'
        else:
            return_mode = 'MEMORY'

        if im_data:
            return ArcpyGdalUtil.write_tiff(np.array(im_data), im_width, im_height, im_bands, im_geotrans, im_proj,
                                       save_path, return_mode=return_mode, no_data_value=no_data_value)

    @staticmethod
    def copy_data_source(file_path, save_dir, save_name=None):
        """复制文件，连带相关的文件"""
        # gdal 自带的方法复制文件会造成中文的乱码，暂时没有方法来解决
        # 类型检查
        if not isinstance(file_path, str):
            raise ValueError('file_path should be str')

        # 分离文件名和后缀
        file_base_path, file_suffix = os.path.splitext(file_path)

        # 是否自定义文件名
        if save_name is None:
            base_name = os.path.basename(file_path)
            save_base_name = os.path.join(save_dir, base_name)
        else:
            save_base_name = os.path.join(save_dir, save_name)

        # 查看文件类型和对应的相关文件
        if file_path.endswith('tif'):
            related_suffix = ['.tfw', '.tif', '.tif.aux.xml', '.tif.ovr', '.tif.vat.cpg', '.tif.vat.dbf']
        elif file_path.endswith('.shp'):
            related_suffix = ['.dbf', '.prj', '.shp', '.shx', '.cpg', '.sbn', '.sbx', '.shp.xml']
        else:
            raise ValueError('file_path can only be endwith shp or tif')

        # 拷贝文件
        for each_suffix in related_suffix:
            old_path = file_base_path + each_suffix
            new_path = save_base_name + each_suffix
            if os.path.exists(old_path):
                shutil.copyfile(old_path, new_path)

    # todo 参考 copy_data_source 完善文件的删除

    @staticmethod
    def file_operate():
        """文件操作"""
        # 操作都会涉及到文件的依赖文件
        # -------------------------------------------------------
        driver = gdal.GetDriverByName('Gtiff')
        driver.Create()  # 使用当前驱动创建新的图像
        driver.CopyFiles()  # 创建数据集副本
        driver.CreateCopy()  # 复制指定文件
        driver.Rename()  # 重命名图像文件
        driver.Delete()  # 删除指定文件
        # -------------------------------------------------------
        driver = ogr.GetDriverByName("ESRI Shapefile")
        driver.CopyDataSource()
        driver.CopyDataSource()
        driver.CreateDataSource()
        driver.DeleteDataSource()
        driver.Open()

    @staticmethod
    def project_raster(in_tiff, prof_tiff=None, im_proj=None):
        """raster 投影转换，传入指定的坐标系统或者指定的 raster ，获取其坐标系统，赋给输入的 raster"""

        """
        使用 Translate 的思路
        # projWin --- subwindow in projected coordinates to extract: [ulx, uly, lrx, lry]
        # projWinSRS --- SRS in which projWin is expressed

        translate_options = gdal.TranslateOptions()

        # return gdal.Translate(tiff_out, tiff_path, options=translate_options)

        # gdal.Translate()  # 转换
        """
        ds = gdal.Open(in_tiff, gdal.GA_Update)  # dataset

        if prof_tiff:  # 如果输入 tiff 获取这个tiff 的 im_proj 信息
            ds_raster = gdal.Open(prof_tiff)
            im_proj = ds_raster.GetProjection()

        if im_proj:
            ds.SetProjection(im_proj)  # 设置坐标系统
        else:
            raise ValueError("need im_proj or proj_tiff")
        return ds


if __name__ == '__main__':

    pass
