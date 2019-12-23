# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from math import *
import numpy as np

# 计算像元经纬度距离
def haversine(lon, lat, dlon, dlat):
    # 将十进制度数转化为弧度
    lon, lat, dlon, dlat = (np.radians(iparam) for iparam in (lon, lat, dlon, dlat))
    # haversine公式
    a = np.sin(dlat / 2) ** 2 + np.cos(lat) * np.cos(lat + dlat) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371.393  # 地球平均半径，单位为公里
    return c * r

def pixArea(lon, lat, res_x, res_y):
    """经度、纬度、经向分辨率、纬向分辨率，返回像元面积"""
    # 面积可以近似看作经、纬度方向的距离之积
    return haversine(lon, lat, res_x, 0) * haversine(lon, lat, 0, res_y)


if __name__ == '__main__':

    lon = np.array([110, 100.2, 100.5])
    lat = np.array([35, 30.2, 30.3])

    # area = pixArea(110, 35, 0.01, 0.01)
    area = pixArea(lon, lat, 0.01, 0.01)
    print(area)
