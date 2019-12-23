# -*- coding: utf-8 -*-
import numpy as np
import netCDF4
# from create_nc_tif import Create_tif
# from Quick_test_nc_grey import Quick_grey
from Z_other.ArcpyUtil.classification_zonal_statistics import CreateOgr

def create_txt():
    inputfile = curPath+r'\workspace\data'+r'\testdata.nc'  # FIXME 不使用传参的方式，直接在函数里面拼接路径
    outputfile = curPath+r'\workspace\data'+r'\xync.txt'
    dataset = 'nitrogendioxide_tropospheric_column'
    # 剔除了-9999
    # scanline Y 3245 & ground_pixel X 450
    file_info = netCDF4.Dataset( inputfile, mode='r')
    # 获取数据
    ntc = file_info.groups['PRODUCT'].variables[dataset][()]
    lon = file_info.groups['PRODUCT'].variables['longitude'][()]
    lat = file_info.groups['PRODUCT'].variables['latitude'][()]
    # 取出数据并转为一维数组
    z, row, col = ntc.shape
    ntc_arr = np.asarray(ntc).reshape((row * col))
    lon_arr = np.asarray(lon).reshape((row * col))
    lat_arr = np.asarray(lat).reshape((row * col))
    # 剔除-9999
    null_index = np.where((ntc_arr > 9.969209968386869047e+35) | (ntc_arr < 0))
    index = list(null_index[0])
    ntc_arr = np.delete(ntc_arr, index)
    lon_arr = np.delete(lon_arr, index)
    lat_arr = np.delete(lat_arr, index)
    # TROPOMI用的是标准单位，然而通用的是 10^15 molec./cm^2,所以要乘上系数6.02214x10^4来转换(6.02214e+4)
    ntc_arr = ntc_arr * (6.02214e+4)
    # 制作文本数据fid，lon，lat，value
    fid = np.array(range(len(ntc_arr))).tolist()
    ntc_arr_list = ntc_arr.tolist()
    lon_arr_list = lon_arr.tolist()
    lat_arr_list = lat_arr.tolist()
    all_arr = [fid, lon_arr_list, lat_arr_list, ntc_arr_list]
    all_arr = np.array(all_arr)
    all_arr = np.transpose(all_arr)
    all_arr = all_arr.tolist()
    a = [str(i).replace('[', '').replace(']', '').replace(' ', '') for i in all_arr]
    # 添加头文件
    with open(outputfile, 'w') as f:
        f.write('fid,lon,lat,value' + '\n')
    with open(outputfile, 'a') as f:
        s = '\n'.join(a)
        f.write(s)
    return outputfile


def create_point_new(inputfile, point_path):
    """ nc 数据转为矢量点"""

    file_info = netCDF4.Dataset(inputfile, mode='r')  # scanline Y 3245 & ground_pixel X 450
    dataset_str = 'nitrogendioxide_tropospheric_column'
    ntc = file_info.groups['PRODUCT'].variables[dataset_str][()].data.flatten()  # 获取数据
    lon = file_info.groups['PRODUCT'].variables['longitude'][()].data.flatten()
    lat = file_info.groups['PRODUCT'].variables['latitude'][()].data.flatten()

    null_index = np.where((ntc > 9.969209968386869047e+35) | (ntc < 0))  # 无效值
    ntc_arr = np.delete(ntc, null_index)
    lon_arr = np.delete(lon, null_index)
    lat_arr = np.delete(lat, null_index)

    # 转为字典结构，转为点
    point_array = np.column_stack((ntc_arr, lon_arr, lat_arr)).tolist()  # 合并转为列表

    point_info = []
    for each in point_array:
        point_info.append({'value': each[0], 'lon': each[1], 'lat': each[2]})

    CreateOgr.create_points_from_dict(point_info, point_path, lon_string='lon', lat_string='lat')  # 转 shp 点

if __name__ == '__main__':

    create_point_new(r'D:\Code\fengbo\workspace\data\testdata.nc', 1)


    # curPath = os.path.abspath(os.path.dirname(__file__))
    # #创建txt，包含fid、经度、纬度、value
    # create_txt = create_txt()
    # #要素转栅格
    # create_tif = Create_tif(create_txt)
    # filename = create_tif.create_tif()
    # #快视图灰度
    # quick_grey = Quick_grey(curPath,filename)
    # quick_grey.quick_grey()



