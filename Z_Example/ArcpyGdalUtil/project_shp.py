# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from Report.ArcpyOsgeoUtil import ShpProjectUtil

shp_path = r'C:\Users\Administrator\Desktop\ArcpyUtilGdal\data\shi.shp'

ShpProjectUtil.project_shp(shp_path, 'test')

