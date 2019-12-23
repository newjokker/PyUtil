# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from Z_other.ArcpyUtil.MappingUtil.Mapping import MappingPicture

# mxd_path = r'D:\Code\FireDetectionH8\algorithm\AuxData\MXD\zoom.mxd'
mxd_path = r'C:\Users\Administrator\Desktop\123456.mxd'

a = MappingPicture(mxd_path)
a.resolution = 300
a.pic_type = 'png'
a.replace_layer_info = {
    # 'mir.tif': r'C:\Users\Administrator\Desktop\H8\temp\a0224040-5c02-11e9-8db4-6c4b905b11db\enhance_B07.tif',
    'FirePoint': r'C:\Users\Administrator\Desktop\H8\temp\a0224040-5c02-11e9-8db4-6c4b905b11db\point_city_info.shp',
    # 'rgb.tif': r'C:\Users\Administrator\Desktop\H8\temp\a0224040-5c02-11e9-8db4-6c4b905b11db\background_rgb.tif',
                        }
# a.page_row_info = {'code': 'xiancode', 'name': 'xianname', 'shengname': 'shengname'}
# a.text_element_info = {'123': {'0': u'呵呵', '11': '123', '202': '234', 'jokker': u'凌德泉'}}
a.save_folder = r'C:\Users\Administrator\Desktop'
a.save_name = '001456'
# 指定数据框范围
a.assign_extent = {'loc_x': 101, 'loc_y': 21.78, 'length': 1.2}

a.do_process()


# import arcpy.mapping as mapping
#
# # 引用当前活动的地图文档
# mxd = mapping.MapDocument("CURRENT")
# # 获取对Layers(所有图层在数据框下面)数据框的引用。
# df = mapping.ListDataFrames(mxd, "Layers")[0]
# # 定义参考图层
# refLayer = arcpy.mapping.ListLayers(mxd, "Burglaries*", df)[0]
# # 定义相对于参考图层的插入图层
# insertLayer = arcpy.mapping.Layer(r"C:\ArcpyBook\data\CityOfSanAntonio.gdb\Crimes2009")
# # 插入图层
# mapping.InsertLayer(df,refLayer,insertLayer,"BEFORE")
#
#
