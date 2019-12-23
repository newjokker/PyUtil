# # -*- coding: utf-8 -*-
#
# # """
# # Modified in 2016/03/28
# # @author: huxuran (一作，通讯作者)
# # @author: jokker (二作)
# # """
# #
# # import urllib2
# # import sys
# #
# # reload(sys)
# # sys.setdefaultencoding('utf8')
# #
# # class GetDataFromCimiss:
# #     """从Cimiss下载数据"""
# #
# #     def __init__(self, info_dict=None, **kwargs):
# #         self.URL=None
# #         self.userID=None
# #         self.pwd=None
# #         self.interfaceId=None  # FIXME 所有的给默认值，
# #         self.dataCode=None
# #         self.timeRange=None
# #         self.adminCodes=None
# #         self.elements=None
# #         self.orderby=None
# #         self.dataType=None
# #         self.dataFormat=None  # 下载的文件的形式，是txt还是穷他的什么
# #
# #         self.__config_list=[]
# #         self.__base_url=None
# #         self.__cimiss_data=None  # 从 cimiss 下载的数据
# #
# #         # 可以输入一个字典信息
# #         if isinstance(info_dict, dict):
# #             pass
# #
# #         # 可以一个个输入信息
# #
# #     def do_pocess(self, save_path=None):
# #         """快速模式，也是经典模式"""
# #         self.__config2url()
# #         self.__print_config()
# #         self.__load_data_from_browser()
# #
# #         if save_path:
# #             self.save_cimiss_data(save_path)
# #
# #     def save_cimiss_data(self, save_path):
# #         """保存从cimiss中下载的数据"""
# #
# #         # 【0】获取保存的格式，若是不是在已支持的文件里面，报错退出
# #
# #         # 【1】根据路径判断需要保存的格式
# #         with open(save_path, 'w') as save_txt_path:
# #             for each_line in self.__cimiss_data.split("\n"):
# #                 save_txt_path.write(each_line)
# #
# #     # -- -- -- -- -- -- 内置函数 -- -- -- -- -- -- --
# #
# #     def __config2url(self):
# #         """拼装字典, 记得 URL 是不需要拼装到字典里面的！"""
# #
# #         self.__config_list.extend([("userID",   self.userID)])
# #         self.__config_list.extend([("pwd",      self.pwd)])
# #         self.__config_list.extend([("orderby",  self.orderby)])
# #         self.__config_list.extend([("interfaceId",  self.interfaceId)])
# #         self.__config_list.extend([("dataCode",     self.dataCode)])
# #         self.__config_list.extend([("timeRange",    self.timeRange)])
# #         self.__config_list.extend([("adminCodes",   self.adminCodes)])
# #         self.__config_list.extend([("elements",     self.elements)])
# #         self.__config_list.extend([("dataFormat",   self.dataFormat)])
# #
# #         # 根据输入的信息拼接 base_url
# #         urls = "?"
# #         for config_data in self.__config_list:
# #             urls += "=".join(config_data) + "&"
# #
# #         self.__base_url = self.URL + urls.rstrip("&")
# #
# #     def __print_config(self):
# #         """打印出配置和URL"""
# #         print("-"*20 + " 参数信息 " + "-"*25)
# #
# #         for each_config in self.__config_list:
# #             print(str(each_config[0])+ " "*(15 - len(str(each_config[0]))) + " : " + str(each_config[1]))
# #
# #         print("base_url        : " + self.__base_url)
# #         print("-"*56)
# #
# #         print(self.__base_url)
# #
# #     def __load_data_from_browser(self):
# #         """从网页获取数据"""
# #         req = urllib2.Request(self.__base_url)
# #         response = urllib2.urlopen(req)
# #         self.__cimiss_data = str(response.read())
# #
# #     def __format_cimiss_data(self):
# #         """将获取的数据转为规范化的格式，不管获取的是什么数据，最后只能有一种规范化格式"""
# #         pass
# #
# #     def __print_cimiss_data(self):
# #         """打印从cimiss下载的数据"""
# #         if self.dataType.lower() == "text":
# #             for each_line in self.__cimiss_data:
# #                 print(each_line)
# #         elif self.dataType.lower() == "json":
# #             pass
# #
# # if __name__ == '__main__':
# #
# #     # getData('DAY', 12)
# #
# #     a = GetDataFromCimiss()
# #     a.userID = 'BEXN_KYS_ygzx'
# #     a.pwd = '6151653'
# #     # a.elements = 'Lat,Lon,TEM_Avg,PRE_Time_2020,SSH,TEM_Min'
# #     #a.elements = 'Station_Id_C,Lat,Lon,Year,Mon,Day,PRE_Time_2008,PRE_Time_0820,PRE_Time_2020,PRE_Time_0808'
# #     a.elements = 'Lat,Lon,TEM_Avg,PRE_Time_2020,SSH,TEM_Min'
# #     a.timeRange = "[20000101000000,20180701000000]"
# #     a.adminCodes = "520000"
# #     a.orderby = "Lat:ASC"
# #     a.dataType = "DAY"
# #     a.dataFormat = "json"
# #     a.dataFormat = "text"
# #     a.interfaceId = "getSurfEleInRegionByTime"
# #     a.dataCode = "SURF_CHN_MUL_" + a.dataType
# #     a.URL = "http://10.181.89.55/cimiss-web/api"
# #
# #     a.do_pocess()
# #     a.save_cimiss_data(r"C:\Users\Administrator\Desktop\TEMP\DAY\2008\all1.txt")
#
#
#
#     # TODO 设置一种向导模式，这样的话就能直接和用户交互了，虽然这样会比较的慢，但是成功一次之后就可以保存输入的记录下次再重新载入即可
#
#     # http://10.181.89.55/cimiss-web/api?userId=BEXN_KYS_ygzx&pwd=6151653&dataFormat=json&interfaceId=getSurfEleInRegionByTimeRange&dataCode=SURF_CHN_MUL_DAY&adminCodes=520000&timeRange=[20180926000000,20180929010000]&elements=Station_Id_C,Lat,Lon,Year,Mon,Day,PRE_Time_2008,PRE_Time_0820,PRE_Time_2020,PRE_Time_0808&dataFormat=json
#
# # 小胡老师原版代码
# '''
# Modified in 2016/03/28
#
# @author: huxuran
# '''
# import urllib2
# import sys
# import uuid
# import os
# import csv
# import datetime
#
# # from collections import OrderedDict
# ##锟斤拷些锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷址锟斤拷锟酵骋伙拷锟斤拷锟揭伙拷卤锟斤拷锟?
# reload(sys)
#
# sys.setdefaultencoding('utf8')
#
#
# def txt2xls(filename, xlsname):  # 文本转换成xls的函数，filename 表示一个要被转换的txt文本，xlsname 表示转换后的文件名
#     print 'converting xls ... '
#     f = open(filename)  # 打开txt文本进行读取
#     x = 0  # 在excel开始写的位置（y）
#     y = 0  # 在excel开始写的位置（x）
#     xls = xlwt.Workbook()
#     sheet = xls.add_sheet('sheet1', cell_overwrite_ok=True)  # 生成excel的方法，声明excel
#     line = f.readline()
#     for i in line.split(','):  # 读取出相应的内容写到x
#         item = i.strip().decode('utf8')
#         sheet.write(x, y, item)
#         y += 1  # 另起一列
#     x += 1  # 另起一行
#     y = 0  # 初始成第一列
#     while True:  # 循环，读取文本里面的所有内容
#         line = f.readline()  # 一行一行读取
#         if not line:  # 如果没有内容，则退出循环
#             break
#         for i in line.split(','):  # 读取出相应的内容写到x
#             item = float(i.strip().decode('utf8'))
#             sheet.write(x, y, item)
#             y += 1  # 另起一列
#         x += 1  # 另起一行
#         y = 0  # 初始成第一列
#     f.close()
#     xls.save(xlsname + '.xls')  # 保存
#
#
# def getData(DataType, strTime):
#     #     strTime='20150101000000'
#     URL = "http://10.181.89.55/cimiss-web/api"
#     dicts = ([('userId', 'BEXN_KYS_ygzx'), \
#               ('pwd', '6151653'), \
#               ('interfaceId', 'getSurfEleInRegionByTime'), \
#               ('dataCode', 'SURF_CHN_MUL_' + DataType), \
#               ('times', strTime), \
#               ('adminCodes', '520000'), \
#               ('elements', 'Lat,Lon,TEM_Avg,PRE_Time_2020,SSH,TEM_Min'), \
#               ('orderby', 'Lat:ASC'), \
#               ('dataFormat', '')])
#     item = dicts
#     urls = "?"
#     for i in item:
#         (key, value) = i
#         temp_str = key + "=" + value
#         urls = urls + temp_str + "&"
#     urls = urls[:len(urls) - 1]
#     baseUrl = URL + urls
#     #     baseUrl = 'http://10.181.89.55/cimiss-web/api?userId=BEXN_KYS_ygzx&pwd=6151653&interfaceId=getSurfEleInRegionByTime&dataCode=SURF_CHN_MUL_YER&times=20150101000000&adminCodes=310000,320000,330000,340000,350000,360000,410000,420000,430000,440000,450000&elements=Station_Name,Province,City,Cnty,Station_Id_C,Station_Id_d,Lat,Lon,TEM_Avg,RHU_Avg,PRE_Time_2020,WIN_S_2mi_Avg,WIN_S_A5ms_Days&dataFormat='
#     # 1.4 锟斤拷锟叫伙拷锟斤拷式
#     dataFormat = 'text'
#     # 2. 锟斤拷锟矫接匡拷
#     req = urllib2.Request(baseUrl + dataFormat)
#     response = urllib2.urlopen(req)
#     data = response.read()
#     file1_path = "C:\\Users\\Administrator\\Desktop\\TEMP\\" + DataType + '\\' + strTime + ".txt"
#     with open(file1_path, "w") as f:
#         f.write(data)
#     file1 = open(file1_path, "r")
#     line = file1.readline()
#     #        txt_root = "D:\\htht\\xueshen"
#     file2_path = "C:\\Users\\Administrator\\Desktop\\NPPdata\\" + DataType + '\\' + strTime + ".txt"
#     file2 = open(file2_path, "w")
#     while 1:
#         line = file1.readline()
#         if (line == ''):
#             break
#         elif (line == '\n' or (line.find("999") != -1)):
#             continue
#         else:
#             line = line.replace(' ', ',')
#             line = line.replace('\n', '')
#             line = line.replace('\r', '\n')
#             if line[-1] == ",":
#                 line = ""
#             elif line.split(',')[-2] == '':
#                 line = ""
#             else:
#                 line = line
#         file2.write(line)
#     file3_path = "C:\\Users\\Administrator\\Desktop\\NPPdata\\"+DataType+'\\'+strTime+".xls"
#     csvcontent = file(file3_path,'wb')
#     writer = csv.writer(csvcontent)
# #
#     for line in open(file2_path).readlines():
#         writer.writerow([a for a in line.split('\n')])
# #
#     csvcontent.save_file()
#
#     with open(file3_path, 'wb') as csvfile:
#         spamwriter = csv.writer(csvfile, dialect='excel')
#     # 读要转换的txt文件，文件每行各词间以@@@字符分隔
#         with open(file2_path, 'rb') as filein:
#             line = filein.readline()
#             spamwriter.writerow(line)
#     file1.close()
#     file2.close()
#
#     # 3. 锟斤拷锟斤拷涌锟?
#
#
# if __name__ == '__main__':
#         strTime1 = ['20170601','20170602','20170603','20170604','20170605','20170606','20170607','20170608','20170609','20170610','20170611','20170612','20170613','20170614','20170615','20170616','20170617','20170618','20170619','20170620','20170621','20170622','20170623','20170624','20170625','20170626','20170627','20170628','20170629','20170630']
#         for i in strTime1:
#             i = i+'000000'
#             DataType1 = 'DAY'
#             getData(DataType1,i)
#     #     strTime2 = ['20180101','20180201','20180301','20180401','20180501','20180601','20180701','20180801']
#     #     start='20170101'
#     #     end='20180101'
#     # # #
#     #     datestart=datetime.datetime.strptime(start,'%Y%m%d')
#     #     dateend=datetime.datetime.strptime(end,'%Y%m%d')
#     #     datelist=[]
#     #
#     #     while datestart<dateend:
#     #         date_everyday = datestart.strftime('%Y%m%d')
#     #         print date_everyday
#     #         datelist.append(date_everyday)
#     #         datestart+=datetime.timedelta(days=1)
#     #     strTime2 = ['20170101', '20170102', '20170103', '20170104', '20170105', '20170106', '20170107', '20170108', '20170109', '20170110', '20170111', '20170112', '20170113', '20170114', '20170115', '20170116', '20170117', '20170118', '20170119', '20170120', '20170121', '20170122', '20170123', '20170124', '20170125', '20170126', '20170127', '20170128', '20170129', '20170130', '20170131', '20170201', '20170202', '20170203', '20170204', '20170205', '20170206', '20170207', '20170208', '20170209', '20170210', '20170211', '20170212', '20170213', '20170214', '20170215', '20170216', '20170217', '20170218', '20170219', '20170220', '20170221', '20170222', '20170223', '20170224', '20170225', '20170226', '20170227', '20170228', '20170301', '20170302', '20170303', '20170304', '20170305', '20170306', '20170307', '20170308', '20170309', '20170310', '20170311', '20170312', '20170313', '20170314', '20170315', '20170316', '20170317', '20170318', '20170319', '20170320', '20170321', '20170322', '20170323', '20170324', '20170325', '20170326', '20170327', '20170328', '20170329', '20170330', '20170331', '20170401', '20170402', '20170403', '20170404', '20170405', '20170406', '20170407', '20170408', '20170409', '20170410', '20170411', '20170412', '20170413', '20170414', '20170415', '20170416', '20170417', '20170418', '20170419', '20170420', '20170421', '20170422', '20170423', '20170424', '20170425', '20170426', '20170427', '20170428', '20170429', '20170430', '20170501', '20170502', '20170503', '20170504', '20170505', '20170506', '20170507', '20170508', '20170509', '20170510', '20170511', '20170512', '20170513', '20170514', '20170515', '20170516', '20170517', '20170518', '20170519', '20170520', '20170521', '20170522', '20170523', '20170524', '20170525', '20170526', '20170527', '20170528', '20170529', '20170530', '20170531', '20170601', '20170602', '20170603', '20170604', '20170605', '20170606', '20170607', '20170608', '20170609', '20170610', '20170611', '20170612', '20170613', '20170614', '20170615', '20170616', '20170617', '20170618', '20170619', '20170620', '20170621', '20170622', '20170623', '20170624', '20170625', '20170626', '20170627', '20170628', '20170629', '20170630', '20170601', '20170602', '20170603', '20170604', '20170605', '20170606', '20170607', '20170608', '20170609', '20170610', '20170611', '20170612', '20170613', '20170614', '20170615', '20170616', '20170617', '20170618', '20170619', '20170620', '20170621', '20170622', '20170623', '20170624', '20170625', '20170626', '20170627', '20170628', '20170629', '20170630', '20170631', '20170801', '20170802', '20170803', '20170804', '20170805', '20170806', '20170807', '20170808', '20170809', '20170810', '20170811', '20170812', '20170813', '20170814', '20170815', '20170816', '20170817', '20170818', '20170819', '20170820', '20170821', '20170822', '20170823', '20170824', '20170825', '20170826', '20170827', '20170828', '20170829', '20170830', '20170831', '20170901', '20170902', '20170903', '20170904', '20170905', '20170906', '20170907', '20170908', '20170909', '20170910', '20170911', '20170912', '20170913', '20170914', '20170915', '20170916', '20170917', '20170918', '20170919', '20170920', '20170921', '20170922', '20170923', '20170924', '20170925', '20170926', '20170927', '20170928', '20170929', '20170930', '20171001', '20171002', '20171003', '20171004', '20171005', '20171006', '20171007', '20171008', '20171009', '20171010', '20171011', '20171012', '20171013', '20171014', '20171015', '20171016', '20171017', '20171018', '20171019', '20171020', '20171021', '20171022', '20171023', '20171024', '20171025', '20171026', '20171027', '20171028', '20171029', '20171030', '20171031', '20171101', '20171102', '20171103', '20171104', '20171105', '20171106', '20171107', '20171108', '20171109', '20171110', '20171111', '20171112', '20171113', '20171114', '20171115', '20171116', '20171117', '20171118', '20171119', '20171120', '20171121', '20171122', '20171123', '20171124', '20171125', '20171126', '20171127', '20171128', '20171129', '20171130', '20171201', '20171202', '20171203', '20171204', '20171205', '20171206', '20171207', '20171208', '20171209', '20171210', '20171211', '20171212', '20171213', '20171214', '20171215', '20171216', '20171217', '20171218', '20171219', '20171220', '20171221', '20171222', '20171223', '20171224', '20171225', '20171226', '20171227', '20171228', '20171229', '20171230', '20171231']
#     #     strTime2 = ['20160101','20160201','20160301','20160401','20160601','20160601','20160701','20160801','20160901','20161001','20161101','20161201','20150101','20150201','20150301','20150401','20150601','20150601','20150701','20150801','20150901','20151001','20151101','20151201','20140101','20140201','20140301','20140401','20140601','20140601','20140701','20140801','20140901','20141001','20141101','20141201']
#     #     strTime2 = ['20170101','20170201','20170301','20170401','20170501','20170601','20170601','20170801','20170901','20171001','20171101','20171201']
#     #     strTime2 = ["20170101","20170102"]
#     #     for i in strTime2:
#     #         DataType1 = 'MON'
#     #         i = i+'000000'
# #     getData('DAY', 12)
#         print("ok")