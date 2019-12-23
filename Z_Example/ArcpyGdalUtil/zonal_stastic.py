# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from Report.ArcpyGdalUtil import ArcpyGdalUtil

temp_path = r'C:\Users\Administrator\Desktop\del\deldel'
a = ArcpyGdalUtil(temp_path)  # 实例化
tiff_path = r'C:\Users\Administrator\Desktop\New_frm_wprd\data\grass.tif'
shp_path = r'D:\Code\Frame_Jokker\Code\Depend\QingHai\CompShp\AreaCity.shp'
grade = [0, 10, 20, 50, 100, 200]
field_name = r'ID'

res_region, res_region_class_format = a.zonal_stastic(tiff_path, shp_path, grade, field_name)

print('ok')
