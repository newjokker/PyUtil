# -*- coding: utf-8  -*-
# -*- author: jokker -*-

# TODO 要素根据属性进行提取，类似于arcpy 中的
# TODO 要素根据范围进行提取，

"""
aa = arcpy.MakeFeatureLayer_management(r'D:\BaiduNetdiskDownload\1567560995279\station_point.shp')
a = arcpy.SelectLayerByAttribute_management(aa, "NEW_SELECTION", '"lon" > 100')
arcpy.CopyFeatures_management(a, r'D:\BaiduNetdiskDownload\1567560995279\123.shp')
"""

# todo 可以将操作 field 的内容进行单独的提取出来，当做一个类来做


import ogr
import gdal
import os
import logging
import osr
import numpy as np


class ArcpyOsgeoUtil(object):

    @staticmethod
    def get_field(shp_path, field_names, need_line=None):
        """
        获取 shp 属性表字段
        :param shp_path: shp 的路径，或者一个 datasourse； path, datasourse
        :param field_names: 需要获取的属性的名称; [str, str]； '*' 全部
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
    def get_field_name(shp_path):
        """获取字段名"""
        gdal.SetConfigOption("SHAPE_ENCODING", "")

        if isinstance(shp_path, ogr.DataSource):
            ds = shp_path
        else:
            ds = ogr.Open(shp_path)

        # 获取 layer
        lyr = ds.GetLayer()
        if not isinstance(lyr, ogr.Layer):
            return

        res_list = []  # 结果
        field_count = lyr.GetLayerDefn().GetFieldCount()  # 字段数目
        lyr_defn = lyr.GetLayerDefn()

        for index in range(field_count):
            field_name = lyr_defn.GetFieldDefn(index).GetNameRef()
            res_list.append(field_name)

        return res_list

    @staticmethod
    def add_field(shp_path, field_name, field_type=ogr.OFTString, field_value_list=None):
        """给 shp 增加一个 field"""
        ds = ogr.Open(shp_path, gdal.GA_Update)
        lyr = ds.GetLayer()

        # 当前字段不存在，可以创建
        if lyr.FindFieldIndex(field_name, 1) == -1:
            new_field = ogr.FieldDefn(field_name, field_type)  # 创建字段
            lyr.CreateField(new_field)  # 增加字段
        else:
            # print('the field have exist')
            return

        # 编辑字段中的元素
        length = len(field_value_list)
        for feature_index, each_feature in enumerate(lyr):
            if length > feature_index:
                each_feature.SetField(field_name, field_value_list[feature_index])
                lyr.SetFeature(each_feature)  # 这一句话不加的话，属性是设置不了的
            else:
                break  # 退出循环，有多少值就设置多少个

        ds.FlushCache()
        ds.Destroy()

    @staticmethod
    def add_object_index(shp_path, field_name: str = 'object_index'):
        """增加要素字段，值与 FID 相同，类型为 int16"""
        info = ArcpyOsgeoUtil.get_field(shp_path, '*')
        ArcpyOsgeoUtil.add_field(shp_path, field_name, ogr.OFTInteger, list(range(len(info))))

    @staticmethod
    def delete_field(shp_path, field_name_list: (tuple, list)):
        """删除指定的字段"""
        gdal.SetConfigOption("SHAPE_ENCODING", "")

        if isinstance(shp_path, ogr.DataSource):
            ds = shp_path
        else:
            ds = ogr.Open(shp_path, gdal.GA_Update)

        # 获取 layer
        lyr = ds.GetLayer()
        if not isinstance(lyr, ogr.Layer):
            return

        for each_field_name in field_name_list:
            field_index = lyr.FindFieldIndex(each_field_name, 0)  # FIXME 这边没弄清楚，第二个参数是干嘛用的
            if field_index != -1:
                lyr.DeleteField(field_index)
                print('delete field ：{0} <-- {1}'.format(each_field_name, shp_path))

    # -------------------------------------- need repair ---------------------------------------------------------------

    @staticmethod
    def update_field():
        """更新属性表信息"""
        pass

    @staticmethod
    def get_proj(proj_str="WGS84"):
        """返回需要的坐标系"""
        osrobj = osr.SpatialReference()
        osrobj.SetWellKnownGeogCS(proj_str)
        return osrobj

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

    # @staticmethod
    # def extract_points_values_in_tiff(tif_path, point_shp, info_field=None):
    #     """
    #     获取点在tif中对应位置的值
    #     :param tif_path: tif 文件路径，单波段
    #     :param point_shp: 点图层，
    #     :param info_field : 用于区分每个值对应的点
    #     :return: float OR int
    #     """
    #     # FIXME 这个函数设计有问题，需要好好的修改
          # FIXME 因为获取范围改变了，所以需要更改这边的代码
    #     # --------------------------------------------------------------------------------------------------------------
    #     im_data, im_width, im_height, im_bands, im_geotrans, im_proj = GdalBase.read_tiff(tif_path)
    #     pixel_width, pixel_height = im_geotrans[1], im_geotrans[5]
    #     lon1, lat1, lon2, lat2 = GdalBase.get_envelope(tif_path)
    #     # --------------------------------------------------------------------------------------------------------------
    #     points_info = CreateOgr.convert_point_to_dict(point_shp)  # 解析点数据，得到点的坐标
    #     # 拿到点的坐标和区分各个点的信息
    #     points_info_need = map(lambda x: {'lon': x['lon'], 'lat': x['lat'], 'info_field': x[info_field]}, points_info)
    #     # --------------------------------------------------------------------------------------------------------------
    #     for each_point in points_info_need:
    #         # 拿到经纬度
    #         point_lon, point_lat = each_point['lon'], each_point['lat']
    #         # 判断点是否在范围内部
    #         if not (lon1 <= point_lon <= lon2 and lat2 <= point_lat <= lat1):
    #             logging.error('point isnot in assign region')
    #             each_point['value'] = None
    #             continue
    #         # 获取点所在栅格行列，返回栅格值
    #         offset_lon = point_lon - lon1
    #         offset_lat = point_lat - lat1
    #         offset_lon_cell = int(offset_lon / pixel_width)
    #         offset_lat_cell = int(offset_lat / pixel_height)
    #         # 返回栅格值在字典中的数据类型
    #         each_point['value'] = im_data[offset_lat_cell, offset_lon_cell]
    #     return points_info_need

    @staticmethod
    def create_points_from_dict(point_info, save_path, proj_path=None, attr_type=None, lon_string='lon',
                                lat_string='lat'):
        """
        从字典创建点数据"
        :param lat_string: 纬度所用的字符串
        :param lon_string: 经度所用的字符串
        :param point_info:  火点信息字典，其中 lon 和 lat 字段用于火点的坐标。point_info = [{'lon': 123, 'lat': 12, 'area': 11, 'date': 'jokk'}]
        :param save_path:  保存的 shp 路径
        :param proj_path:  坐标文件路径
        :param attr_type:  指定文件的数据类型， dict,{'lon': 'int', 'date': 'string'}
        :return: None
        """

        # TODO 对数据进行过滤，改变输入的 字典的内容

        # 读取坐标系信息
        if proj_path is None:
            proj = ArcpyOsgeoUtil.get_proj("WGS84")
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
        # 新建 Layer ,我终于知道了，当传进来的是 folder 的时候 那个 'fire_point' 就发挥作用了，作为文件名了
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
            proj = ArcpyOsgeoUtil.get_proj("WGS84")
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
            proj = ArcpyOsgeoUtil.get_proj("WGS84")
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


class RasterProjectUtil(object):
    """raster相关的投影转换"""

    @staticmethod
    def project_raster(in_tiff, prof_tiff=None, im_proj=None):
        """raster 投影转换，传入指定的坐标系统或者指定的 raster ，获取其坐标系统，赋给输入的 raster"""
        ds = gdal.Open(in_tiff, gdal.GA_Update)  # dataset

        if prof_tiff:  # 如果输入 tiff 获取这个tiff 的 im_proj 信息
            ds_raster = gdal.Open(prof_tiff)
            im_proj = ds_raster.GetProjection()

        if im_proj:
            ds.SetProjection(im_proj)  # 设置坐标系统
        else:
            raise ValueError("need im_proj or proj_tiff")
        return ds

    # ----------------------- need repair --------------------------------------

    # 下面的直接从网上拉过来的，需要进行改写

    @staticmethod
    def get_srs_pair(dataset):
        """
        获得给定数据的投影参考系和地理参考系
        :param dataset: GDAL地理数据
        :return: 投影参考系和地理参考系
        """
        prosrs = osr.SpatialReference()
        prosrs.ImportFromWkt(dataset.GetProjection())
        geosrs = prosrs.CloneGeogCS()
        return prosrs, geosrs

    @staticmethod
    def geo_2_lonlat(dataset, x, y):
        """
        将投影坐标转为经纬度坐标（具体的投影坐标系由给定数据确定）
        :param dataset: GDAL地理数据
        :param x: 投影坐标x
        :param y: 投影坐标y
        :return: 投影坐标(x, y)对应的经纬度坐标(lon, lat)
        """
        prosrs, geosrs = RasterProjectUtil.get_srs_pair(dataset)
        ct = osr.CoordinateTransformation(prosrs, geosrs)
        coords = ct.TransformPoint(x, y)
        return coords[:2]

    @staticmethod
    def lonlat_2_geo(dataset, lon, lat):
        """
        将经纬度坐标转为投影坐标（具体的投影坐标系由给定数据确定）
        :param dataset: GDAL地理数据
        :param lon: 地理坐标lon经度
        :param lat: 地理坐标lat纬度
        :return: 经纬度坐标(lon, lat)对应的投影坐标
        """
        prosrs, geosrs = RasterProjectUtil.get_srs_pair(dataset)
        ct = osr.CoordinateTransformation(geosrs, prosrs)
        coords = ct.TransformPoint(lon, lat)
        return coords[:2]

    @staticmethod
    def image_xy_2_geo(dataset, row, col):
        """
        根据GDAL的六参数模型将影像图上坐标（行列号）转为投影坐标或地理坐标（根据具体数据的坐标系统转换）
        :param dataset: GDAL地理数据
        :param row: 像素的行号
        :param col: 像素的列号
        :return: 行列号(row, col)对应的投影坐标或地理坐标(x, y)
        """
        trans = dataset.GetGeoTransform()
        px = trans[0] + col * trans[1] + row * trans[2]
        py = trans[3] + col * trans[4] + row * trans[5]
        return px, py

    @staticmethod
    def geo_2_image_xy(dataset, x, y):
        """
        根据GDAL的六 参数模型将给定的投影或地理坐标转为影像图上坐标（行列号）
        :param dataset: GDAL地理数据
        :param x: 投影或地理坐标x
        :param y: 投影或地理坐标y
        :return: 影坐标或地理坐标(x, y)对应的影像图上行列号(row, col)
        """
        trans = dataset.GetGeoTransform()
        a = np.array([[trans[1], trans[2]], [trans[4], trans[5]]])
        b = np.array([x - trans[0], y - trans[3]])
        return np.linalg.solve(a, b)  # 使用numpy的linalg.solve进行二元一次方程的求解


class ShpProjectUtil(object):
    """矢量相关的投影转换"""

    @staticmethod
    def prj2geo(shp_path, x, y):
        """输入为待操作shp的路径，和一组待转换的投影坐标"""
        # 为了支持中文路径，请添加下面这句代码
        gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
        # 为了使属性表字段支持中文，请添加下面这句
        gdal.SetConfigOption("SHAPE_ENCODING", "")
        # 注册所有的驱动
        ogr.RegisterAll()
        # 数据格式的驱动
        driver = ogr.GetDriverByName('ESRI Shapefile')
        ds = driver.Open(shp_path)
        layer0 = ds.GetLayerByIndex(0)

        # 或取到shp的投影坐标系信息
        prosrs = layer0.GetSpatialRef()
        geosrs = osr.SpatialReference()
        # 设置输出坐标系为WGS84
        geosrs.SetWellKnownGeogCS("WGS84")

        ct = osr.CoordinateTransformation(prosrs, geosrs)
        coords = ct.TransformPoint(x, y)
        # 输出为转换好的经纬度
        return coords[:2]

    @staticmethod
    def project_shp(shp_path, proj_shp_path=None):
        """将 shp 进行重新投影"""

        # todo 定义投影

        # 定义投影转换关系
        inosr = osr.SpatialReference()
        # inosr.ImportFromEPSG(4269)  # fixme 这边需要看看和自定义
        inosr.ImportFromEPSG(26912)  # fixme 这边需要看看和自定义

        inosr.ImportFromProj4(shp_path)


        outosr = osr.SpatialReference()
        outosr.ImportFromEPSG(26912)  # fixme 看看对应的是什么坐标系
        trans = osr.CoordinateTransformation(inosr, outosr)

        # todo 我觉得步奏应该是这样的 （1）用写的方式读取 shp 文件 （2）定义投影转换 （3）对 shp 进行投影转换


if __name__ == '__main__':

    pass






