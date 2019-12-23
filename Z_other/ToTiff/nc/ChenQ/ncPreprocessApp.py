# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import os
import datetime

a = []


def get_file(input_nc_path, time_info, type):
    """找到符合要求的文件"""

    file_list = []

    for file in os.listdir(input_nc_path):
        # 1.获取文件业务时间（起报时间、预报时间）
        if os.path.splitext(file)[1] == type:
            filetime = file.split('-')[-1][:10]

            # FIXME 根据文件的后缀，决定是用什么时间标准
            # 2.判断文件是否是世界时，采用对应的str
            if file.split('_')[8] == 'ASI':
                prd_time = time_info['UTC_str']
            else:
                prd_time = time_info['BJ_str']

            # FIXME 获取符合时间条件的文件
            # 3.根据判断条件获取所有文件
            if filetime == prd_time:
                print file
                file_list.append(os.path.join(input_nc_path, file))

    return file_list


def get_time_info(BJ_str):
    """将输入的当做北京时间，变为时间时，并将数据存放入字典"""

    # FIXME 将输入的 issue 当做北京时，对北京时 -8 得到世界时
    BJ_time = datetime.datetime(int(BJ_str[:4]), int(BJ_str[4:6]), int(BJ_str[6:8]), int(BJ_str[8:10]))
    UTC_time = (BJ_time - datetime.timedelta(hours=8))
    UTC_str = UTC_time.strftime('%Y%m%d%H')

    # WANGBIN
    BJ_str = BJ_str[0:10]
    # /WANGBIN  FIXME 将需要的时间放进字典，有时间结构，有字符串
    time_info = {'UTC_str':UTC_str,'UTC_time':UTC_time,'BJ_str':BJ_str,'BJ_time':BJ_time}
    return time_info


def get_outfile_path(file, out_absdir, BJ_str):
    '''
    :param file: 获取产品存放绝对路径并返回；out_absdir/年月/年月日/RT&NRT/DAY&HOR  例：out_absdir/201812/20181213/RT/DAY
    :param out_absdir:
    :param BJ_str:
    :return:
    '''
    # 取到文件产品时间之前，
    f_basename = os.path.basename(file)[:-13]
    out_reladir = BJ_str[:6] + os.sep + BJ_str[:8]
    if f_basename.find('NRT_') is -1:
        out_reladir = out_reladir + os.sep + 'RT'
    else:
        out_reladir = out_reladir + os.sep + 'NRT'
    if f_basename.find('_HOR') is -1:
        out_reladir = out_reladir + os.sep + 'DAY'
    else:
        out_reladir = out_reladir + os.sep + 'HOR'
    out_path = out_absdir + os.sep + out_reladir
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    geotif_name = f_basename + BJ_str + '.tif'
    out_geotif = out_path + os.sep + geotif_name
    return out_geotif

def nc_to_tif(nc_file, out_geotif, gdaltranslatePath):
    """
     nc 转为 tiff
    :param nc_file: nc 文件
    :param out_geotif: 输出文件
    :param gdaltranslatePath:  gdal exe 的路径
    :return:
    """
    
    processList = []
    
    # 通过gdal_translate把nc转为tif
    cmd = gdaltranslatePath + ' -a_srs WGS84 -of GTiff -sds ' + nc_file + ' ' + out_geotif

    print('-'*100)
    print(nc_file)
    a.append(nc_file)

    #cmd = 'C:/Python27/ArcGISx6410.3/Lib/site-packages/osgeo/gdal_translate.exe -a_srs WGS84 -of GTiff -sds ' + nc_file + ' ' + out_geotif
    os.system(cmd)
    
    outPrePath = os.path.split(out_geotif)[0]
    outPreNameNoExt = os.path.split(out_geotif)[1].split('.')[0]
    
    allFileList = os.listdir(outPrePath)
    if len(allFileList) == 0:
        return processList
    else:
        for f in allFileList:
            if outPreNameNoExt in f:
                processList.append(outPrePath+os.sep+f)
    return processList

def main(prd_date,input_nc_path1,input_nc_path2,out_absdir,temp_dir,gdaltranslatePath):
    """main 文件"""

    # 0.初始化，获取信息
    time_info = get_time_info(prd_date)  # FIXME 输入的是 issue

    # 1.获取文件夹下对应文件

    file_list = []
    file_list.extend(get_file(input_nc_path1, time_info, '.nc'))
    file_list.extend(get_file(input_nc_path2, time_info, '.nc'))


    # 2.将文件转为tif
    outList = []
    for file in file_list:

        # print('-'*100)

        # print file

        # 2.1获取输出tif的绝对路径， FIXME 按照北京时间进行命名
        out_geotif = get_outfile_path(file, out_absdir, time_info['BJ_str'])

        # 2.2cmd调用gdal_translate转为tif
        processList = nc_to_tif(file, out_geotif, gdaltranslatePath)
        # 更新输出数据
        outList.extend(processList)

    for each in a:
        print each


    return outList

