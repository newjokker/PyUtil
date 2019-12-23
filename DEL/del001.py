# -*- coding: utf-8  -*-
# -*- author: jokker -*-


from Report.ArcpyGdalUtil import ArcpyGdalUtil

tiff_path = r'C:\Users\Administrator\Desktop\del\bl\data\NDVI_FY3D_MERSI_201908120000.tif'
out_tiff_path = r'C:\Users\Administrator\Desktop\del\bl\res\123.tif'

ArcpyGdalUtil.set_no_data_value(tiff_path, no_data_value=-9999, res_format='GTiff', out_tiff_path=out_tiff_path)

