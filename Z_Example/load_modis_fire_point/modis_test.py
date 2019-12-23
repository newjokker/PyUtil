# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from Report.ZipUtil import ZipUtil
from Report.LoadUtil import LoadUtil
from Report.ArcpyOsgeoUtil import ArcpyOsgeoUtil
from Report.HTHTIssue import HTHTIssue
import time
import os
import uuid


MODIS_url = r'https://firms.modaps.eosdis.nasa.gov/data/active_fire/c6/shapes/zips/MODIS_C6_Russia_and_Asia_24h.zip'

# todo 需要计算火点面积，所在省市县等信息


class ModisFire(object):

    def __init__(self, temp_folder):
        self.temp_folder = temp_folder  # 临时文件夹
        self.temp_path = os.path.join(self.temp_folder, str(uuid.uuid1()))
        os.makedirs(self.temp_path)

        self.fire_shp = None  # 火点 shp 地址
        self.roi_fire_shp = None  # 感兴趣区域的火点 shp 文件地址
        self.fire_point_roi = None  # 感兴趣区域的火点
        self.fire_point_roi_new = None  # 感兴趣区域的新火电

        self.fire_point_dict_roi_new = None  # 找到的新火电的火点信息

    def get_modis_fire_file(self):
        """获取 modis 监测到的火点"""
        issue = time.strftime('%Y%m%d_%H%M%S')
        save_path_zip = os.path.join(self.temp_path, issue + '.zip')
        LoadUtil.load_file_from_url(MODIS_url, save_path_zip)
        save_folder_shp = os.path.join(self.temp_path, issue)
        ZipUtil.unzip_file(save_path_zip, save_folder=save_folder_shp)
        self.fire_shp = os.path.join(save_folder_shp, 'MODIS_C6_Russia_and_Asia_24h.shp')

    def get_roi_fire_point_by_clip_fire_shp(self):
        """通过裁剪获取感兴趣区域的火点"""
        # todo arcpy clip 实现

    def cal_fire_point_info(self):
        """计算火点属性，在哪个省市县"""

    def get_fire_point_from_shp(self):
        """从 shp 中获取火点字典"""

        self.fire_point_dict_roi_new = ArcpyOsgeoUtil.convert_point_to_dict(self.fire_shp)

        for each in self.fire_point_dict_roi_new[:10]:
            print(each)



if __name__ == '__main__':

    temp_folder = r'C:\Users\Administrator\Desktop\modis'
    a = ModisFire(temp_folder)
    a.get_modis_fire_file()
    a.get_fire_point_from_shp()




