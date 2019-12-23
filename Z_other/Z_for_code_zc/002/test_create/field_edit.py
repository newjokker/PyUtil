# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from Report.ArcpyOsgeoUtil import ArcpyOsgeoUtil

"""
当客户提供的数据不符合规范，难以直接用 Arcgis 直接对属性进行编辑的时候，就可以使用这个属性编辑功能
"""

shp_path = r'E:\Algorithm\Util_Util\Z_for_code_zc\002\data\test_001.shp'

# 获取字段名
field_names = ArcpyOsgeoUtil.get_field_name(shp_path)  # 当不确定将要打开的 shp 的属性表内容，可以先读取属性名
# # 获取属性
field_info = ArcpyOsgeoUtil.get_field(shp_path, ['lon', 'lat'], need_line=[0, 3, 5])
# 增加属性
# ArcpyOsgeoUtil.add_field(shp_path, 'grade', field_value_list=list(map(lambda x: str(x % 6), range(len(field_info)))))
# ArcpyOsgeoUtil.add_field(shp_path, 'grade_2', field_value_list=['1','2','3'])
# 删除属性
# ArcpyOsgeoUtil.delete_field(shp_path, ['grade', 'grade_2'])

for each in field_info:
    print(each)





