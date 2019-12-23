# -*- coding: utf-8 -*-
import numpy as np
import netCDF4

#flip90_right将图像（0，0）点从右上角换到左下角
def flip90_right(arr):
    new_arr = arr.reshape(arr.size)
    new_arr = new_arr[::-1]
    new_arr = new_arr.reshape(arr.shape)
    new_arr = np.transpose(new_arr)[::-1]
    new_arr = np.transpose(new_arr)
    return new_arr
#scanline Y 3245 & ground_pixel X 450
file_info = netCDF4.Dataset('D:/pyitem/kuangda/data/test_data/nc/data.nc',mode='r')
#print file
#获取对流层NO2垂直柱浓度
ntc=file_info.groups['PRODUCT'].variables['nitrogendioxide_tropospheric_column'][()]
#获取全经度数据
lon = file_info.groups['PRODUCT'].variables['longitude'][()]
#获取全纬度数据
lat = file_info.groups['PRODUCT'].variables['latitude'][()]
#获取左下角经纬度
lon_min=file_info.geospatial_lon_max
lat_min=file_info.geospatial_lat_min
#取出数据并转为二维数组
z,row,col=ntc.shape
ntc_arr = np.asarray(ntc).reshape((row,col))
lon_arr = np.asarray(lon).reshape((row,col))
lat_arr = np.asarray(lat).reshape((row,col))
#获取xllcorner（lon_arr_min）和yllcorner（lat_arr_min）
lon_arr_min=min(min(lon_arr.tolist()))
lat_arr_min=min(min(lat_arr.tolist()))

#上下翻转数组
ntc_arr = flip90_right(ntc_arr)
#替换数组中的值
ntc_arr[ntc_arr >= 9.969209968386869047e+35] = -9999
#制作tif文本文件
np.savetxt('D:/pyitem/kuangda/data/test_data/nc/test1.txt',ntc_arr)
fp = file('D:/pyitem/kuangda/data/test_data/nc/test1.txt')
lines = []
for line in fp:
    lines.append(line)
fp.close()
#插入头文件
lines.insert(0, '''ncols         450
nrows         3245
xllcorner     -179.99826
yllcorner     -89.956314
cellsize      0.01
NODATA_value  -9999
''')  # 在第一行插入
s = ''.join(lines)
fp = file('D:/pyitem/kuangda/data/test_data/nc/test1.txt', 'w')
fp.write(s)
fp.close()
pass