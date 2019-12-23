# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
对于好几天才能接受完整的数据来说，不能用面向期次的解决思路
公司之前的预处理是很有问题的，之前的预处理是面向期次的，不断去扫描一个期次需要的文件夹，运行这个期次，其实正确的方法是面向文件的增量
来一次文件就对新的文件进行一次运行，而不是不断的去扫描固定的期次，面向期次是不能检测是否运行完成的
"""


import os
import datetime
from Decorator.time_it import timethis


class NcFileToTiff(object):
    """传入 nc 文件，输出 tiff 文件"""

    def __init__(self):
        # 需要处理的文件
        self.files_to_transform = []
        # 保存的路径
        self.save_dir = None
        # 转换用到的 exe
        self.gdal_translate_exe_path = None

    @staticmethod
    def get_file_time(file_path):
        """获取文件的时间，世界时转为北京时"""
        file_base_name = os.path.basename(file_path)  # 文件名
        if 'ASI' in file_base_name:
            UTC_str = file_base_name[-13:-3]
            UTC_time = datetime.datetime.strptime(UTC_str, '%Y%m%d%H')
            CHN_time = UTC_time + datetime.timedelta(hours=-8)
            CHN_str = datetime.datetime.strftime(CHN_time, '%Y%m%d%H')
            return CHN_str
        elif 'CHN' in file_base_name:
            return file_base_name[-13:-3]
        else:
            return

    def get_save_path(self, file_path):
        """根据文件名，得到输出路径"""
        CHN_time_str = self.get_file_time(file_path)  # 获取北京时间

        # 取到文件产品时间之前，
        file_basename = os.path.basename(file_path)
        # 输出文件夹
        out_reladir = os.path.join(CHN_time_str[:6], CHN_time_str[:8])
        out_reladir += r'\NRT' if '_NRT_' in file_basename else r'\RT'
        out_reladir += r'\HOR' if '_HOR-' in file_basename else r'\DAY'
        out_path = os.path.join(self.save_dir, out_reladir)
        # 新建文件夹
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        #
        geotif_name = file_basename[:-13] + CHN_time_str + '.tif'  #  把 basename 的时间统一改为北京时间
        out_geotif = os.path.join(out_path, geotif_name)
        return out_geotif

    def nc_to_tiff(self, nc_file, out_geotif):
        """调用cmd ， nc 文件转为 tiff 文件"""
        cmd_str = self.gdal_translate_exe_path + ' -a_srs WGS84 -of GTiff -sds ' + nc_file + ' ' + out_geotif
        os.system(cmd_str)

    @timethis
    def do_process(self):
        """主流程"""
        for each_file in self.files_to_transform:
            if not each_file.endswith('.nc'):  # 过滤非 nc 文件
                continue

            # 得到返回值
            save_path = self.get_save_path(each_file)
            # 转换
            self.nc_to_tiff(each_file, save_path)


if __name__ == '__main__':

    a = NcFileToTiff()

    a.save_dir = r'C:\Users\74722\Desktop\NC\out'

    # data_dir = r'C:\Users\Administrator\Desktop\NC\data'
    data_dir = r'C:\Users\74722\Desktop\NC\nc_data\20190702'

    # a.gdal_translate_exe_path = r'C:\Python27\ArcGIS10.5\Lib\site-packages\osgeo\gdal_translate.exe'
    a.gdal_translate_exe_path = r'C:\Python27\ArcGIS10.3\Lib\site-packages\osgeo\gdal_translate.exe'

    a.files_to_transform = map(lambda x:os.path.join(data_dir, x), os.listdir(data_dir))

    a.do_process()

