# # -*- coding: utf-8  -*-
# # -*- author: jokker -*-
#
# """
# 袁小琪贡献，等到集成，将数据转为点，再将点插值为 tiff 即可
# """
#
# import h5py
# import gdal
# import os
# import sys
# import arcpy
# from arcpy import env
# from arcpy.sa import *
# from arcpy import sa
# import cmd
#
#
# def ListtoTXT(list_name, ident_name, txt_name):
#     file = open(txt_name, 'w')
#     create_envi_head = 'Lon,Lat,' + ident_name + '\n'
#     file.write(create_envi_head)
#     for i in range(len(list_name)):
#         str_data = str(list_name[i][0]) + ',' + str(list_name[i][1]) + ',' + str(list_name[i][2]) + '\n'
#         file.write(str_data)
#     file.close()
#
#
# def TXTtoIDW(ident_name, txt_name, out_Layer_name, shp_name, tif_Name, tempPath):
#     if not os.path.exists(shp_name):
#         geoPrj = os.path.join(os.path.dirname(__file__), 'GCS_WGS_1984.prj')
#         arcpy.MakeXYEventLayer_management(txt_name, "lon", "lat", out_Layer_name, geoPrj, "")
#         arcpy.CopyFeatures_management(out_Layer_name, shp_name, "", "0", "0", "0")
#     #     env.workspace =tempPath+'\\'
#     #     arcpy.env.extent ="114.876586897476 29.395559287302 119.646586897476 34.655559287302"
#     #     outIDW = Idw(shp_name, ident_name, "0.01", "","")
#     outIDW = Idw(shp_name, ident_name, "0.1", "", RadiusFixed(0.4, 0))
#     outIDW.save(tif_Name)
#     return tif_Name
#
#
# def getTif(tifData, tifName):
#     # 将计算好的NDVI保存为GeoTiff文件
#     gtiff_driver = gdal.GetDriverByName('GTiff')
#     # 输出文件名
#     out_data = gtiff_driver.Create(tifName,
#                                    tifData.shape[1], tifData.shape[0], 1, gdal.GDT_Float32)
#     # 将NDVI数据坐标投影设置为原始坐标投影
#
#     #     out_data.SetProjection(indata.GetProjection())
#     #     out_data.SetGeoTransform(indata.GetGeoTransform())
#     out_band = out_data.GetRasterBand(1)
#     out_band.WriteArray(tifData)
#     out_band.FlushCache()
#
#
# if __name__ == '__main__':
#     inPutFile = r'E:\jsmi\ocean\test2_n.h5'
#     tempPath = r'E:/jsmi/ocean/temp'
#     outPutPath = r'E:/jsmi/ocean/result'
#     issue = '201810100000'
#     f = h5py.File(inPutFile, 'r')
#     lat = f['latitude'][:]  # 纬度
#     lon = f['longitude'][:]  # 经度
#     #     SST = f['data_fields']['Res0_Retrieve_Swath_Fast_Product']['Res0_SST'][:]#海温
#     SST = f['WS'][:]
#     f.close()
#     cmd = 'C:\Python27\ArcGIS10.3\Lib\site-packages\osgeo\gdal_translate.exe -a_srs WGS84 -of GTiff -sds ' + inPutFile + ' ' + outPutPath
#     os.system(cmd)
#
#     SST_list = []
#     min_list = []
#     for x in range(SST.shape[0]):
#
#         data = []
#         data.append(lon[x])
#         data.append(lat[x])
#         data.append(SST[x])
#         #             if  SST[x,y] > 0 and lon[x,y]*1e-6<132 and lon[x,y]*1e-6 > 116 and lat[x,y]*1e-6<38 and lat[x,y]*1e-6 >18:
#         SST_list.append(data)
#         if SST[x] > 0:
#             min_list.append(SST[x] * 0.01)
#     minvalue = min(min_list)
#     txt_name = tempPath + os.sep + 'SST_data1.txt'
#     out_Layer_name = "'" + issue + "_SST_shp1'"
#     shp_name = tempPath + '\\' + issue + '_SST_station1.shp'
#     tif_Name_nonull = tempPath + '\\' + issue + '_SST1.tif'
#     tif_Name_all = tempPath + '\\' + issue + '_SST_all1.tif'
#     tif_Name = outPutPath + '\\' + issue + '_SST1.tif'
#     ListtoTXT(SST_list, 'SST1', txt_name)
#     TXTtoIDW('SST1', txt_name, out_Layer_name, shp_name, tif_Name_nonull, tempPath)
#
#     tif_null = SetNull(tif_Name_nonull, tif_Name_nonull, 'VALUE < ' + str(minvalue))
#     tif_null.save(tif_Name)
#     #     fileShp = r'E:\htht\JS_MI\Depend\jiangsu\worldshp\Worldnew.shp'
#     # #     outExtractByMask = sa.ExtractByMask(tif_Name_all, fileShp)
#     # #     outExtractByMask.save(tif_Name)
#     #     arcpy.Clip_management(tif_Name_all, fileShp, tif_Name_all,"#", "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
#
#     print 'success'