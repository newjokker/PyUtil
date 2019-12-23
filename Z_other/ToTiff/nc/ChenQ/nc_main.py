# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import datetime
import os
from Z_other.ToTiff import main
import time

def doInnerPy():
    """执行内部的py模块时必须重写 算法输出存储至self.rsOutMap"""

    # FIXME 获取 issus
    # issue = self.pluginParam.getInputInfoByKey('issue')
    issue = '201907012300'
    # #huxuran
    # if issue[-4:]<'0800':
    #     inputTime = datetime.datetime.strptime(issue[0:4]+'-'+issue[4:6]+'-'+issue[6:8], '%Y-%m-%d')
    #     delta = datetime.timedelta(days=1)
    #     n_days = inputTime - delta
    #     strTime = n_days.strftime('%Y%m%d')+'0000'
    #     nc_inputpath = self.pluginParam.getInputInfoByKey('inputFile') + os.sep + strTime[0:8]
    # else:
    #     nc_inputpath = self.pluginParam.getInputInfoByKey('inputFile') + os.sep + issue[0:8]

    # 2019-6-26
    # 由于世界时和北京时的原始NC数据存在同一文件夹下，因此当期号为0-8北京时的时候出现跨文件夹情况
    issueTime = datetime.datetime.strptime(issue[0:4] + '-' + issue[4:6] + '-' + issue[6:8], '%Y-%m-%d')
    delta = datetime.timedelta(days=1)
    yestodayTime = issueTime - delta

    # FIXME 传入的数据, nc 数据所在的主文件夹，拼起来得到 nc 源文件的文件夹，
    input_path = r'D:\BaiduNetdiskDownload'
    # nc_inputpath1 = os.path.join(self.pluginParam.getInputInfoByKey('inputFile'), issue[0:8])
    # nc_inputpath2 = os.path.join(self.pluginParam.getInputInfoByKey('inputFile'), yestodayTime.strftime('%Y%m%d'))
    nc_inputpath1 = os.path.join(input_path, issue[0:8])
    nc_inputpath2 = os.path.join(input_path, yestodayTime.strftime('%Y%m%d'))

    # FIXME 输出文件夹，
    # out_absdir = self.pluginParam.getInputInfoByKey('outFolder')
    out_absdir = r'C:\Users\Administrator\Desktop\NC\out'
    # tempDir = self.tempFolder
    tempDir = r'C:\Users\Administrator\Desktop\NC\temp'

    # FIXME 获取 exe 的路径 ， C:/Python27/ArcGISx6410.3/Lib/site-packages/osgeo/gdal_translate.exe
    # gdaltranslatePath = self.pluginParam.getInputInfoByKey('gdal_translate')
    gdaltranslatePath = r'C:\Python27\ArcGIS10.5\Lib\site-packages\osgeo\gdal_translate.exe'
    preResultList = main(issue, nc_inputpath1, nc_inputpath2, out_absdir, tempDir, gdaltranslatePath)  # FIXME 这边是传入了临时文件夹的，







if __name__ == "__main__":

    start = time.time()

    doInnerPy()


    stop = time.time()

    print(stop - start)
