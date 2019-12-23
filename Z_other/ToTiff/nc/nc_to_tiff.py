# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import os
import datetime
from Report.XmlUtil import Xml_Util
import time


class NcToTiff(object):
    """nc文件转为 tiff 文件, issue 默认的是北京时间"""

    # FIXME 可以设置 NRT 和 RT 只生产一个文件

    def __init__(self):
        # 后面需要用到的时间信息
        self.__assign_time_BJ = None
        self.__assign_time_BJ_str = None
        self.__assign_time_UTC = None
        self.__assign_time_UTC_str = None
        # 需要的文件
        self.__file_needed = []
        # 输出文件路径列表
        self.__file_put_path = []
        # gdal_translate exe 的路径
        self.gdal_translate_exe_path = None
        # 输出的文件
        self.__out_tiff_path = []
        # 需要检查的文件夹
        self.dirs_to_check = []
        # 找到的符合条件的文件
        self.__file_seek_out = []
        # 保存的文件夹
        self.save_dir = None
        # 期号
        self.issue = None
        # 过滤条件
        self.file_check_condition = '*'

    def init(self):
        """初始化"""
        # 解析 xml
        # xml_dict = Xml_Util.xml_parser(r'E:\Algorithm\Util_Util\ToTiff\nc\input.xml', ['input'], 'identify')
        # 北京时间， FIXME 默认输入的是北京时间
        self.__assign_time_BJ_str = self.issue
        self.__assign_time_BJ = datetime.datetime.strptime(self.__assign_time_BJ_str, '%Y%m%d%H', )
        # 世界时
        self.__assign_time_UTC = self.__assign_time_BJ + datetime.timedelta(hours=-8)
        self.__assign_time_UTC_str = datetime.datetime.strftime(self.__assign_time_UTC, '%Y%m%d%H')
        # 保存文件夹
        # self.save_dir = xml_dict['out_dir']
        # exe path
        # self.gdal_translate_exe_path = xml_dict['gdal_translate_exe_path']

    def remove_file_unnecessary(self, file_seek_out):
        """根据传入的关键字，去除不需要的文件"""
        if self.file_check_condition == '*':
            self.__file_seek_out = file_seek_out
        elif isinstance(self.file_check_condition, list):
            for each_file in file_seek_out:
                base_name = os.path.basename(each_file)  # 文件名
                for each_condition in self.file_check_condition:
                    if each_condition in base_name:
                        self.__file_seek_out.append(each_file)

    def get_assign_file_path(self):
        """找到符合要求的文件"""
        file_seek_out = []

        for each_dir in self.dirs_to_check:
            # 文件不存在的情况
            if not os.path.exists(each_dir):
                continue

            # 遍历文件夹中的文件
            for each_file in os.listdir(each_dir):
                # 过滤非 nc 数据
                if each_file.endswith('.nc'):
                    # 根据是否有 ASI 判断当前文件的时间
                    prd_time = self.__assign_time_UTC_str if 'ASI' in each_file else self.__assign_time_BJ_str
                    # 拿出文件中的时间
                    if prd_time == each_file[-13:-3]:
                        file_seek_out.append(os.path.join(each_dir, each_file))

            # 对文件进行遍历，去掉不需要的文件
            self.remove_file_unnecessary(file_seek_out)

    def get_save_path(self, file_path):
        """根据规则得到输出文件夹的文件名"""
        # 取到文件产品时间之前，
        f_basename = os.path.basename(file_path)
        # 输出文件夹
        out_reladir = os.path.join(self.__assign_time_BJ_str[:6], self.__assign_time_BJ_str[:8])
        out_reladir += r'\NRT' if 'NRT_' in f_basename else r'\RT'
        out_reladir += r'\HOR' if '_HOR' in f_basename else r'\DAY'
        out_path = os.path.join(self.save_dir, out_reladir)
        # 新建文件夹
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        #
        geotif_name = f_basename[:-13] + self.__assign_time_BJ_str + '.tif'  #  把 basename 的时间统一改为北京时间
        out_geotif = os.path.join(out_path, geotif_name)
        return out_geotif

    def nc_to_tif(self, nc_file, out_geotif):
        """通过gdal_translate把nc转为tif"""
        cmd_str = self.gdal_translate_exe_path + ' -a_srs WGS84 -of GTiff -sds ' + nc_file + ' ' + out_geotif
        os.system(cmd_str)

    def translate(self):
        """转换"""
        for each_file in self.__file_seek_out:
            #
            # 保存路径
            save_path = self.get_save_path(each_file)
            # 转换
            self.nc_to_tif(each_file, save_path)

    def do_process(self):
        """总步奏"""
        # 初始化
        self.init()
        #
        self.get_assign_file_path()
        #
        self.translate()


if __name__ == '__main__':

    start = time.time()
    # ------------------------------------------------
    a = NcToTiff()
    # ------------------------------------------------
    # 解析 xml
    # xml_dict = Xml_Util.xml_parser(r'E:\Algorithm\Util_Util\ToTiff\nc\input.xml', ['input'], 'identify')
    xml_dict = Xml_Util.xml_parser(r'D:\Code\Util_Util\ToTiff\nc\input.xml', ['input'], 'identify')
    # 北京时间， FIXME 默认输入的是北京时间
    a.issue = xml_dict['issue'][:10]
    # 保存文件夹
    a.save_dir = xml_dict['out_dir']
    # exe path
    a.gdal_translate_exe_path = xml_dict['gdal_translate_exe_path']
    # ------------------------------------------------
    # 根据当前的日期找到需要遍历的文件夹，FIXME 直接返回当前时间的文件夹和昨天的文件夹即可，没必要再去运算
    # 北京时间
    assign_time = datetime.datetime.strptime(a.issue, '%Y%m%d%H',)
    assign_time_str = datetime.datetime.strftime(assign_time, '%Y%m%d')
    # 北京时间的前一天
    assign_time_yeasterday = assign_time + datetime.timedelta(days=-1)
    assign_time_yeasterday_str = datetime.datetime.strftime(assign_time_yeasterday, '%Y%m%d')
    # 拼出两个要找的文件夹
    a.dirs_to_check = []
    a.dirs_to_check.append(os.path.join(xml_dict['input_path'], assign_time_str))
    a.dirs_to_check.append(os.path.join(xml_dict['input_path'], assign_time_yeasterday_str))
    # 处理的文件的条件，FIXME 这边其实就是用运算量换存储量而已，目前来看大的运算量没有问题，有问题的是存储写入效率比较低
    if xml_dict['file_check_condition'] == "*":
        a.file_check_condition = '*'
    else:
        a.file_check_condition = xml_dict['file_check_condition'].split(',')
    # ------------------------------------------------
    a.do_process()

    stop = time.time()

    print(stop - start)
