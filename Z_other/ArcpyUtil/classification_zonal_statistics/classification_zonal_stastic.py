# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import arcpy
import uuid
import os
from GdalUtil import GdalBase, OgrBase
import numpy as np


class Stastic(object):

    @staticmethod
    def __extract_by_attributes(tiff_path, min_value, max_value, save_path=None):
        """根据属性对栅格进行提取，模仿的 arcpy.sa.ExtractByAttributes"""
        im_data, im_width, im_height, im_bands, im_geotrans, im_proj = GdalBase.read_tiff(tiff_path)
        im_data = im_data.astype(np.float64)  # FIXME 为了能使用 np.nan，将类型转为 float 类型，如何才能找到根据数据类型自定义无效值的值呢？
        # 获取无效值
        no_data_value = GdalBase.get_no_data_value(tiff_path)[0]
        if no_data_value is None:
            no_data_value = np.nan

        # 将不符合条件的复制为空
        im_data[im_data <= min_value] = no_data_value
        im_data[im_data > max_value] = no_data_value
        # 保存 tiff
        if save_path:
            return GdalBase.write_tiff(im_data, im_width, im_height, im_bands, im_geotrans, im_proj, out_path=save_path, no_data_value=no_data_value)
        else:
            return GdalBase.write_tiff(im_data, im_width, im_height, im_bands, im_geotrans, im_proj, return_mode="MEMORY", no_data_value=no_data_value)

    @staticmethod
    def zonal_stastic(tiff_path, shp_path, temp_path, assign_field='ID', need_data_list=None):
        """分级统计"""
        # 规范统计要数
        if need_data_list is None:
            need_data_list = [assign_field,'SUM', 'MIN', 'MAX', 'MEAN']
        else:
            need_data_list = list(need_data_list)
            need_data_list.insert(0, assign_field)  # 添加指定的 field

        # 先预设输出结果，假使输入的 tiff 为空，也能有返回值
        result_dict = {}
        # for each_line in arcpy.da.SearchCursor(shp_path, assign_field):
        for each_line in OgrBase.get_field(shp_path, [assign_field]):
            id_temp = each_line[0]
            result_dict[id_temp] = {}
            for each_need_data in need_data_list[1:]:
                result_dict[id_temp][each_need_data] = None

        out_table = os.path.join(temp_path, '{0}.dbf'.format(str(uuid.uuid1())[:5]))  # 输出统计表位置
        # FIXME 这是最后一个需要 Arcpy 的功能，在合适的情况下进行替换

        try:
            arcpy.sa.ZonalStatisticsAsTable(shp_path, assign_field, tiff_path, out_table, "DATA", "ALL")  # 统计
            cursor = arcpy.da.SearchCursor(out_table, need_data_list)  # 查询需要的字段
            # cursor = DbfUtil.get_table(out_table, need_data_list)  # 查询需要的字段

            # 格式化输出
            for each_line in cursor:
                id_temp = each_line[0]
                print id_temp
                for field_index, each_field_name in enumerate(need_data_list[1:]):
                    result_dict[id_temp][each_field_name] = each_line[field_index+1]
        # FIXME 这边就是会报错，是需要用 try 结构来接住结果的
        except:
            # 格式化输出
            cursor = arcpy.da.SearchCursor(shp_path, [assign_field])
            for each_line in cursor:
                id_temp = each_line[0]
                for field_index, each_field_name in enumerate(need_data_list[1:]):
                    result_dict[id_temp][each_field_name] = None

        # 输出统计字典
        return result_dict

    @staticmethod
    def classification_zonal_stastic(tiff_path, shp_path, temp_path, class_value_list, assign_field='ID', need_data_list=None, show_detail=False):
        """分级分区统计"""
        result_dict = {}
        for i in range(len(class_value_list)-1):
            # 遍历每个级别
            low, high = class_value_list[i], class_value_list[i+1]
            print(low, " - ", high)
            # 得到每个级别的 tiff
            tiff_temp_path = os.path.join(temp_path, str(uuid.uuid1())+'.tif')
            Stastic.__extract_by_attributes(tiff_path, min_value=low, max_value=high, save_path=tiff_temp_path)
            # -------------------------------------------------------
            # FIXME 使用 GdalUtil 里面的方法替换下面的语句
            # sql_conditions = "{0}<VALUE and VALUE<={1}".format(low, high); print(sql_conditions)  # 获取 sql 条件语句
            # tiff_temp_path = arcpy.sa.ExtractByAttributes(tiff_path, sql_conditions)
            # -------------------------------------------------------
            # FIXME 这边会报错，直接用
            # 对每个级别进行统计
            zonal_stastic_result_temp = Stastic.zonal_stastic(tiff_temp_path, shp_path, temp_path, assign_field=assign_field, need_data_list=need_data_list)
            # 规范化统计结果
            result_dict[i] = zonal_stastic_result_temp

            # 删除用于统计的临时文件
            try:
                os.remove(tiff_temp_path)
            except:
                print('remove temp file : {0}'.format(tiff_temp_path))

            # 查看输出
            if show_detail:
                for each in zonal_stastic_result_temp.items():
                    print(each)
                print('-'*100)

        # 输出结果
        return result_dict





















