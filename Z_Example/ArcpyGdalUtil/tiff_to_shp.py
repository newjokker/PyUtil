# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from Report.ArcpyGdalUtil import ArcpyGdalUtil
from Report.ArcpyOsgeoUtil import ArcpyOsgeoUtil


tiff_path = r'C:\Users\Administrator\Desktop\del\mndwi_pro.tif'
shp_path = r'C:\Users\Administrator\Desktop\del\del_ningan\mndwi_pro.shp'


ArcpyGdalUtil.tiff_to_shp(tiff_path, shp_path)
