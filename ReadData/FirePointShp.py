# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
* 从 shp 解析火点，并存储到 自定义的结果中去，尝试使用 pandas 来辅助解决
* 可以将每一天的火点存在一个 shp 文件中，这样比较清晰，或者是每一期的存放在一个 shp 中
"""

from Report.ArcpyOsgeoUtil import ArcpyOsgeoUtil
from Assist.AssistUtil import AssistUtil
import os


class FirePointShpOperation(object):

    def __init__(self):
        self.data_folder = r''  # 文件下载的地址
        self.temp_path = r''  # 缓存文件的地址

    @staticmethod
    def split_fire_shp_by_issue(fire_shp_path, save_folder):
        """根据期次对火点进行拆分，不同期次放到不同的文件中"""
        # todo 改为动态函数

        fire_points = ArcpyOsgeoUtil.convert_point_to_dict(fire_shp_path)

        # 给火点字典增加期次属性
        for each_fire_point in fire_points:
            issue = each_fire_point['ACQ_DATE'].replace('/', '') + each_fire_point['ACQ_TIME']  # 两个属性得到期次
            each_fire_point['issue'] = issue

        # 对产品按照 期次属性进行分组
        for each_issue in AssistUtil.group_by(fire_points, 'issue'):
            points_in_assign_issue = list(each_issue[1])  # 获得一个期次的所有火点列表
            save_path = os.path.join(save_folder, each_issue[0] + '.shp')
            attr_type = {'lon': 'int', 'lat': 'int'}
            ArcpyOsgeoUtil.create_points_from_dict(points_in_assign_issue, save_path, attr_type=attr_type)

    def have_fire_file_in_assign_issue(self):
        """指定期次是否有火点文件"""
        pass

    def get_file_point_in_assign_issue(self):
        """查询指定期次的火点，没有对应的文件就返回 None ，没有火点返回 [] 有火点返回火点列表"""
        pass

    def get_file_point_in_assign_issue_range(self):
        """获取指定期次范围内的火点"""
        pass


if __name__ == "__main__":

    fireShpPath = r'C:\Users\Administrator\Desktop\del\del_ningan\test_data\VNP14IMGTDL_NRT_Russia_and_Asia_24h.shp'
    saveFolder = r'C:\Users\Administrator\Desktop\del\del_ningan\split_data_2'
    FirePointShpOperation.split_fire_shp_by_issue(fireShpPath, saveFolder)









