# -*- coding: utf-8 -*-

import arcpy
import os
import sys


class Create_tif():
    def __init__(self, filePath):
        self.filePath = filePath  # 文件路径

    # 清空文件夹下所有文件
    def del_file(self,dir_path):
        for i in os.listdir(dir_path):
            path_file = os.path.join(dir_path, i)
            if os.path.isfile(path_file):
                os.remove(path_file)
            else:
                self.del_file(path_file)

    # 寻找投影文件
    def file_path(self,file_dir):
        path_list = []
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                if os.path.splitext(file)[1] == '.prj':
                    path_list.append(os.path.join(root, file))
        return path_list

    def create_tif(self):
        path, filename = os.path.split(sys.argv[0])
        workspace = path + '/workspace'
        output_dir = path + '/workspace/outfile'
        proj_wgs1984 = self.file_path(workspace + '/WGS1984')[0]
        proj_Albers = self.file_path(workspace + '/Albers')[0]
        arcpy.env.workspace = workspace
        input_file = self.filePath
        output_name = input_file.split("\\")[-1].split('.')[0]

        # 清空文件夹
        self.del_file(output_dir)
        spatRef = arcpy.SpatialReference(proj_wgs1984)
        createFC = arcpy.CreateFeatureclass_management(output_dir, output_name + '.shp', 'POINT', '', '', '', spatRef)
        arcpy.AddField_management(output_dir + '\\' + output_name + '.shp', 'NAME', 'LONG', 10)
        arcpy.AddField_management(output_dir + '\\' + output_name + '.shp', 'VALUE', 'DOUBLE', 20, 20)
        iflds = ['NAME', 'SHAPE@XY', 'VALUE']
        # iCur = arcpy.da.InsertCursor(createFC, iflds)
        iCur = arcpy.da.InsertCursor(output_dir + "\\" + output_name + '.shp', iflds)
        count = 1
        try:
            for ln in open(input_file, 'r').readlines():
                if count > 1:
                    dataList = ln.split(',')
                    value = dataList[3]
                    lat = dataList[2]
                    lon = dataList[1]
                    id = dataList[0]
                    ivals = [id, (float(lon), float(lat)), float(value)]
                    iCur.insertRow(ivals)
                count += 1
            del iCur
        except BaseException:
            print "存在异常"
        #点转栅格
        arcpy.FeatureToRaster_conversion(output_dir + '/' + output_name + '.shp', 'VALUE', output_dir + '/' + output_name + '.tif', 0.1)
        #栅格投影
        arcpy.ProjectRaster_management(output_dir + '/' + output_name + '.tif', output_dir + '/' + output_name + '_Albers.tif', proj_Albers)
        output_path = output_dir + '/' + output_name + '_Albers.tif'
        return output_path

