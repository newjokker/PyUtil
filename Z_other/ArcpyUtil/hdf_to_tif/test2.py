# -*- coding: cp936 -*-
import arcpy



arcpy.env.overwriteOutput = 1
arcpy.CheckOutExtension("Spatial")
inPath= r'C:\Users\lingdequan\Desktop\test\\'
arcpy.env.workspace = inPath


hdf = r"C:\Users\lingdequan\Desktop\test\MOD13Q1.A2000049.h26v05.006.2015136104818.hdf"
eviName= r"C:\Users\lingdequan\Desktop\test\0000" + ".tif"
data1=arcpy.ExtractSubDataset_management(hdf, eviName, "0")

eviName= r"C:\Users\lingdequan\Desktop\test\7777" + ".tif"
data1=arcpy.ExtractSubDataset_management(hdf, eviName, "7")

print "完成"
