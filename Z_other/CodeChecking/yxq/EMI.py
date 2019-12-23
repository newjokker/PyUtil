# -- coding: utf-8 --
import os
import datetime
from getcimissData import getcimissData
import numpy as np
import arcpy
from arcpy import env
from arcpy.sa import *
import gdal


class EMI:

    def __init__(self, issue, inputFolder_cimiss,inputFolder_ndvi,delday,tempFolder,outputFolder,city_shp):
        self.issue = issue
        self.outputFolder=outputFolder
        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)
        self.inputFolder_ndvi = inputFolder_ndvi
        self.delday = delday
        self.tempFolder = tempFolder
        if not os.path.exists(tempFolder):
            os.makedirs(tempFolder)
        end_date = datetime.datetime.strptime(issue, "%Y%m%d%H%M")
        days = datetime.timedelta(days=-int(delday))
        begin_date = end_date + days
        begin_issue = datetime.datetime.strftime(begin_date, "%Y%m%d%H%M%S")[0:12]
        self.begin_issue = begin_issue   #起始时间
        self.inputcimiss = os.path.join(inputFolder_cimiss,issue + '_' + delday)
        self.city_shp=city_shp
        self.datas={}
        self.station={}
        self.city_statistics={}
        self.INV=None
        self.IAE=None
        self.IFET=None
        self.EMI=None

    def doprocess(self):
        self.readDatas()
        #计算能见度指数
        self.getINV()
        #计算大气环境指数
        self.getIAE()
        #计算温湿适宜频率指数
        self.getIFET()
        #计算EMI气象生态评价指数
        self.getEMI()
        return self.EMI,self.city_statistics

    def readDatas(self):
        if not os.path.isdir(self.inputcimiss) or len(os.listdir(self.inputcimiss))!=((int(self.delday)+1)*24):
            getcimissData(self.inputcimiss, self.issue, self.begin_issue)
        cimiss_list=[int(x.split('.')[0]) for x in os.listdir(self.inputcimiss)]
        cimiss_list_sort = sorted(cimiss_list)
        for i in cimiss_list_sort:
            station_data = open(os.path.join(self.inputcimiss,str(i)+'.txt'), "r")
            line_head = station_data.readline().replace("\n","")
            Station_ID_C = line_head.split(',').index('Station_ID_C')  # FIXME 不需要多次进行裁切，得到一个裁切结果，下面全部用这个结果就行
            Lon = line_head.split(',').index('Lon')
            Lat = line_head.split(',').index('Lat')
            TEM = line_head.split(',').index('TEM')
            RHU = line_head.split(',').index('RHU')
            PRE = line_head.split(',').index('PRE')
            VIS = line_head.split(',').index('VIS')

            # ------------------------------ (1) ------------------------------------
            solit_res = line_head.split(',')
            Lon, Lat, TEM = solit_res.index('Lon'), solit_res.index('Lat'), solit_res.index('TEM')
            RHU, PRE, VIS = solit_res.index('RHU'), solit_res.index('PRE'), solit_res.index('VIS')
            # ------------------------------ (2) ------------------------------------
            solit_res = line_head.split(',')
            Lon, Lat, TEM, RHU, PRE, VIS = map(lambda x: solit_res.index(x), ['Lon', 'Lat', 'TEM', 'RHU', 'PRE', 'VIS'])
            # ------------------------------ (3) ------------------------------------
            Lon, Lat, TEM, RHU, PRE, VIS = map(lambda x: line_head.split(',').index(x), ['Lon', 'Lat', 'TEM', 'RHU', 'PRE', 'VIS'])
            # -----------------------------------------------------------------------


            for station in range(81):
                line = station_data.readline().replace("\n","").split(',')
                Station_ID=line[Station_ID_C]
                if not ( Station_ID in self.datas.keys()):
                    self.datas[Station_ID]={'TEM':[],'RHU':[],'PRE':[],'VIS':[]}
                    self.station[Station_ID]={}
                    self.station[Station_ID]['lon']=line[Lon]
                    self.station[Station_ID]['lat']=line[Lat]
                    self.datas[Station_ID]['TEM'].append(float(line[TEM]))
                    self.datas[Station_ID]['RHU'].append(float(line[RHU]))
                    self.datas[Station_ID]['PRE'].append(float(line[PRE]))
                    self.datas[Station_ID]['VIS'].append(float(line[VIS]))
                else:
                    self.datas[Station_ID]['TEM'].append(float(line[TEM]))
                    self.datas[Station_ID]['RHU'].append(float(line[RHU]))
                    self.datas[Station_ID]['PRE'].append(float(line[PRE]))
                    self.datas[Station_ID]['VIS'].append(float(line[VIS]))

    def getINV(self):
        V_mean_month ={}
        V_mean=[]
        #计算每个站点的月均能见度
        for keys in self.datas.keys():
            PRE=self.datas[keys]['PRE']
            RHU=self.datas[keys]['RHU']
            VIS = self.datas[keys]['VIS']
            V_month=[]
            for i in range(len(PRE)):
                if PRE[i] == 999999 and RHU[i] < 90 and VIS[i]!=999999:  # FIXME  可以同时获取切片和计数
                    V_month.append(float(VIS[i]))

            # ---------------------------------------------------------------------
            for index, each in enumerate(PRE):
                if each == 999999 and RHU[index] < 90 and VIS[index]!=999999:
                    V_month.append(float(VIS[index]))
            # ---------------------------------------------------------------------

            if np.mean(V_month)!=999999:
                # V_mean.append(np.mean(V_month))
                V_mean_month[keys]=np.mean(V_month)
        #计算每个站点的能见度指数
        V_min = min(V_mean_month.values())
        V_max = max(V_mean_month.values())
        for keys in V_mean_month.keys():
            INV=(V_mean_month[keys]-V_min)/(V_max-V_min)
            V_mean_month[keys]=INV

        txt_name=self.write_txt(self,'INV',V_mean_month)
        INV_tif=self.TXTtoIDW(self, 'INV', txt_name)
        self.INV=INV_tif
        self.city_statistics['INV']=self.stat_city(self, INV_tif, 'INV')

    def getIAE(self):
        IAE={}
        IAE_F={}
        for keys in self.datas.keys():
            RHU = self.datas[keys]['RHU']
            VIS = self.datas[keys]['VIS']
            F = 0
            F_q = 0
            F_Mid = 0
            F_z = 0
            for i in range(len(VIS)):
                if RHU[i] < 80 and VIS[i] < 10000:
                    F = F + 1
                if RHU[i] < 80 and 2999 < VIS[i] < 10000:
                    F_q = F_q + 1
                if RHU[i] < 80 and 1999 < VIS[i] < 3000:
                    F_Mid = F_Mid + 1
                if RHU[i] < 80 and VIS[i] < 2000:
                    F_z = F_z + 1
            IAE_F[keys]={'F':F,'F_q':F_q,'F_Mid':F_Mid,'F_z':F_z}
        F_min = min(map(lambda x:x[1]['F'],IAE_F.items()))           # FIXME 建议改为下面的形式，看着舒服一点
        F_max = max(map(lambda x:x[1]['F'],IAE_F.items()))
        F_q_min = min(map(lambda x:x[1]['F_q'],IAE_F.items()))
        F_q_max = max(map(lambda x:x[1]['F_q'],IAE_F.items()))
        F_Mid_min = min(map(lambda x:x[1]['F_Mid'],IAE_F.items()))
        F_Mid_max = max(map(lambda x:x[1]['F_Mid'],IAE_F.items()))
        F_z_min = min(map(lambda x:x[1]['F_z'],IAE_F.items()))
        F_z_max = max(map(lambda x:x[1]['F_z'],IAE_F.items()))

        # -----------------------------------------------------------------
        F_data = map(lambda x: x[1]['F'], IAE_F.items())
        F_min, F_max, = min(F_data), max(F_data)
        # -----------------------------------------------------------------

        for keys in IAE_F.keys():
            if F_max - F_min == 0:
                F0 = 0.0
            else:
                F0 = 1 - float(IAE_F[keys]['F'] - F_min) / float(F_max - F_min)  # FIXME  做的都是一样的事情，可以使用一个函数
            if F_q_max - F_q_min == 0:
                F1 = 0.0
            else:
                F1 = 1 - float(IAE_F[keys]['F_q'] - F_q_min) / float(F_q_max - F_q_min)
            if F_Mid_max - F_Mid_min == 0:
                F2 = 0.0
            else:
                F2 = 1 - float(IAE_F[keys]['F_Mid'] - F_Mid_min) / float(F_Mid_max - F_Mid_min)
            if F_z_max - F_z_min == 0:
                F3 = 0.0
            else:
                F3 = 1 - float(IAE_F[keys]['F_z'] - F_z_min) / float(F_z_max - F_z_min)

            # -----------------------------------------------------------------  # FIXME lambda 表达式和 三元表达式可以让代码更加清晰
            get_vale_temp = lambda x_key, x, x_max, x_min: 1 - float(IAE_F[x_key][x] - x_min) / float(x_max - x_min)  # 获取需要的值

            for each in IAE_F:
                F0 = 0.0 if F_max -     F_min == 0      else get_vale_temp(each, 'F',    F_max, F_min)
                F1 = 0.0 if F_q_max -   F_q_min == 0    else get_vale_temp(each, 'F_q',  F_q_max, F_q_min)
                F2 = 0.0 if F_Mid_max - F_Mid_min == 0  else get_vale_temp(each, 'F_Mid',F_Mid_max, F_Mid_min)
                F3 = 0.0 if F_z_max -   F_z_min == 0    else get_vale_temp(each, 'F_z',  F_z_max, F_z_min)
            # -----------------------------------------------------------------

            IAE_value = 0.4 * F0 + 0.3 * F1 + 0.2 * F2 + 0.1 * F3
            IAE[keys]=IAE_value
        txt_name = self.write_txt(self, 'IAE', IAE)
        IAE_tif = self.TXTtoIDW(self, 'IAE', txt_name)
        self.IAE = IAE_tif

        self.city_statistics['IAE'] = self.stat_city(self, IAE_tif, 'IAE')

    def getIFET(self):
        Et = {} #温湿指数
        for keys in self.datas.keys():
            TEM = self.datas[keys]['TEM']
            RHU=self.datas[keys]['RHU']
            E_base = 15
            m = 0
            day = len(TEM) / 24
            for i in range(day):
                E_14 = E_base + 24 * i
                E_day = TEM[E_14] - 0.55 * (1 - RHU[E_14] / 100) * (58 - TEM[E_14])
                if 18.9 < E_day < 25.6:
                    m = m + 1   #温湿适宜的天数
            Et_value = float(m) / float(day)
            Et[keys]=Et_value
        txt_name=self.write_txt(self,'IFET',Et)
        IFET_tif=self.TXTtoIDW(self, 'IFET', txt_name)
        self.IFET=IFET_tif
        self.city_statistics['IFET'] = self.stat_city(self, IFET_tif, 'IFET')

    def getEMI(self):
        INV_data = gdal.Open(self.INV)
        IAE_data = gdal.Open(self.IAE)
        IFET_data = gdal.Open(self.IFET)
        NDVI_data = gdal.Open(self.inputFolder_ndvi)
        EMI = INV_data.GetRasterBand(1).ReadAsArray() * 0.2 + IAE_data.GetRasterBand(
            1).ReadAsArray() * 0.5 + IFET_data.GetRasterBand(1).ReadAsArray() * 0.1 + NDVI_data.GetRasterBand(
            1).ReadAsArray() * 0.2
        im_data, im_width, im_height, im_bands, im_geotrans, im_proj = self.read_tiff(str(self.inputFolder_ndvi))
        EMI_path_nomask=os.path.join(self.tempFolder,self.issue+'_EMI_nomask.tif')
        EMI_path=os.path.join(self.outputFolder,self.issue+'_EMI.tif')
        self.write_tiff(EMI, im_width, im_height, im_bands, im_geotrans, im_proj, EMI_path_nomask)
        ndvi_mask = SetNull(self.inputFolder_ndvi, EMI_path_nomask, 'VALUE<0')
        ndvi_mask.save(EMI_path)
        self.EMI=EMI_path
        self.city_statistics['EMI'] = self.stat_city(self, EMI_path, 'EMI')
        self.city_statistics['NDVI'] = self.stat_city(self, self.inputFolder_ndvi, 'NDVI')

    @staticmethod
    def stat_city(self,outtif,name):  # FIXME 不要用 self 作为参数
        stat_city={}
        to_outTable=os.path.join(self.tempFolder,name+'_'+self.issue+'_.dbf')
        stat = []
        outZSaT = ZonalStatisticsAsTable(self.city_shp, "ID", outtif, to_outTable, "DATA", "ALL")
        index_name = []
        shp_name = self.city_shp.replace('shp', 'dbf')
        for k in arcpy.da.SearchCursor(shp_name, ["ID", "NAME"]):
            index_name.append(k)
        for i in arcpy.da.SearchCursor(to_outTable, ["ID", "MEAN"]):
            stat.append(i)
        for m in range(len(stat)):
            for t in range(len(index_name)):
                if index_name[m][0] == stat[t][0]:
                    stat_city[index_name[m][1]]=stat[t][1]
        return stat_city

    @staticmethod
    def write_txt(self,ident_name,data):
        txt_name = os.path.join(self.tempFolder,ident_name+self.issue+'.txt')
        file = open(txt_name, 'w')  # FIXME 不要用关键字做变量名
        head = 'Lon,Lat,' + ident_name + '\n'
        file.write(head)
        for i in data.keys():
            str_data = self.station[i]['lon'] + ',' + self.station[i]['lat'] + ',' + str(data[i]) + '\n'
            file.write(str_data)
        file.close()
        return txt_name

    def write_txt_new(self,ident_name,data):
        """将data内容写入文件"""

        txt_name = '{0}/{1}{2}.txt'.format(self.tempFolder, ident_name, self.issue)  # 保存的文件名
        table_head = 'Lon,Lat,{0}\n'.format(ident_name)  # 表头

        with open(txt_name, 'w') as txt_file:
            # 表头
            txt_file.write(table_head)
            # 表身
            for each in data:
                each_lon, each_lat, each_data = self.station[each]['lon'], self.station[each]['lat'], data[each]['lon']
                each_line = ','.join([each_lon, each_lat, each_data]) + '\n'
                txt_file.write(each_line)

        return txt_name

    @staticmethod
    def TXTtoIDW(self,ident_name, txt_name):
        im_data, im_width, im_height, im_bands, im_geotrans, im_proj = self.read_tiff(str(self.inputFolder_ndvi))

        issue=self.issue
        out_Layer_name="'" +issue+ident_name+"_shp'"
        shp_name=os.path.join(self.tempFolder,issue+ident_name+'.shp')
        tif_Name=os.path.join(self.tempFolder,issue+ident_name+'.tif')
        if not os.path.exists(shp_name):
            # geoPrj = os.path.join(os.path.dirname(pluginParam.getIdlExePath()), 'prj', 'haianxian.prj')
            # geoPrj = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
            arcpy.MakeXYEventLayer_management(txt_name, "lon", "lat", out_Layer_name, im_proj, "")  # FIXME 可以改为最新的 gdal 中的生成点的方法，比arcpy的更加快，也不容易出错
            arcpy.CopyFeatures_management(out_Layer_name, shp_name, "", "0", "0", "0")
        env.workspace = self.tempFolder + '\\'
        arcpy.env.extent = "114.876586897476 29.395559287302 119.646586897476 34.655559287302"  # FIXME 里面写死了范围，这种方式不可取
        # arcpy.env.extent = '"'+str(im_geotrans[0])+' '+str(im_geotrans[3]+(im_height+1)*im_geotrans[5])+' '+str(im_geotrans[0]+(im_width+1)*im_geotrans[1])+' '+str(im_geotrans[3])+'"'
        outIDW = Idw(shp_name, ident_name, "0.01", "", "")
        outIDW.save(tif_Name)
        return tif_Name

    @staticmethod
    def read_tiff(path):
        """读取 TIFF 文件"""
        # 参数类型检查
        if isinstance(path, str):
            dataset = gdal.Open(path)
        elif isinstance(path, gdal.Dataset):
            dataset = path
        else:
            raise TypeError('path can only be string or dataset')

        if dataset:
            im_width = dataset.RasterXSize  # 栅格矩阵的列数
            im_height = dataset.RasterYSize  # 栅格矩阵的行数
            im_bands = dataset.RasterCount  # 波段数
            im_proj = dataset.GetProjection()  # 获取投影信息
            im_geotrans = dataset.GetGeoTransform()  # 获取仿射矩阵信息
            im_data = dataset.ReadAsArray(0, 0, im_width, im_height)  # 获取数据
            return im_data, im_width, im_height, im_bands, im_geotrans, im_proj

        else:
            print(' 读取失败 ')

    @staticmethod
    def write_tiff(im_data, im_width, im_height, im_bands, im_geotrans, im_proj, out_path, data_no_value=None):

        if 'int8' in im_data.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in im_data.dtype.name:
            datatype = gdal.GDT_UInt16
        else:
            datatype = gdal.GDT_Float32

        if len(im_data.shape) == 3:
            im_bands, im_height, im_width = im_data.shape
        elif len(im_data.shape) == 2:
            # 不管是多少波段，矩阵的 shape 要统一为 (band_num, rows, cols) 形式？行列有没有反了
            im_data = np.array([im_data])
        else:
            im_bands, (im_height, im_width) = 1, im_data.shape

        driver = gdal.GetDriverByName("GTiff")
        dataset = driver.Create(out_path, im_width, im_height, im_bands, datatype)

        if dataset is not None:
            # 写入仿射变换参数
            dataset.SetGeoTransform(im_geotrans)
            # 写入投影
            dataset.SetProjection(im_proj)

        # 写入矩阵
        for i in range(im_bands):
            dataset.GetRasterBand(i + 1).WriteArray(im_data[i])
            if data_no_value is not None:
                dataset.GetRasterBand(i + 1).SetNoDataValue(data_no_value)
        del dataset


    """

    """



if __name__ == '__main__':
    issue='201802120000'
    inputFolder_cimiss=u'E:/anhui/reslut_test'
    inputFolder_ndvi=u'E:/anhui/EMI/cimiss_data/340000000000.tif'
    inputFolder_ndvi_last=u'E:/anhui/EMI/cimiss_data/340000000000.tif'
    delday='4'
    tempFolder=u'E:/anhui/temp'
    outputFolder=u'E:/anhui'
    city_shp=u'E:/htht/new/Depend/AnHui/CompShp/AreaCity.shp'

    a=EMI(issue,inputFolder_cimiss,inputFolder_ndvi,delday,tempFolder,outputFolder,city_shp)
    EMI,statistics=a.doprocess()






