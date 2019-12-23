# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import urllib2
import sys

reload(sys)


# FIXME 这个要重写，写简单一些

class GetDataFromCimiss:
    """从Cimiss下载数据"""

    def __init__(self, info_dict=None, **kwargs):
        self.URL=None
        self.userID=None
        self.pwd=None
        self.interfaceId=None  # FIXME 所有的给默认值，
        self.dataCode=None
        self.timeRange=None
        self.adminCodes=None
        self.elements=None
        self.orderby=None
        self.dataType=None
        self.dataFormat=None  # 下载的文件的形式，是txt还是穷他的什么

        self.__config_list=[]
        self.__base_url=None
        self.__cimiss_data=None  # 从 cimiss 下载的数据

        # 可以输入一个字典信息
        if isinstance(info_dict, dict):
            pass

        # 可以一个个输入信息

    def do_pocess(self, save_path=None):
        """快速模式，也是经典模式"""
        self.__config2url()
        self.__print_config()
        self.__load_data_from_browser()

        if save_path:
            self.save_cimiss_data(save_path)

    def save_cimiss_data(self, save_path):
        """保存从cimiss中下载的数据"""

        # 【0】获取保存的格式，若是不是在已支持的文件里面，报错退出

        # 【1】根据路径判断需要保存的格式
        with open(save_path, 'w') as save_txt_path:
            for each_line in self.__cimiss_data.split("\n"):
                save_txt_path.write(each_line)

    # -- -- -- -- -- -- 内置函数 -- -- -- -- -- -- --

    def __config2url(self):
        """拼装字典, 记得 URL 是不需要拼装到字典里面的！"""

        self.__config_list.extend([("userID",   self.userID)])
        self.__config_list.extend([("pwd",      self.pwd)])
        self.__config_list.extend([("orderby",  self.orderby)])
        self.__config_list.extend([("interfaceId",  self.interfaceId)])
        self.__config_list.extend([("dataCode",     self.dataCode)])
        self.__config_list.extend([("timeRange",    self.timeRange)])
        self.__config_list.extend([("adminCodes",   self.adminCodes)])
        self.__config_list.extend([("elements",     self.elements)])
        self.__config_list.extend([("dataFormat",   self.dataFormat)])

        # 根据输入的信息拼接 base_url
        urls = "?"
        for config_data in self.__config_list:
            urls += "=".join(config_data) + "&"

        self.__base_url = self.URL + urls.rstrip("&")

    def __print_config(self):
        """打印出配置和URL"""
        print("-"*20 + " 参数信息 " + "-"*25)

        for each_config in self.__config_list:
            print(str(each_config[0])+ " "*(15 - len(str(each_config[0]))) + " : " + str(each_config[1]))

        print("base_url        : " + self.__base_url)
        print("-"*56)

        print(self.__base_url)

    def __load_data_from_browser(self):
        """从网页获取数据"""
        req = urllib2.Request(self.__base_url)
        response = urllib2.urlopen(req)
        self.__cimiss_data = str(response.read())

    def __format_cimiss_data(self):
        """将获取的数据转为规范化的格式，不管获取的是什么数据，最后只能有一种规范化格式"""
        pass

    def __print_cimiss_data(self):
        """打印从cimiss下载的数据"""
        if self.dataType.lower() == "text":
            for each_line in self.__cimiss_data:
                print(each_line)
        elif self.dataType.lower() == "json":
            pass
