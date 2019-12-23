# -*- coding: cp936 -*-


from  __future__ import division
from pyhdf.SD import SD,SDC
import pprint 


hdf_name = r'C:\Users\lingdequan\Desktop\FY3B_MWRIX_GBAL_L2_SWE_MLT_ESD_20160101_AOAD_025KM_MS.HDF'

hdf_name = r"C:\Users\lingdequan\Desktop\MOD13Q1.A2000049.h26v05.006.2015136104818.hdf"
print ('file found {}'.format(hdf_name))

hdf_obj = SD(hdf_name)
print (hdf_obj.info())

data_dic = hdf_obj.datasets()
for idx,sds in enumerate(data_dic.keys()):
	print (idx,sds)

Map = hdf_obj.select('250m 16 days NDVI')
data = Map.get()


print(data)


print("-"*50)

Map = hdf_obj.select('250m 16 days EVI')
data = Map.get()



print(data)


import arcpy





outRaster = arcpy.NumPyArrayToRaster(data)

arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("WGS 1984 UTM Zone 18N")
outRaster.save(r"C:\Users\lingdequan\Desktop\test\12345.tif")


print(outRaster)


