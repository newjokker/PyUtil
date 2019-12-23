# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
* 修改分级个数（√）
* 修改分级的标签名字（√）
* 修改分级的颜色（×）
"""


import arcpy

mxd = arcpy.mapping.MapDocument(r'D:\Code\Util_Util\ArcpyUtil\class_color\data\1.mxd')
df = arcpy.mapping.ListDataFrames(mxd, 'layers')[0]
lyr = arcpy.mapping.ListLayers(mxd, "tiffFile", df)[0]

print(lyr.symbologyType)

if lyr.symbologyType == "RASTER_CLASSIFIED":
    lyr.symbology.classBreakValues = [0.1, 0.2, 0.5, 0.6, 0.7,0.8,0.9]
    lyr.symbology.classBreakLabels = [u'第一个级别',u'1-2',u'2-3',u'3-4',u'4-5', u'最后一个级别']   # 更改标签

arcpy.mapping.ExportToJPEG(mxd, r'C:\Users\Administrator\Desktop\123.jpg')
del mxd, lyr
