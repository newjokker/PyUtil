# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import os
import uuid
import time
import math
import shutil
import numpy as np
import gdal
import osr
import cv2
from collections import defaultdict
from multiprocessing import Pool

from algorithm.Function.GdalUtil.GdalBase import GdalBase
from algorithm.FireProcess.fire_config import ConfigPara

# from Function.GdalUtil.GdalBase import GdalBase
# from FireProcess.fire_config import ConfigPara


class FireMonitorProcessH8(object):

    @staticmethod
    def output_raster(tiff_dir, fire_data, tiff_geotrans, tiff_proj):
        # 给文件赋名
        if 'int8' in fire_data.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in fire_data.dtype.name:
            datatype = gdal.GDT_UInt16
        else:
            datatype = gdal.GDT_Float64

        driver = gdal.GetDriverByName("GTiff")  # 存的数据格式
        dataset = driver.Create(tiff_dir, fire_data.shape[1], fire_data.shape[0], 1, datatype)
        dataset.SetGeoTransform(tiff_geotrans)  # 写入仿射变换参数
        dataset.SetProjection(tiff_proj)  # 写入投影
        dataset.GetRasterBand(1).WriteArray(fire_data)
        del dataset

    @staticmethod
    def SolarAngles(year, month, day, hour, minute, second, timezone, longitude, latitude):
        # year, month, day, hour, minute, second, timezone, longitude, latitude = getParams(paramsDict)
        # #
        JD0 = int(365.25 * (year - 1)) + int(30.6001 * (1 + 13)) + 1 + hour / 24 + 1720981.5
        if month <= 2:
            JD2 = int(365.25 * (year - 1)) + int(30.6001 * (month + 13)) + day + hour / 24 + 1720981.5
        else:
            JD2 = int(365.25 * year) + int(30.6001 * (month + 1)) + day + hour / 24 + 1720981.5
        # 年积日 Day of year
        J = JD2 - JD0 + 1
        #     print J

        dayang = 360.0 * (J - 1) / 365.0
        # ;    /* Earth radius vector * solar constant = solar energy */
        # ;        /*  Spencer, J. W.  1971.  Fourier series representation of the
        # ;            position of the sun.  Search 2 (5), page 172 */
        sd = math.sin(dayang / 180. * math.pi)
        cd = math.cos(dayang / 180. * math.pi)
        d2 = 2.0 * dayang
        c2 = math.cos(d2 / 180. * math.pi)
        s2 = math.sin(d2 / 180. * math.pi)

        erv = 1.000110 + 0.034221 * cd + 0.001280 * sd
        erv = erv + 0.000719 * c2 + 0.000077 * s2
        interval = 0
        utime = hour * 3600.0 + minute * 60.0 + second - interval / 2.0
        utime = utime / 3600.0 - timezone

        delta = year - 1949
        leap = int(delta / 4.0)
        julday = 32916.5 + delta * 365.0 + leap + J + utime / 24.0

        ectime = julday - 51545.0

        mnlong = 280.460 + 0.9856474 * ectime

        mnlong = mnlong - 360.0 * int(mnlong / 360.0)
        if mnlong < 0.0:
            mnlong = mnlong + 360.0

        mnanom = 357.528 + 0.9856003 * ectime
        # /* (dump the multiples of 360, so the answer is between 0 and 360) */
        mnanom = mnanom - 360.0 * int(mnanom / 360.0)
        if (mnanom < 0.0):
            mnanom = mnanom + 360.0

        # ;    /* Ecliptic longitude */
        # ;        /*  Michalsky, J.  1988.  The Astronomical Almanac's algorithm for
        # ;            approximate solar position (1950-2050).  Solar Energy 40 (3),
        # ;            pp. 227-235. */
        eclong = mnlong + 1.915 * math.sin(mnanom / 180. * math.pi) + 0.020 * math.sin(2.0 * mnanom / 180. * math.pi)

        # ;    /* (dump the multiples of 360, so the answer is between 0 and 360) */
        eclong -= 360.0 * int(eclong / 360.0)
        if (eclong < 0.0):
            eclong = eclong + 360.0

        ecobli = 23.439 - 4.0e-07 * ectime

        declin = 180 / math.pi * math.asin(math.sin(ecobli / 180. * math.pi) * math.sin(eclong / 180. * math.pi))

        top = math.cos(math.pi / 180 * ecobli) * math.sin(math.pi / 180 * eclong)
        bottom = math.cos(math.pi / 180 * eclong)

        rascen = 180 / math.pi * math.atan2(top, bottom)

        if (rascen < 0.0):
            rascen = rascen + 360.0

        gmst = 6.697375 + 0.0657098242 * ectime + utime

        # ;    /* (dump the multiples of 24, so the answer is between 0 and 24) */
        gmst -= 24.0 * int(gmst / 24.0)
        if (gmst < 0.0):
            gmst += 24.0

        # ;    /* Local mean sidereal time */
        # ;        /*  Michalsky, J.  1988.  The Astronomical Almanac's algorithm for
        # ;            approximate solar position (1950-2050).  Solar Energy 40 (3),
        # ;            pp. 227-235. */
        lmst = gmst * 15.0 + longitude

        # ;    /* (dump the multiples of 360, so the answer is between 0 and 360) */
        lmst -= 360.0 * int(lmst / 360.0)
        if (lmst < 0.):
            lmst += 360.0

        # ;    /* Hour angle */
        # ;        /*  Michalsky, J.  1988.  The Astronomical Almanac's algorithm for
        # ;            approximate solar position (1950-2050).  Solar Energy 40 (3),
        # ;            pp. 227-235. */
        hrang = lmst - rascen

        # ;    /* (force it between -180 and 180 degrees) */
        if (hrang < -180.0):
            hrang += 360.0
        elif (hrang > 180.0):
            hrang -= 360.0

        cd = math.cos(math.pi / 180 * declin)
        ch = math.cos(math.pi / 180 * hrang)
        cl = math.cos(math.pi / 180 * latitude)
        sd = math.sin(math.pi / 180 * declin)
        sl = math.sin(math.pi / 180 * latitude)

        cz = sd * sl + cd * cl * ch

        # ;    /* (watch out for the roundoff errors) */
        if (abs(cz) > 1.0):
            if (cz >= 0.0):
                cz = 1.0
            else:
                cz = -1.0
        zenetr = math.acos(cz) * 180 / math.pi

        # ;    /* (limit the degrees below the horizon to 9 [+90 -> 99]) */
        if (zenetr > 99.0):
            zenetr = 99.0
        elevetr = 90.0 - zenetr

        # CNQ 不每次重复计算卫星方位角，使用固定文件代替-----------------------------------------------------------------------
        # ce = math.cos(math.pi / 180 * elevetr)
        # se = math.sin(math.pi / 180 * elevetr)
        #
        # azim = 180.0
        # cecl = ce * cl
        # if (abs(cecl) >= 0.001):
        #     ca = (se * sl - sd) / cecl
        #     if (ca > 1.0):
        #         ca = 1.0
        #     elif (ca < -1.0):
        #         ca = -1.0
        #     azim = 180.0 - math.acos(ca) * 180 / math.pi
        #     if (hrang > 0):
        #         azim = 360.0 - azim
        #
        # zenith = (90 - elevetr)
        # azimuth = azim
        # return azimuth, elevetr
        # --------------------------------------------------------------------------------------------------------------
        return elevetr

    @staticmethod
    def fire_monitor_H8(day_or_night, all_band, checkable_mask, cfg_xml_info, cloud_mask, tif_aux_tuple):
        """# 计算背景温度时选用不同卷积核的大小
        kernel_shp = [3, 5, 7, 9, 11]  # 2KM
        # kernel_shp = [7,9,11,13,15,17,19] # 1KM

        # 火点判断系数
        refine_mir_fire = 3.5
        refine_m_f_fire = 3

        # 云判断阈值
        Th_p1 = 0.9
        Th_p2 = 0.7
        Th_t1 = 265
        Th_t2 = 285

        # 云边缘和荒漠边缘影响判识阈值
        Th_cloud_desert = 8

        # 水体阈值
        Th_p3 = 0.15

        # 火情判断阈值
        Th_t7 = 320 # 白天背景像元中背景火点像元的BT_04判断阈值
        Th_t8 = 295 # 夜间背景像元中背景火点像元的BT_04判断阈值
        Th_dt2 = 20 # 白天背景像元中背景火点像元的D_BT_04_11判断阈值
        Th_dt3 = 10 # 夜间背景像元中背景火点像元的D_BT_04_11判断阈值
"""

        Th_t7 = 310 # 白天背景像元中背景火点像元的BT_04判断阈值
        Th_t8 = 295 # 夜间背景像元中背景火点像元的BT_04判断阈值
        Th_dt2 = 20 # 白天背景像元中背景火点像元的D_BT_04_11判断阈值
        Th_dt3 = 10 # 夜间背景像元中背景火点像元的D_BT_04_11判断阈值"""
        Th_cloud_desert = 8

        # FIXME （1）2000 m tif 数据的信息，tuple，

        # FIXME 这些移到主流程里面去，在这里面不方便函数之间的交流
        # FIXME 之后使用太阳天顶角计算，不使用一个固定的值
        # 更改各波段数据名称，使其名称中带有波长，方便日后更改到其它卫星数据或做算法调整

        # FIXME （2）data 读的直接是 array 数据


        # 校正
        Ref_64 = all_band['Ref_B03_data']
        # MIR
        BT_04 = all_band['BT_B07_data']
        # FIR
        BT_11 = all_band['BT_B14_data']

        # MIR-FIR
        D_BT_04_11 = BT_04 - BT_11


        # --------------------------------------------------------------------------------

        # 获取可监测像元,去除其中的背景火点像元（避免高温点对周围区域背景温度的影响）作为各卷积运算的有效像元
        #（1）：读取掩膜数据中的有效像元
        checkable_mask = GdalBase.read_tiff(checkable_mask)[0]
        #（2）：背景火点像元判断条件：BT_04 > Th_t7(325) & D_BT_04_11 > Th_dt2(20) # 白天 BT_04 > Th_t8(310) & D_BT_04_11 > Th_dt3(10) # 晚上
        # TODO CNQ 这判识标准的来源，背景高温火点判识效果差
        if day_or_night == 0:
            bg_fire_mask = np.logical_not(
                np.logical_and(BT_04 > Th_t7 * 100, D_BT_04_11 > Th_dt2 * 100))  # 白天
        else:
            bg_fire_mask = np.logical_not(
                # np.logical_and(BT_04 > Th_t8 * 100, D_BT_04_11 > Th_dt3 * 100))  # 晚上 TODO CNQ 晚上这个阈值明显错误，识别的火点太多！！！
                np.where(BT_04 > BT_11 + Ref_64 + 2000, 1, 0))

        # # BT_B07 ≥ BT_B14 + 100*Ref_B03 + 20K
        # bg_fire_mask = np.where(BT_04 > BT_11 + Ref_64 + 2000, 1, 0)

        #（3）：将去除背景火点像元后的结果作为有效像元
        valid_bg_pix_mask = checkable_mask * bg_fire_mask

        # --------------------------------------------------------------------------------
        
        # 掩膜背景，计算各通道的背景温度（取卷积窗口中的平均值）
        Ref_64_bg = CustomKernel.cal_kernel_mean(Ref_64, valid_bg_pix_mask)
        BT_04_bg = CustomKernel.cal_kernel_mean(BT_04, valid_bg_pix_mask)
        BT_11_bg = CustomKernel.cal_kernel_mean(BT_11, valid_bg_pix_mask)
        D_BT_04_11_bg = CustomKernel.cal_kernel_mean(D_BT_04_11, valid_bg_pix_mask)

        # --------------------------------------------------------------------------------

        # 计算标准差
        BT_04_bg_std = CustomKernel.cal_std(BT_04, BT_04_bg, valid_bg_pix_mask)
        D_BT_04_11_bg_std = CustomKernel.cal_std(D_BT_04_11, D_BT_04_11_bg, valid_bg_pix_mask)

        # --------------------------------------------------------------------------------

        # 火点确认：
        #（1）绝对火点：当监测区满足中红外亮温大于360K，太阳天顶角小于87度，可见光反射率小于70%；
        soe_angle_data = all_band['soe_angle_data']
        fire_abs = np.logical_and(np.logical_and(BT_04>36000, soe_angle_data>3), Ref_64<7000)

        # --------------------------------------------------------------------------------

        #（2）一般火点：当T4 ≥ T4_bg + a * δT4_bg 且 T4_11 ≥ T4_11bg + a * δT4_11bg ,a 初值为4
        # FIXME 这个参数要从外面传进来
        # a.火点判断系数------------------------------------------
        refine_mir_fire = float(cfg_xml_info['refine_mir_fire'])
        refine_m_f_fire = float(cfg_xml_info['refine_m_f_fire'])

        mir_fire = np.where(BT_04 >= BT_04_bg + refine_mir_fire * BT_04_bg_std, 1, 0) # (2)
        m_f_fire = np.where(D_BT_04_11 >= D_BT_04_11_bg + refine_m_f_fire * D_BT_04_11_bg_std, 1, 0) # (4)
        fire_nom = np.logical_and(mir_fire * m_f_fire, checkable_mask)

        # b.云污染去除-------------------------------------------
        '''云污染去除：在白天还将进行云污染判定，如果火点像元满足以下条件，认为是受到云污染，将不作为火点像元.
        Rvis ≥ Rvis_bg + RC_th; T11 ≤ T11bg - TC_th RC_th为可见光云污染判识阈值，初值置为15%。TC_th为远红外云污染判识阈值，初值置为5K 
        '''

        if day_or_night == 0:
            cloud_pollution_mat = np.logical_and(Ref_64 >= Ref_64_bg + 1500 , BT_11 <= BT_11_bg - 500)  #在白天还将进行云污染判定
            fire_rm_colud_pollution = fire_nom * np.logical_not(cloud_pollution_mat)
        else:
            fire_rm_colud_pollution = fire_nom

        # c.云边缘和荒漠区边缘影响去除------------------------------
        # 云边缘掩膜
        # cloud_mask_mat = GdalBase.read_tiff(cloud_mask)[0]
        fire_nom_rm_edge = fire_rm_colud_pollution.copy()

        # 获取云污染去除后的火点位置
        index = np.argwhere(fire_rm_colud_pollution > 0)

        # 云区边缘像元满足以下条件将去除 T4 ≤ T4_bg + c * δT4_bg 且  T4_11 ≤  T4_11bg + c * δT4_11bg TODO CNQ 目前计算结果有误，暂不使用
        # edge_clear = np.logical_and(BT_04 <= BT_04_bg + Th_cloud_desert * BT_04_bg_std,D_BT_04_11 <= D_BT_04_11_bg + Th_cloud_desert * D_BT_04_11_bg_std)

        # FIXME 对于图像边缘的火点计算有误，所有在图像边缘2个像素以内的火点都会被排除,临时使用
        # TODO 此条件计算有问题，临时去除 ==> edge_clear[i[0],i[1]]==0
        cloud_mask_mat = GdalBase.read_tiff(cloud_mask)[0]
        for i in index:
            # if np.sum(cloud_mask_true[i[0]-2:i[0]+3, i[1]-2:i[1]+3]) != 25: # 1KM分辨率适用
            # if np.sum(cloud_mask_mat[i[0]-1:i[0]+2, i[1]-1:i[1]+2])!=0 and edge_clear[i[0], i[1]]==True: # 正确的云边缘去除使用
            if np.sum(cloud_mask_mat[i[0]-1:i[0]+2, i[1]-1:i[1]+2]) != 0:
                fire_nom_rm_edge[i[0], i[1]] = 0

        # --------------------------------------------------------------------------------

        #（3）FIXME 云区火点判识
        # a.计算云区像元的有效掩膜 T4 ≥ 325K 且  T4_11 ≥ 30K 且 Rvis ≤ 60%
        cloud_valid_pix = np.logical_and(np.logical_and(BT_04 >= 32500, D_BT_04_11 >= 3000), Ref_64 <= 6000)
        # b.计算云区的背景值
        # 云区T4的数值
        cloud_BT_04 = BT_04 * cloud_valid_pix
        # 云区T4_bg的数值
        cloud_BT_04_bg = BT_04_bg * cloud_valid_pix
        # c.云区火点判定
        fire_cloud = np.where(cloud_BT_04 >= cloud_BT_04_bg + 2000, 1, 0)

        # --------------------------------------------------------------------------------

        # 最终的火点
        fire_final = np.where(fire_abs + fire_nom_rm_edge + fire_cloud > 0, 1, 0)

        # --------------------------------------------------------------------------------

        # FIXME 这些移到火点属性计算里面去做
        # 火点像元面积计算
        # 判断是否达到饱和条件 T4 ≥T_max, 这里T_max为中红外亮温上限，初值置为360K,若中红外通道亮温未达到饱和，用中红外通道计算亚像元火点
        # 面积比例P,否则使用远红外
        # TODO 计算火点面积 P = (N4_mix - N4_bg) / (N4_ft - N4_bg)；N4_ft有特定计算公式，日后修正
        P = abs((BT_04 - BT_04_bg).astype(np.float)) / (75000 - D_BT_04_11_bg_std)
        fire_area = (P * 10000).astype(np.int)

        # ----------------------输出中间结果用于验证------------------------------------------------------------

        # # #
        # im_width, im_height, im_bands, im_geotrans, im_proj = (map(lambda x: x[1], enumerate(tif_aux_tuple)))
        # #
        # out_path = r'E:\DEMO\Mask/'
        # file_path = out_path + 'bg_fire_mask.tif'
        # GdalBase.write_tiff(bg_fire_mask, im_width, im_height, im_bands, im_geotrans, im_proj, file_path)
        # #
        # #
        # fire_final_dir = out_path + 'fire_final.tif'
        # GdalBase.write_tiff(fire_final, im_width, im_height, im_bands, im_geotrans, im_proj, fire_final_dir)
        #
        # fire_abs_dir = out_path + 'fire_abs.tif'
        # GdalBase.write_tiff(fire_abs, im_width, im_height, im_bands, im_geotrans, im_proj, fire_abs_dir)
        #
        # fire_nom_rm_edge_dir = out_path + 'fire_nom_rm_edge.tif'
        # GdalBase.write_tiff(fire_nom_rm_edge, im_width, im_height, im_bands, im_geotrans, im_proj, fire_nom_rm_edge_dir)
        #
        # fire_cloud_dir = out_path + 'fire_cloud.tif'
        # GdalBase.write_tiff(fire_cloud, im_width, im_height, im_bands, im_geotrans, im_proj, fire_cloud_dir)
        #
        # # cloud_mask_true_dir = out_path + 'cloud_mask_true.tif'
        # # GdalBase.write_tiff(cloud_mask_true, im_width, im_height, im_bands, im_geotrans, im_proj, cloud_mask_true_dir)
        #
        # cloud_pollution_mask_dir = out_path + 'cloud_pollution_mask.tif'
        # # GdalBase.write_tiff(cloud_pollution_mask, im_width, im_height, im_bands, im_geotrans, im_proj, cloud_pollution_mask_dir)
        #
        # cloud_mask_mat_dir = out_path + 'cloud_mask_mat.tif'
        # GdalBase.write_tiff(cloud_mask_mat, im_width, im_height, im_bands, im_geotrans, im_proj, cloud_mask_mat_dir)
        #
        # fire_nom_dir = out_path + 'fire_nom.tif'
        # GdalBase.write_tiff(fire_nom, im_width, im_height, im_bands, im_geotrans, im_proj, fire_nom_dir)

        print '* fire monitor success!'
        return fire_final, fire_area

    @staticmethod
    def affirm_fire_rough(checkable_mark):
        """判断是否有火"""
        checkable_mark_mat = GdalBase.read_tiff(checkable_mark)[0]
        if np.sum(checkable_mark_mat) <= 0:
            return False
        else:
            return True

    # -------------------- 预处理 ----------------------------------

    @staticmethod
    def h8satellitAz(lon, lat):
        # Azimuth,Elevation,Zenith
        # R/H=6378.1370/42164==0.15127
        # ssp_lon=140.7
        satLon = 140.7
        S = satLon / 180. * math.pi
        N = lon / 180. * math.pi
        L = lat / 180. * math.pi
        G = S - N
        # Elevat
        if L == 0 and G == 0:
            E = math.pi / 2
        else:
            LL = math.sqrt(1 - (math.cos(G) * math.cos(L)) ** 2)
            E = math.atan((math.cos(G) * math.cos(L) - 0.15127) / LL)
        # Azimuth
        A = math.pi - math.atan2(math.tan(G), math.sin(L))
        # 弧度->度
        Azimuth = A / math.pi * 180
        Elevat = E / math.pi * 180
        zenith = (90 - Elevat)
        return Azimuth, zenith

    @staticmethod
    def deletFiles(tempPath):
        # 删除临时路径
        filelist = os.listdir(tempPath)
        for f in filelist:
            filepath = os.path.join(tempPath, f)
            if os.path.isfile(filepath):
                os.remove(filepath)
            elif os.path.isdir(filepath):
                shutil.rmtree(filepath, True)
        shutil.rmtree(tempPath, True)
        print tempPath + " is removed!"

    @staticmethod
    def writeGeotif(infile, outfile, extend, pixSize, width, height):
        # 将数据写入TIFF文件
        datab = np.fromfile(infile, dtype=np.uint16)
        datab = datab + 0.5
        datab[datab < 0] = 0
        out_driver = gdal.GetDriverByName('GTiff')
        out_dataset = out_driver.Create(outfile, width, height, 1, gdal.GDT_UInt16)
        out_band = out_dataset.GetRasterBand(1)
        out_band.WriteArray(datab.reshape(height, width), 0, 0)
        out_dataset.SetGeoTransform([float(extend[0]), pixSize, 0, float(extend[3]), 0, -pixSize])
        proj = osr.SpatialReference()
        proj.SetWellKnownGeogCS('WGS84')
        out_dataset.SetProjection(proj.ExportToWkt())
        out_dataset = None

    @staticmethod
    def getInputFileName(fileTime, channals, segments):
        # 根据时间、波段、条带拼写要处理的HSD文件名，支持官网原始HSD文件名格式：
        # HS_H08_20180809_0910_B16_FLDK_R20_S0410.DAT.bz2
        bNames = defaultdict(list)
        for band in channals:
            bandind = int(band) - 1
            chlstr = '_' + ConfigPara.chltag[bandind] + '_'
            resstr = '_' + ConfigPara.resTag[bandind] + '_'
            for seg in segments:
                segind = int(seg) - 1
                segstr = ConfigPara.segTag[segind]
                segName = 'HS_H08_' + fileTime + chlstr + 'FLDK' + resstr + segstr + '10.DAT'
                bNames[str(ConfigPara.chltag[bandind])].append(segName)
        return bNames

    @staticmethod
    def confirm_fire_point():
        pass

    @staticmethod
    def get_args_list(day_night, fileTime, channals, segments, extend, pixSize, inputPath, outPath, tempDir):
        # 计算各自的参数列表
        inputfilename_dict = FireMonitorProcessH8.getInputFileName(fileTime, channals, segments)
        args_dict_org = {'fileTime': fileTime, 'extend': extend, 'inputPath': inputPath, 'outPath': outPath,
                         'tempDir': tempDir}
        def update_dic(x, y):
            bname_bandf_value = [[], []]
            bname_bandf_value[0], bname_bandf_value[1] = x, inputfilename_dict[x]
            args_dict = args_dict_org.copy()  # 避免指向同一个内存地址
            args_dict.update({'bname_bandf': bname_bandf_value, 'pixSize': y})
            return args_dict
        # 白天黑夜
        if day_night == 0:
            ## 处理123，pix[1], 3,4,7,14 pix[2]
            arg_list = map(update_dic, ['B01', 'B02', 'B03', 'B03','B04', 'B07', 'B14'],([pixSize[1]]* 3)+([pixSize[0]]* 4))
        else:
            arg_list = map(update_dic, sorted(inputfilename_dict.keys())[2:], [pixSize[0]]* 4)
        return arg_list


    @staticmethod
    def cal_H8_angles(extend, pixSize, fileTime, inputFile, output):

        # TODO 直接使用参数固定生成？


        start_time = time.time()

        gdal.AllRegister()
        dataset = gdal.Open(inputFile)
        geoTrans = dataset.GetGeoTransform()
        print(geoTrans[0])
        print(geoTrans[3])
        # nXSize = dataset.RasterXSize  # 列数
        # nYSize = dataset.RasterYSize  # 行数
        nXSize = int((extend[1] - extend[0]) / pixSize[0])
        nYSize = int((extend[3] - extend[2]) / pixSize[0])
        print nXSize, nYSize
        # inRaster = arcpy.Raster(inputFile)
        dataset = gdal.Open(inputFile)
        # 仿射矩阵
        tiff_geotrans = dataset.GetGeoTransform()
        # 投影坐标
        tiff_proj = dataset.GetProjection()

        year = int(fileTime[0:4])
        month = int(fileTime[4:6])
        day = int(fileTime[6:8])
        hour = int(fileTime[9:11])
        minute = int(fileTime[11:]) + 2 # TODO CNQ 为何加2？ 确认行读取和列读取的效率差异
        second = 0
        timezone = 0

        # tempSoA = np.zeros((nYSize, nXSize), dtype=np.float16)
        tempSoE = np.zeros((nYSize, nXSize), dtype=np.float16)
        # tempSaA = np.zeros((nYSize, nXSize), dtype=np.float16)
        # tempSaZ = np.zeros((nYSize, nXSize), dtype=np.float16)
        for i in range(nYSize):
            for j in range(nXSize):
                longitude = geoTrans[0] + j * geoTrans[1] + i * geoTrans[2]  # 经度
                latitude = geoTrans[3] + j * geoTrans[4] + i * geoTrans[5]  # 纬度
                if longitude < 0.:
                    longitude = longitude + 360.
                tempSoE[i, j] = FireMonitorProcessH8.SolarAngles(year, month, day, hour, minute, second, timezone,
                                                                       longitude, latitude)

        # 保存成tif
        outPutPath = output + '\\'


        # 对比二者之间输出tif的数值无差异
        FireMonitorProcessH8.output_raster(outPutPath + 'soe.tif', tempSoE, tiff_geotrans, tiff_proj)

        # soe_path = outPutPath + 'soe.tif'
        # saz_path = outPutPath + 'saz.tif'
        print (outPutPath + 'soe.tif')
        print '# calculate saz cost: ' + str(time.time() - start_time)
        return (outPutPath + 'soe.tif')
        # return  {'saz': saz_path, 'soe': soe_path}

    @staticmethod
    def pretreatment(fileTime, channals, segments, extend, pixSize, inputPath, outPath, tempDir):
        """数据预处理"""
        pre_data_dict = {}
        # 检查列表中的文件夹是否存在，若不存在则新建
        check_dirpath([tempDir,outPath])
        # 计算太阳高度角,此处使用固定的卫星方位角文件
        curPath = os.path.abspath(os.path.dirname(__file__))
        saz_path = curPath + '/pretreatment_data/SaZ.tif'
        soe_tif_path = FireMonitorProcessH8.cal_H8_angles(extend, pixSize, fileTime, saz_path, outPath) # 试运行特别慢
        # 通过高度角判断白天、黑夜
        soe_data = GdalBase.read_tiff(soe_tif_path)[0]
        print np.min(soe_data)
        if np.min(soe_data) > 3.:   # 视为白天
            day_night = 0
            arg_list = FireMonitorProcessH8.get_args_list(
                day_night, fileTime, channals, segments, extend, pixSize, inputPath, outPath, tempDir)
            p = Pool(7)
            map(lambda x:pre_data_dict.update(x) ,p.map(single_band_process, arg_list))
        else:
            day_night = 1
            arg_list = FireMonitorProcessH8.get_args_list(
                day_night, fileTime, channals, segments, extend, pixSize, inputPath, outPath, tempDir)
            p = Pool(4)
            map(lambda x:pre_data_dict.update(x) ,p.map(single_band_process, arg_list))

        p.close()  # 关闭进程池，不再接受新的进程
        p.join()  # 主进程阻塞等待子进程的退出
        pre_data_dict.update({'soe':soe_tif_path})
        print 'all band has done!'
        return pre_data_dict


class CustomKernel(object):
    """
    使用原来的配置，提不出一个火点，现缩小矩阵范围
    这个包对数据类型支持的这么弱，不同数据类型运算的结果是0且不报错
    """

    # 获取计算背景温度的核函数（i*i）， 其中i中心的数为0，2KM分辨率使用这个
    @staticmethod
    def get_bg_kernel(i):
        cernel = np.ones(i*i, int).reshape(i, i).astype(np.float64)
        center = (i-1)/2
        cernel[center,center] = 0
        return cernel

    @staticmethod
    def get_valid_pix_mask(valid_pix_mask):
        """
        获取对应数据集中有效像元的掩膜dst,有效像元为1，无效为2
        :param src:有效像元的掩膜dst
        :return:返回的掩膜文件字典,包括有效像元sum和bin;和用到的层数
        """
        valid_pix_dic = {}
        dst_bin = np.zeros_like(valid_pix_mask).astype(np.float64)
        dst_sum_all = np.zeros_like(valid_pix_mask).astype(np.float64)
        # dst_sum = np.zeros_like(valid_pix_mask).astype(np.float64)  # 若是在此初始化，则字典中的sum的items指向同一内存位置
        for i in ConfigPara.kernel_shp:
            dst_sum = np.zeros_like(valid_pix_mask).astype(np.float64)
            dst = valid_pix_mask.astype(np.float64)
            # 1.获取计算有效像元的核函数
            sum_cernel = CustomKernel.get_bg_kernel(i)
            # 计算并返回计算结果 (cv2.filter2D有其具体对应的数据类型),不支持int32,uint32, 支持float64, uint16(值域过小)
            cv2.filter2D(dst, -1, sum_cernel, dst_sum)
            # TODO 改为2KM将修复 判断有效像元是否超过20%；超过才适用i*i下的背景温度计算
            valid_value = int((i*i-1)*0.25) # 计算有效值
            # valid_value = int((i * i - 9) * 0.25)
            # 计算i*i范围内的有效像元
            valid_pix_dic[str(i) + '_sum'] = dst_sum
            # 获得i*i矩阵计算下的有效像元 .astype(np.uint32)
            dst_i_bin_org = np.where((dst_sum > valid_value), 1, 0)
            # 去除之前有效像元的影响
            valid_pix_dic[str(i) + '_bin'] = np.where((dst_i_bin_org - dst_bin == 1), 1, 0).astype(np.float64)
            # 计算之前i-1层的有效像元
            dst_bin += valid_pix_dic[str(i) + '_bin']
            # 获取之前i-1层的有效像元邻域内可监测像元总数
            # dst_sum_all += valid_pix_dic[str(i) + '_sum']
            dst_sum_all = dst_sum_all + valid_pix_dic[str(i) + '_sum']*valid_pix_dic[str(i) + '_bin']
            # 判断dst_bin中是否有为0的像元，有继续循环，否则跳出
            if 0 in dst_bin[:, :]:
                continue
            else:
                # TODO CNQ 此处待修复
                return valid_pix_dic, ConfigPara.kernel_shp.index(i)
        return valid_pix_dic,dst_sum_all,len(ConfigPara.kernel_shp)


    # 计算对应i*i卷积计算下的背景温度
    @staticmethod
    def cal_bg_i(valid_mask, src, i, valid_pix_num_dst, valid_pix_bin_dst):
        # 计算src中的有效值部分; 计算后src_i的数据类型会变为int32,向通用类型转变
        # src_i = src * valid_pix_bin_dst   # -- 不使用i*i的有效掩膜
        # 获取i*i下计算背景像元的核函数
        bg_kernel_i = CustomKernel.get_bg_kernel(i)
        # 计算src中每个像元i*i矩阵内的和
        bg_dst_i_sum = np.zeros_like(src)
        cv2.filter2D(src, -1, bg_kernel_i, bg_dst_i_sum)
        # 计算src的背景温度
        bg_dst_i = bg_dst_i_sum / valid_pix_num_dst * valid_pix_bin_dst
        where_are_nan = np.isnan(bg_dst_i)
        where_are_inf = np.isinf(bg_dst_i)
        bg_dst_i[where_are_nan] = 0
        bg_dst_i[where_are_inf] = 0
        # bg_dst_i_float = bg_dst_i_sum * 1. / valid_pix_num_dst
        return bg_dst_i


    # 计算src_dst的背景温度
    @staticmethod
    def cal_kernel_mean(tif_dst,valid_mask):
        tif_dst = (tif_dst*valid_mask).astype(np.float64)
        valid_pix_mask_dic, temp, kernel_sum = CustomKernel.get_valid_pix_mask(valid_mask)
        bg_dst = np.zeros_like(tif_dst)
        # 分别计算每一层卷积的背景温度，在对其结果求和
        for i in ConfigPara.kernel_shp[:kernel_sum+1]:
            # 计算i卷积的背景温度
            org_bg_i = CustomKernel.cal_bg_i(valid_mask, tif_dst, i, valid_pix_mask_dic[str(i) + '_sum'], valid_pix_mask_dic[str(i) + '_bin'])
            # 更新bd_dst的数据
            bg_dst += org_bg_i*valid_pix_mask_dic[str(i) + '_bin']
        return bg_dst


    @staticmethod
    def cal_std(org_dst, bg_dst ,valid_mask):
        # 计算差值,平方
        sb_sq = np.square(org_dst - bg_dst)
        # 有效像元求和
        sum_sb_sq = CustomKernel.cal_kernel_mean(sb_sq, valid_mask)
        # 获取有效像元邻域内可监测像元总数
        temp, valid_sum, temp_1 = CustomKernel.get_valid_pix_mask(valid_mask)
        # 开方求平均
        std = np.sqrt(sum_sb_sq) / valid_sum
        std_valid = CustomKernel.rm_nan_inf(std)  # 将std值归一到指定区间
        # 如果标准差小于下限（初值为2K），将标准差置为2K;如果标准差大于上限（初值为3.5K），将标准差置为3.5K  ？？？
        a = np.where(std_valid > 350, 350, std_valid)
        std_nd = np.where(a < 200, 200, a)
        # std_v = rm_nan_inf(b * valid_mask)
        return std_nd

    @staticmethod
    def rm_nan_inf(dst):
        """将dst中的nan和inf值赋值为0"""

        where_are_nan = np.isnan(dst)
        where_are_inf = np.isinf(dst)
        dst[where_are_nan] = 0
        dst[where_are_inf] = 0
        return dst


def output_raster(tiff_dir, fire_data, tiff_geotrans, tiff_proj):
    # 给文件赋名
    if 'int8' in fire_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in fire_data.dtype.name:
        datatype = gdal.GDT_UInt16
    elif 'float16' in fire_data.dtype.name:
        datatype = gdal.GDT_Float32
    else:
        # TODO CNQ 打印出数据类型
        datatype = gdal.GDT_Float64
    driver = gdal.GetDriverByName("GTiff")  # 存的数据格式
    dataset = driver.Create(tiff_dir, fire_data.shape[1], fire_data.shape[0], 1, datatype)
    dataset.SetGeoTransform(tiff_geotrans)  # 写入仿射变换参数
    dataset.SetProjection(tiff_proj)  # 写入投影
    dataset.GetRasterBand(1).WriteArray(fire_data)
    del dataset


def check_dirpath(dir_list):
    '''检查对应的文件夹路径是否存在，若不存在则新建'''
    if type(dir_list) == list:
        for dir_path in dir_list:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
    elif type(dir_list) == str:
        if not os.path.exists(dir_list):
            os.makedirs(dir_list)
    else:
        print 'Function only support str&list type!'


def single_band_process(arg_list):
    '''批处理单波段的文件'''
    # fileTime, extend, pixSize, inputPath, outPath, tempDir, file_lists, bname_bandf
    fileTime, extend, pixSize, inputPath, outPath, tempDir, bname_bandf = \
        arg_list['fileTime'],arg_list['extend'],arg_list['pixSize'],arg_list['inputPath'],arg_list['outPath'],\
        arg_list['tempDir'],arg_list['bname_bandf']

    bname = bname_bandf[0]
    bandf = bname_bandf[1]

    # 根据经纬度范围计算输出图像的列数，行数
    width = int((float(extend[1]) - float(extend[0])) / pixSize)
    height = int((float(extend[3]) - float(extend[2])) / pixSize)

    # 获取C++可执行程序，本文件所在文件夹的同级文件夹hisd2latlon中，移动位置需更改此处
    curPath = os.path.abspath(os.path.dirname(__file__))
    cExe = os.path.join(curPath, r'pretreatment_data\hisd2latlon\hisd_lonlatprj.exe')

    # 检测文件是否存在
    if not os.path.exists(cExe):
        print 'cExe is not exsit'
        return

    # 拼写C++固定参数 # TODO 使用map函数
    geostr = ' '.join([str(extend[3]), str(extend[0]), str(width), str(height), str(pixSize), str(pixSize)])
    # 单波段临时文件夹，必须唯一
    tmptag = 'h8_' + ''.join(str(uuid.uuid1()).split('-'))
    bandTmp = os.path.join(tempDir, tmptag) + os.sep
    os.makedirs(bandTmp)
    # 复制解压该波段各个条带文件到临时文件夹
    ## 支持长短名格式的文件
    curPath = os.path.abspath(os.path.dirname(__file__))
    bzip2_path = curPath + '/pretreatment_data/GnuWin32/bin/bzip2.exe'
    for segf in bandf:
        # 检查输入文件
        for file in os.listdir(inputPath):
            if segf in file:
                segf = file
                bfile = inputPath + os.sep + segf
                cpbfile = os.path.join(bandTmp, segf)
                # 复制
                os.system('copy "' + bfile + '" "' + bandTmp + '"')
                # 解压
                if file[-3:] == 'BZ2':
                    os.system('rename "' + cpbfile + '" "' + segf[:-3] + "bz2" + '"')
                cpbfile = cpbfile[:-3] + 'bz2'
                os.system('"' + bzip2_path + '" -df ' + cpbfile)
    # 调用C++可执行程序，获取等经纬数据
    os.system(cExe + ' ' + bandTmp + ' ' + bandTmp + ' ' + geostr)
    outBand = os.path.join(bandTmp, 'H8.out')
    if not os.path.exists(outBand):
        # C++执行失败，处理别的波段
        print 'C++ exe failed at get h8.out files'
        # logFile.write(str(datetime.datetime.now()) + ' C++ exe failed at ' + segf[7:25] + '\r\n')
    # 定义输出文件H08_20181010_0230_B03_geo.tif HS_H08_20180926_0100_B14_FLDK_R20_S0410.DAT
    if pixSize == 0.01:
        outname = 'HS_H08_' + fileTime + '_' + bname + '_FLDK_R10.tif'
    elif pixSize == 0.02:
        outname = 'HS_H08_' + fileTime + '_' + bname + '_FLDK_R20.tif'
    elif pixSize == 0.005:
        outname = 'HS_H08_' + fileTime + '_' + bname + '_FLDK_R05.tif'
    else:
        print'WARN pixSize is not defined!'
        outname = 'HS_H08_' + fileTime + '_' + bname + '_FLDK_RXX.tif'
    outfile = os.path.join(outPath, outname)
    # 输出为TIFF文件 # TODO 确认是否使用这种数据格式
    FireMonitorProcessH8.writeGeotif(outBand, outfile, extend, pixSize, width, height)
    # file_lists.append(outfile)
    # logFile.write(str(datetime.datetime.now()) + '完成TIFF文件输出\r\n')
    # 删除临时文件
    # FireMonitorProcessH8.deletFiles(bandTmp)

    return {bname + '_' + str(pixSize):outfile}
