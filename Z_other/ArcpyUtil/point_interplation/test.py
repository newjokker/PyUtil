# -- coding: utf-8 --

import os
import arcpy

def init_arcpy():
    arcpy.CheckOutExtension("3D")
    arcpy.CheckOutExtension("spatial")
    arcpy.env.workspace = r"C:\work_code\arcpy_util\txt2point\temp"
    arcpy.env.overwriteOutput = True
    print("* 初始化 Arcpy 运行环境")

def point_interpolation(rainPoint, border, rainTif):
    """ 将降水点数据(shp)插值为面数据(tif) """

    #【1】InterPolation
    tempInterRainTif = r'tempRainTif.tif'
    # extenction = arcpy.Extent(24, 103, 30, 110)  # XMin、YMin、XMax、YMax ; 24, 103, 30, 110
    arcpy.env.extent = border
    outIDW = arcpy.sa.Idw(rainPoint, "PRE_Time_2")
    outIDW.save(tempInterRainTif)
    #【2】插值结果裁边
    extractResult = arcpy.sa.ExtractByMask(tempInterRainTif, border)
    extractResult.save(rainTif)
    print("* 插值站点降水数据")


if __name__ == "__main__":
    # 好像读取的 txt 必须要隔一行空一行

    # FIXME 插值的问题已解决，投影要了我的命了，后来发现，本来边界就是不一样大，因为一个是流域，一个是行政边界，流域的面积就是要大一些
    # FIXME （1）能得到点但是不能插值，因为 降水量没有设为 float 类型的，自动识别为 str；（2）extent 范围设置有问题（3）插值的字段的名字错了，arcgis 会自动减少名字长度

    init_arcpy()

    point = r".\data\point\point1.shp"
    border = r".\data\border\gz_border.shp"
    resultTif = r".\result\result.tif"

    point_interpolation(point, border, resultTif)

    print("ok")