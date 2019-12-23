# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from Report import ArcpyGdalUtil


tiff_path = r'C:\Users\Administrator\Desktop\aa\SEAAOD_201911011045.tif'
out_tiff_path = r'C:\Users\Administrator\Desktop\aa\out.tif'

# no_data_value = ArcpyGdalUtil.get_no_data_value(tiff_path)
# print(no_data_value)
#
# im_data = ArcpyGdalUtil.read_tiff(tiff_path)[0]
# print(im_data)
# ArcpyGdalUtil.set_no_data_value(tiff_path, -999, res_format='GTiff', out_tiff_path=out_tiff_path)

import numpy as np

im_data = ArcpyGdalUtil.read_tiff(tiff_path)[0]
im_data[np.isnan(im_data)] = -999
ArcpyGdalUtil.set_array_data(tiff_path, im_data, out_tiff_path=out_tiff_path)
