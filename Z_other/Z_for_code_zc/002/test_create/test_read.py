# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from Report.GdalUtil import CreateOgr, GdalBase


point_shp = r'D:\Code\Util_Util\Z_for_code_zc\002\data\factory.shp'
polygon_shp = r'D:\Code\Util_Util\Z_for_code_zc\002\data\test_001.shp'

# point_info = CreateOgr.convert_point_to_dict(point_shp)
polygon_info = CreateOgr.convert_polygon_to_dict(point_shp)


for each in point_info:
    print(each)
