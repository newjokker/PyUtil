# -*- coding: utf-8 -*-
# author：ChenQiang 
# time:2019/12/5 0005

import numpy as np
import rasterio
# from rasterio.mask import mask
from shapely.geometry import box
import geopandas as gpd
from fiona.crs import from_epsg

import glob
from scipy.io import loadmat
from GdalUtil.GdalBase import GdalBase

from osgeo import gdal


def readFile(filename):
    filehandle = gdal.Open(filename)
    band1 = filehandle.GetRasterBand(1)
    geotransform = filehandle.GetGeoTransform()
    geoproj = filehandle.GetProjection()
    Z = band1.ReadAsArray()
    xsize = filehandle.RasterXSize
    ysize = filehandle.RasterYSize
    return xsize,ysize,geotransform,geoproj,Z,band1



def writeFile(filename,geotransform,geoprojection,data,NoDataValue=-9999):
    (x,y) = data.shape
    format = "GTiff"
    driver = gdal.GetDriverByName(format)
    # you can change the dataformat but be sure to be able to store negative values including -9999
    dst_datatype = gdal.GDT_Float32
    dst_ds = driver.Create(filename,y,x,1,dst_datatype)
    dst_ds.GetRasterBand(1).WriteArray(data)
    dst_ds.SetGeoTransform(geotransform)
    dst_ds.SetProjection(geoprojection)
    dst_ds.GetRasterBand(1).SetNoDataValue(NoDataValue)
    return 1