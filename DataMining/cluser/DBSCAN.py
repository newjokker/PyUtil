# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import numpy as np
from sklearn.cluster import DBSCAN
from Report.ArcpyOsgeoUtil import ArcpyOsgeoUtil


"""
* min_samples : 小于 min_samples 就不是一类
* 结果为 -1 就是孤点的意思
"""


class DbscanUtil(object):

    @staticmethod
    def cluser_saptial_point(points, eps, min_samples=2):
        """空间点的聚类"""
        res = {}
        point_type = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(points)
        #
        for point_index, each_point in enumerate(points):
            each_type = point_type[point_index]
            if each_type in res:
                res[each_type].append(each_point)
            else:
                res[each_type] = [each_point]
        return res

    @staticmethod
    def cluser_point_shp(point_path, save_path, eps, min_samples=2):
        """聚类邻近的点"""
        point_info = ArcpyOsgeoUtil.convert_point_to_dict(point_path)
        points = list(map(lambda x: (x['lon'], x['lat']), point_info))
        point_cluser_res = DbscanUtil.cluser_saptial_point(points, eps, min_samples=min_samples)
        point_dict = dict(list(map(lambda x: ((x['lon'], x['lat']), x), point_info)))

        points_new = []
        for each_cluser_type in point_cluser_res:
            # 对于孤立点特殊处理
            if each_cluser_type == -1:
                for each_point in point_cluser_res[each_cluser_type]:
                    each_point_new = point_dict[each_point]
                    each_point_new['is_single'] = '1'
                    points_new.append(each_point_new)
            else:
                # 得到中心经纬度
                lons = list(map(lambda x: float(x[0]), point_cluser_res[each_cluser_type]))
                lats = list(map(lambda x: float(x[1]), point_cluser_res[each_cluser_type]))
                each_point_new = point_dict[point_cluser_res[each_cluser_type][0]]  # 使用第一个的属性
                each_point_new['lon'], each_point_new['lat'] = np.mean(lons), np.mean(lats)
                each_point_new['is_single'] = '0'
                points_new.append(each_point_new)

        # 输出点
        ArcpyOsgeoUtil.create_points_from_dict(points_new, save_path)


if __name__ == '__main__':

    point_shp = r'C:\Users\Administrator\Desktop\modis\data\fire_point\MODIS_C6_Russia_and_Asia_24h.shp'
    res_shp = r'C:\Users\Administrator\Desktop\modis\cluser\new_cluser_point.shp'
    DbscanUtil.cluser_point_shp(point_shp, res_shp, 0.0241, 2)
