# -*- coding: utf-8 -*-
"""
Created on Mon Apr 02 10:38:27 2018

@author: Administrator
"""

# coding=utf8
'''
Modified in 2018/11/09

@author: huxuran
'''
import urllib2
import sys
import time
import os
import calendar
import string
import datetime
# import Compute_MonAvg
# import uuid
#from collections import OrderedDict
##有些输出是中文字符，统一设置一下编码
#reload(sys) 
#sys.setdefaultencoding('utf8')
def getYearData(DataType,date_list,var,txt_path):
    for i in range(len(date_list)):
        strTime1 = date_list[i]
#             strTime = strTime+"000000"
        URL = "http://10.129.89.17:8008/cimiss-web/api"
        dicts = ([('userId', 'user_qks'),\
                         ('pwd', 'user_qks123'),\
                         ('interfaceId','getSurfEleInRegionByTime'),\
                         ('dataCode','SURF_CHN_MUL_'+DataType),\
                         ('times',strTime1),\
                         ('adminCodes','340000'),\
                         ('elements','Station_ID_C'+','+'Lon'+','+'Lat'+','+'TEM'+','+'RHU'+','+'PRE'+','+var),\
                         ('orderby','Station_ID_C:ASC'),\
                         ('dataFormat','')])

        month = strTime1[4:6]
        day_1 = strTime1[6:8]
        hour = strTime1[8:10]
        item=dicts
        urls="?"
        for i in item:
            (key,value)=i
            temp_str = key+"="+value
            urls = urls + temp_str+"&"
        urls = urls[:len(urls)-1]
        baseUrl = URL + urls
        dataFormat = 'text'
        req = urllib2.Request(baseUrl + dataFormat)
        response = urllib2.urlopen(req)
        data = response.read()
#             txt_path = "E:\\temp\\cimiss_data_03"
        if not os.path.exists(txt_path):
            os.makedirs(txt_path)
        file1_path = txt_path + "\\" + "temp_" + month+'_'+ day_1+'_'+hour+ ".txt"
        with open(file1_path,"w") as f:
            f.write(data)
        file1 = open(file1_path,"r")
        line = file1.readline()
#         line = file1.readline()
        file2_path = txt_path + "\\" + strTime1[0:4] + month+ day_1+hour+ ".txt"
        file2 = open(file2_path,"w")
        while 1:
            line = file1.readline()
            if len(var)>10:
                if var in line:
                    line.replace(var,var[0:10])
            if (line ==''):
                break
            elif(line =='\n'):
                continue
            else:
                line = line.replace(' ',',')
                line = line.replace('\r','')

            file2.write(line)
    #     ID2 = uuid.uuid1()
        file1.close()
        file2.close()
        os.remove(file1_path)

def gettimelist(begin_issue,end_issue):
    end_issue_all = str(int (end_issue) + 2300)
    begin_date = datetime.datetime.strptime(begin_issue, "%Y%m%d%H%M")  # str -> date
    end_date = datetime.datetime.strptime(end_issue_all, "%Y%m%d%H%M")
    date_list = []
    while begin_date <= end_date:
        curissue = begin_date.strftime ("%Y%m%d%H%M")  # date -> str
        issue = ""
        deltday = 0
        delthour = 0
        issue = curissue[0:10] + "0000"  # 小时后面赋值为0
        deltday = 0
        delthour = 1
        date_list.append(issue)
        begin_date = datetime.datetime.strptime(issue, "%Y%m%d%H%M%S")
        begin_date += datetime.timedelta(days=deltday, hours=delthour)
    return date_list
def getcimissData(txtPath,end_issue,begin_issue):
    var_list = ['VIS']
    date_list = gettimelist(begin_issue,end_issue)
    for var in var_list:
        getYearData("HOR",date_list,var,txtPath)