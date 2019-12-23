# -*- coding: utf-8  -*-
# -*- author: jokker -*-


from Report.ArcpyGdalUtil import ArcpyGdalUtil
from Report.DecoratorUtil import DecoratorUtil

@DecoratorUtil.time_this
def ok():
    tiff_path = r'C:\Users\Administrator\Desktop\del\del\rastercalc91.tif'
    save_path = r'C:\Users\Administrator\Desktop\del\del\plaque.tif'
    ArcpyGdalUtil.get_plaque(tiff_path, save_path)

ok()
