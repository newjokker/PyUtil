# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from Report.GdalUtil import CreateOgr, OgrBase, GdalBase
from ReadData.RandomUtil import RandomUtil


def main(shp_save_path, fire_points):
    """生成测试火点"""
    fire_dict_new = []
    # 将每一个火点进行处理
    for each in fire_points:
        each_fire_info = {'lon': each[0], 'lat': each[1]}
        fire_dict_new.append(each_fire_info)
    # 生成测试火点 shp
    CreateOgr.create_points_from_dict(fire_dict_new, save_path=shp_save_path)


def get_random_fire_point(lon_min, lon_max, lat_min, lat_max, fire_num=10):
    """获取一定范围内的随机火点"""
    res_fire_point = []
    for i in range(fire_num):
        each_lon = RandomUtil.rand_range_float(lon_min, lon_max)
        each_lat = RandomUtil.rand_range_float(lat_min, lat_max)
        res_fire_point.append((each_lon, each_lat))
    return res_fire_point


if __name__ == "__main__":

    fire_point_save_path = r'E:\Algorithm\Util_Util\Z_for_code_zc\002\data\test_001.shp'
    assign_fire_points = []
    # 添加指定火点
    assign_fire_points.extend([('133.225', '47.745'), ('133.469', '47.76'), ('133.352', '47.795')])  # 浓江农场
    assign_fire_points.append(('117.40', '31.84'))  # 合肥
    assign_fire_points.append(('128.74', '43.49'))  # 延边
    assign_fire_points.append(('125.49', '44.40'))  # 长春
    assign_fire_points.extend([('120.08', '40.47'), ('120.08', '40.57'), ('120.06', '40.57')])  # 葫芦岛
    # 添加随机火点
    random_fire_point = get_random_fire_point(100, 120, 30, 50, fire_num=10000)
    assign_fire_points.extend(random_fire_point)
    #
    main(fire_point_save_path, assign_fire_points)
