# -- coding: utf-8 --

import os
import xlrd
import arcpy
import numpy as np

from osgeo import gdal
from osgeo import osr
from common.config.ConstParam import ConstParam
from common.process.ProcessBase import BaseProcess
from common.utils.FileUtil import BaseFile
from common.utils.ArcPyUtil import ArcPyUtil
from IDLApps.AnHui.WSS_FY3BVIRR_COMPOSE.ReadReMap import ReadReMap

import shutil

"""

"""



class WSS_FY3BVIRR_COMPOSE(BaseProcess):
    '''
    风云3B-NDVI产品
    '''

    def __init__(self, pluginParam):
        BaseProcess.__init__(self, pluginParam)
        # # self.processOther = 1

    # ☆
    def getRSCmdInfo(self):
        """获取算法cmd字符串
        :return:
        """
        try:
            inputFolder = self.pluginParam.getInputInfoByKey("inputFile")
            if inputFolder is None:
                return None
            issue = self.pluginParam.getInputInfoByKey("issue")
            pluginName = self.pluginParam.getPluginName()
            idlTiffileName = pluginName + '_' + issue + "_IDL.tif"
            idlExePath = self.pluginParam.getIdlExePath()  # 算法封装路径
            if BaseFile.isFileOrDir(idlExePath) != BaseFile.ISFILE:
                return None
            tpFolder = self.pluginParam.getTempFolder()  # 临时目录根目录
            tempFolder = os.path.join(tpFolder, self.milsecondStr)

            # inputfile文件路径写入到txt中
            TxtfileDir = tempFolder + "\\"
            Txtfile = open(TxtfileDir + 'hecheng' + '.txt', "w")
            Txtfile.write(inputFolder)
            Txtfile.close()
            self.rsOutMap["OUTFILEPATH"] = os.path.join(tempFolder, idlTiffileName)

            # 组合cmdStr命令行
            # cmdStr = idlrt.exe路径 + .sav路径 + -args + hecheng.txt路径 + 排除值 + 合成方式（min\max\mean） + 最小值 + 最大值 + 输出路径
            #eg:"D:\\Program Files\\Exelis\\IDL84\\bin\\bin.x86_64\\idlrt.exe" F:\\NewFrame_AH\\IDLApps\\AnHui\\WSS_FY3BVIRR_COMPOSE\\productCompose.sav -args F:\\NewFrame_AH\\outputfile\\Temp\\1566122594584\\hecheng.txt 0 max -1 1 F:\\NewFrame_AH\\outputfile\\Temp\\1566122594584\\WSS_FY3BVIRR_COMPOSE_201703010000_IDL.tif'
            cmdStr = self.idlEnExePath + " " + idlExePath + " -args "
            cmdStr += Txtfile.name + " " + "0" + " " + "max" + " " + "-1" + " " + "1" + " " \
                      + os.path.join(tempFolder, idlTiffileName)
            return cmdStr
        except:
            return None

    def getReplacelyr(self, tifPath, ComShpDir):
        lyr_dict = {"raster": tifPath}

        return lyr_dict

    def getStaConditionRe(self):
        """分级统计条件"""
        return ["Count"]

    def getStaCondition(self):
        """统计条件"""
        return ["MAX", "MEAN", "MIN"]

    def updateStaMapInfo(self, staMapInfo):
        """更新统计信息 staMaps["StaMapRe"]结构 [AreaID][Level]=row  staMaps["StaMap"]结构 [AreaID]=row"""
        staMapRe = staMapInfo["StaMapRe"]
        staMap = staMapInfo["StaMap"]

        issue = self.pluginParam.getIssue()
        if len(staMapRe) > 0:
            self.outStaMap["htht_cluster_schedule_zonal_histogram"] = {
                "field": "\'issue\', \'region_id\', \'level\', \'value\'", "values": []}
            outStaMapReValues = self.outStaMap["htht_cluster_schedule_zonal_histogram"]["values"]
            for areaIDRe in staMapRe.keys():
                areaStaRe = staMapRe[areaIDRe]
                for levelStr in areaStaRe.keys():
                    valueStr = str(areaStaRe[levelStr][1] * 0.25 * 0.25)  # 计算面积，像元个数乘以分辨率的平方，即每个像元的面积
                    outStaMapReValues.append(issue + "," + areaIDRe + "," + levelStr + "," + valueStr)

        if len(staMap) > 0:
            self.outStaMap["htht_cluster_schedule_zonal_statistics"] = {
                "field": "\'issue\', \'region_id\', \'MAX\', \'MEAN\', \'MIN\'", "values": []}
            outStaMapValues = self.outStaMap["htht_cluster_schedule_zonal_statistics"]["values"]
            for areaID in staMap.keys():
                areaSta = staMap[areaID]
                outStaMapValues.append(
                    issue + "," + areaID + "," + str(areaSta[1]) + "," + str(areaSta[2]) + "," + str(areaSta[3]))

    # ☆
    def doStatisComp(self, tempDir, tifPath, minAreaShp, levelArea, curProNumber):
        """统计分析"""

        tpFolder = self.pluginParam.getTempFolder()  # 临时目录根目录
        tempFolder = os.path.join(tpFolder, self.milsecondStr)
        subareaDir = tempFolder  # FIXME  这句话和上面那句话为什么不合并起来？

        # 基于小麦分布区掩膜文件，掩膜NDVI最大值合成tif
        idlExePath = self.pluginParam.getIdlExePath()
        landcoverTif = os.path.join(os.path.dirname(idlExePath), "wheatRegion", "wheatRegion.tif")  # TODO 原来os.path.join() 是可以传入多个参数的（看源码）
        maskfile_path = os.path.splitext(tifPath)[0] + "mask.tif"  # FIXME 多个命名风格混合使用
        tifpath_mask = self.MaskByLandcover(tifPath, landcoverTif, maskfile_path)
        print '掩膜小麦区完成'

        # 分6个区进行裁剪
        dependDic = self.pluginParam.getDependFolder()
        MaskDir = os.path.join(dependDic,"Auxshp", "ZoningBoundary")
        issue = self.pluginParam.getInputInfoByKey("issue")
        subMasklist = self.subAreatif(tifpath_mask, MaskDir, subareaDir, issue)
        print "分区裁剪完成"

        # 根据6个区的阈值分别进行重分类
        subareaReClasslist = self.Reclassifytif(subMasklist, subareaDir)
        print "分区重分类完成"

        # 镶嵌六个区的重分类后的数据
        NewRasterDic = os.path.dirname(subareaReClasslist[0])
        tifPath_reclass = self.MosaicToNewRaster(subareaReClasslist, NewRasterDic)
        print "分区重分类_拼接完成"

        # 【0】 FIXME 读取需要的属性，生成默认的 staMap 字典
        initStaMap = self.doStatisInit()

        # 判断是否读初始化成功
        if len(initStaMap) == 0:
            BaseFile.appendLogInfo(self.logPath, str(float('%.2f' % curProNumber)) + "%", "初始化统计分析失败，查看 shp 文件是否错误")
            return False
        BaseFile.appendLogInfo(self.logPath, str(float('%.2f' % curProNumber)) + "%", "初始化统计分析成功")

        # #【1】统计，【临时文件夹，tif文件，最小的行政区划，区域的等级】，无需返回值
        # # ConstParam.GRADUATIONSTATISTICS（分级统计）, ConstParam.NORMALSTATISTICS（正常统计）, ConstParam.ALLSTATISTICS（分级统计 + 正常统计）
        self.areaStatis(tempDir, tifPath_reclass, minAreaShp, levelArea, ConstParam.ALLSTATISTICS)

        # 【2】专题图
        curProNumber = curProNumber + 2
        self.creatPic(tifPath_reclass, initStaMap, str(float('%.2f' % curProNumber)))

        # 【3】裁切
        curProNumber = curProNumber + 2
        self.areaClipTif(tifPath_reclass, initStaMap, str(float('%.2f' % curProNumber)))

        # 【4】报告
        # curProNumber = curProNumber + 2
        # self.exportWord(self, tifPath, staMap, str(float('%.2f' % curProNumber)))

        return True

    def doStatisComp_new(self, tempDir, tifPath, minAreaShp, levelArea, curProNumber):
        """统计分析"""

        tifPath_reclass = self.do_init_py(tifPath)  # **** 流程

        # 【0】
        initStaMap = self.doStatisInit()

        # 判断是否读初始化成功
        if len(initStaMap) == 0:
            BaseFile.appendLogInfo(self.logPath, str(float('%.2f' % curProNumber)) + "%", "初始化统计分析失败，查看 shp 文件是否错误")
            return False
        BaseFile.appendLogInfo(self.logPath, str(float('%.2f' % curProNumber)) + "%", "初始化统计分析成功")

        # #【1】统计，【临时文件夹，tif文件，最小的行政区划，区域的等级】，无需返回值
        # # ConstParam.GRADUATIONSTATISTICS（分级统计）, ConstParam.NORMALSTATISTICS（正常统计）, ConstParam.ALLSTATISTICS（分级统计 + 正常统计）
        self.areaStatis(tempDir, tifPath_reclass, minAreaShp, levelArea, ConstParam.ALLSTATISTICS)

        # 【2】专题图
        curProNumber = curProNumber + 2
        self.creatPic(tifPath_reclass, initStaMap, str(float('%.2f' % curProNumber)))

        # 【3】裁切
        curProNumber = curProNumber + 2
        self.areaClipTif(tifPath_reclass, initStaMap, str(float('%.2f' % curProNumber)))

        return True

    ## 基于分区矢量，裁剪tif
    def subAreatif(self, tifPath, MaskDir, subareaDir, issue):
        file_list = os.listdir(MaskDir)
        subMasklist = []
        for shpName in file_list:
            if os.path.splitext(shpName)[1] == '.shp':
                filename = issue + '_' + os.path.splitext(shpName)[0] + '.tif'
                subMaskPath = os.path.join(subareaDir, filename)  # 创建输出路径
                if os.path.exists(subMaskPath):
                    os.remove(subareaDir)
                    os.mkdir(subareaDir)
                inMaskData = os.path.join(MaskDir, shpName)
                outExtractByMask = arcpy.sa.ExtractByMask(tifPath, inMaskData)  # 执行掩膜处理
                outExtractByMask.save(subMaskPath)  # 保存
                subMasklist.append(subMaskPath)
        return  subMasklist

    @staticmethod
    def subAreatif_new(tiff_path, mask_dir, sub_area_dir, issue):
        """"使用一个文件夹下面的所有 shp 文件对 tiff 进行掩膜，并返回掩膜后的各个 tiff 路径"""

        # 创建空的 subareaDir 文件夹
        if os.path.exists(sub_area_dir):
            shutil.rmtree(sub_area_dir)
        os.makedirs(sub_area_dir)

        res_tiff_path_list = []  # 结果路径
        for each_file in os.listdir(mask_dir):
            if each_file.endswith('.shp'):
                mask_path = os.path.join(mask_dir, each_file)  # shp 掩膜路径
                filename = "{0}_{1}.tif".format(issue, os.path.splitext(each_file)[0])  # 文件名
                res_tiff_path = os.path.join(sub_area_dir, filename)  # 结果 tiff 路径
                arcpy.sa.ExtractByMask(tiff_path, mask_path).save(res_tiff_path)  # 保存掩膜  # 执行掩膜处理
                res_tiff_path_list.append(res_tiff_path)  #

        """
        问题
        （1）判断结果路径是否存在，不存在就删除路径的文件夹，这个逻辑比较奇怪
        （2）删除文件夹不能用 os.remove()
        （3）最好在函数下面用一下句话对函数进行说明
        （4）变量名眼花缭乱，未判断是否为 shp 文件之前命名为 shpName；inMaskData，outExtractByMask，subMasklist 比较容易误解
        """
        return  res_tiff_path_list

    def Reclassifytif(self, subMasklist, ReClassDir):
        depth = "000~006"
        idlExePath = self.pluginParam.getIdlExePath()
        pluginName = self.pluginParam.getPluginName()
        SMDAS2xmlPath = os.path.dirname(idlExePath) + "\\" + pluginName + "_Reclass.xml"
        ReMapIns = ReadReMap(SMDAS2xmlPath)
        ReMapIns.loadCfgInfo(True, "ProductReMapTable", False)

        subareaReClasslist = []
        for filename in subMasklist:
            if os.path.splitext(filename)[1] == '.tif':  # 获取.tif文件
                subareaReClassPath = os.path.splitext(filename)[0] + '_ReClass.tif'  # 创建重分类文件名
                if os.path.exists(subareaReClassPath):
                    os.remove(ReClassDir)
                    os.mkdir(ReClassDir)
                areaName = os.path.splitext(os.path.basename(filename))[0]
                region = areaName.split("_")[1]
                remap = arcpy.sa.RemapRange(ReMapIns.OutReMapList(depth, region))

                outReClass = arcpy.sa.Reclassify(filename, "Value", remap, "NODATA")
                outReClass.save(subareaReClassPath)
                subareaReClasslist.append(subareaReClassPath)
        return  subareaReClasslist

    # 对重分类后的六个区的tif进行镶嵌处理
    def MosaicToNewRaster(self,ReClasslist, NewRasterDic):
        input_rasters = ""
        for filename in ReClasslist:
            if os.path.splitext(filename)[1] == '.tif':  # 获取.tif文件
                input_rasters += filename + ";"

        ReClassDir = os.path.dirname(ReClasslist[0])
        arcpy.env.workspace = ReClassDir
        input_rasters = input_rasters[:-1]
        output_location = NewRasterDic
        rasterName = self.pluginParam.getInputInfoByKey("areaID") + "_mosaic" + ".tif"
        if os.path.exists(os.path.join(output_location, rasterName)):
            os.remove(NewRasterDic)
            os.remove(NewRasterDic)

        arcpy.MosaicToNewRaster_management(input_rasters, output_location, rasterName, number_of_bands=1)

        return os.path.join(output_location, rasterName)

    def getReplaceele(self):
        issue = self.pluginParam.getIssue()
        if issue[6:8] == "11":
            cyclestr = u"上"
            monthstr = issue[4:6]
            yearstr = issue[0:4]
        elif issue[6:8] == "21":
            cyclestr = u"中"
            monthstr = issue[4:6]
            yearstr = issue[0:4]
        elif issue[6:8] == "01" and issue[4:6] != "01":
            monthstr = str(int(issue[4:6]) - 1)
            cyclestr = u"下"
            yearstr = issue[0:4]
        elif issue[6:8] == "01" and issue[4:6] == "01":
            monthstr = "12"
            cyclestr = u"下"
            yearstr = str(int(issue[0:4]) - 1)
        ele_dict = {
            "title_name": {"yyyy": yearstr, "MM": monthstr, "XX": cyclestr}
        }
        return ele_dict

    def getReplaceele_new(self):
        """根据 issue 获取需要计算的时间标签"""
        issue = self.pluginParam.getIssue()
        yearstr, monthstr, daystr = issue[:4], issue[4:6], issue[6:8]  # 从 issue 获取月和日
        cyclestr = {'11': u'上', '21': u'中', '01': u'下'}[daystr]  # 获取旬标签

        if daystr == '01':  # 当日为 01 时候为特殊值，需要进行处理
            if monthstr == '01':
                monthstr = str(int(monthstr) - 1)  # 月数减一
            else:
                monthstr = '12'  # 月恢复为 12
                yearstr = str(int(yearstr) - 1)  # 年数减一

        return {"title_name": {"yyyy": yearstr, "MM": monthstr, "XX": cyclestr}}

    def MaskByLandcover(self, hecheng_subset, landcover_tif, maskfile_path):
        ## 打开输入影像
        in_hecheng = gdal.Open(hecheng_subset)
        date_hecheng = in_hecheng.ReadAsArray()
        in_gt_hecheng = in_hecheng.GetGeoTransform()
        in_proj_hecheng = in_hecheng.GetProjection()
        rows_hecheng = len(date_hecheng)
        cols_hecheng = len(date_hecheng[0])

        ## 打开掩膜文件
        in_landcover = gdal.Open(landcover_tif)
        date_landcover = in_landcover.ReadAsArray()

        # 基于掩膜文件，提取小麦分布区的NDVI.tif
        maskfile_array = np.zeros([rows_hecheng, cols_hecheng], dtype=float)
        index1 = np.where(date_landcover == 0)
        maskfile_array[index1] = 0
        index2 = np.where(date_landcover == 1)
        maskfile_array[index2] = date_hecheng[index2]

        #创建文件
        out_driver = gdal.GetDriverByName("GTiff")
        out_dataset = out_driver.Create(maskfile_path, cols_hecheng, rows_hecheng, 1, 6)

        out_dataset.SetGeoTransform(in_gt_hecheng) #写入仿射变换参数
        out_dataset.SetProjection(in_proj_hecheng) #写入投影
        out_dataset.GetRasterBand(1).WriteArray(maskfile_array) #写入数组

        out_dataset.FlushCache()

        return maskfile_path

    @staticmethod
    def MaskByLandcover_new(hecheng_subset, landcover_tif, maskfile_path):
        """将掩膜文件中值为1的范围提取出来，将其他值设置为 0 """
        date_hecheng, im_width, im_height, im_bands, im_geotrans, im_proj = GdalBase.read_tiff(hecheng_subset)  # 打开合成 tiff
        date_landcover = GdalBase.read_tiff(landcover_tif)[0]  # 打开掩膜 tiff
        #
        date_hecheng[date_landcover != 1] = 0  # 小麦分布区的NDVI 设置为 0
        #
        GdalBase.write_tiff(date_hecheng, im_width, im_height, im_bands, im_geotrans, im_proj, out_path=maskfile_path)  # 输出为文件

        """
        小问题
        （1）函数只干了一件事情，将掩膜值为非1的区域的 hecheng_subset 值，设置为 0，所以直接一步就可以实现 date_hecheng[date_landcover != 1] = 0
        （2）函数最后输出了输入值，出现 maskfile_path，这一步难以理解
        （3）对于常用的 tiff 打开和保存操作，为了简洁，最好使用封装好的函数，看代码也容易找到重点
        （4）没有通道 self 参数的最好改为静态函数
        """

    def do_init_py(self, tifPath):
        """掩膜小麦区，分区裁剪，分区重分类，拼接"""
        tpFolder = self.pluginParam.getTempFolder()  # 临时目录根目录
        tempFolder = os.path.join(tpFolder, self.milsecondStr)
        subareaDir = tempFolder  # FIXME  这句话和上面那句话为什么不合并起来？

        # 基于小麦分布区掩膜文件，掩膜NDVI最大值合成tif
        idlExePath = self.pluginParam.getIdlExePath()
        landcoverTif = os.path.join(os.path.dirname(idlExePath), "wheatRegion", "wheatRegion.tif")  # TODO 原来os.path.join() 是可以传入多个参数的（看源码）
        maskfile_path = os.path.splitext(tifPath)[0] + "mask.tif"  # FIXME 多个命名风格混合使用
        tifpath_mask = self.MaskByLandcover(tifPath, landcoverTif, maskfile_path)
        print '掩膜小麦区完成'

        # 分6个区进行裁剪
        dependDic = self.pluginParam.getDependFolder()
        MaskDir = os.path.join(dependDic,"Auxshp", "ZoningBoundary")
        issue = self.pluginParam.getInputInfoByKey("issue")
        subMasklist = self.subAreatif(tifpath_mask, MaskDir, subareaDir, issue)
        print "分区裁剪完成"

        # 根据6个区的阈值分别进行重分类
        subareaReClasslist = self.Reclassifytif(subMasklist, subareaDir)
        print "分区重分类完成"

        # 镶嵌六个区的重分类后的数据
        NewRasterDic = os.path.dirname(subareaReClasslist[0])
        tifPath_reclass = self.MosaicToNewRaster(subareaReClasslist, NewRasterDic)
        print "分区重分类_拼接完成"

        return tifPath_reclass












