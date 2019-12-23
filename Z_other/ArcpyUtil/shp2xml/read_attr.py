# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import arcpy
from xml.dom.minidom import Document
import sys

# FIXME, 新修改的要求 （1）只需要 id 和 name 就能做 （2）要支持多个级别数据的转换 （3）使用面向对象的方法来做

def main(shp_path_provience, shp_path_city, shp_path_country, xml_path):

    arcpy.gp.overwriteOutput = 1
    arcpy.CheckOutExtension("spatial")
    arcpy.env.workspace = r'C:\Users\lingdequan\Desktop\del'

    # 【2】得到等级和地理信息字典
    all_data_country = arcpy.da.SearchCursor(shp_path_country, ["id", "name", "xcenter", "ycenter", "xmin", "xmax", "ymin", "ymax"])
    shi_dict = {}
    all_area_data_dict = {}

    for country_data in all_data_country:
        xian_id = str(country_data[0])
        shi_id = xian_id[:4] + "00000000"

        if shi_id in shi_dict:
            shi_dict[shi_id][xian_id] = xian_id
        else:
            shi_dict[shi_id] = {}
            shi_dict[shi_id][xian_id] = xian_id

        #【2.1】存储县的信息

        country_info = {"id":str(country_data[0]), "name":str(country_data[1]),
                     "lon":str(country_data[2]), "lat":str(country_data[3]), "left":str(country_data[4]),
                     "right":str(country_data[5]), "bottom":str(country_data[6]), "top":str(country_data[7]),
                     "level":"3"}

        all_area_data_dict[xian_id] = country_info

    # 【2.2】存储市的信息
    all_data_city = arcpy.da.SearchCursor(shp_path_city, ["id", "name", "xcenter", "ycenter", "xmin", "xmax", "ymin", "ymax"])

    for city_data in all_data_city:

        city_info = {"id":str(city_data[0]), "name":str(city_data[1]),
                     "lon":str(city_data[2]), "lat":str(city_data[3]), "left":str(city_data[4]),
                     "right":str(city_data[5]), "bottom":str(city_data[6]), "top":str(city_data[7]),
                     "level":"2"}

        city_id = str(city_data[0])
        all_area_data_dict[city_id] = city_info

    # 【2.3】存储省的信息
    all_data_provience = arcpy.da.SearchCursor(shp_path_provience, ["id", "name", "xcenter", "ycenter", "xmin", "xmax", "ymin", "ymax"])

    for provience_data in all_data_provience:

        provience_info = {"id":str(provience_data[0]), "name":str(provience_data[1]),
                     "lon":str(provience_data[2]), "lat":str(provience_data[3]), "left":str(provience_data[4]),
                     "right":str(provience_data[5]), "bottom":str(provience_data[6]), "top":str(provience_data[7]),
                     "level":"1"}

        provience_id = str(provience_data[0])
        all_area_data_dict[provience_id] = provience_info

    print("OK")

    # 【3】写 xml

    def addSubNode(document, curNode, nodeKey, nodeValue, nodeAtt={}):
        """在节点下添加子节点信息"""
        try:
            child = document.createElement(nodeKey)
            # 写属性
            for attKey in nodeAtt:
                child.setAttribute(attKey, nodeAtt[attKey])
            # 写值
            if nodeValue:
                child_text = document.createTextNode(nodeValue)
                child.appendChild(child_text)
            # 添加节点
            curNode.appendChild(child)
        except :
            print("添加节点错误")
            pass

        return child

    document = Document()

    # 省级节点
    rootElement = document.createElement('provience')
    # logMap_province = all_area_data_dict["530000000000"]
    logMap_province = all_area_data_dict[provience_id]
    for each_attr in logMap_province:
        rootElement.setAttribute(each_attr, logMap_province[each_attr])
    document.appendChild(rootElement)

    # 市县级节点
    for each_city in shi_dict:
        country_dict = shi_dict[each_city]
        city_id = each_city
        # logMap_city = {"id":city_id}
        logMap_city = all_area_data_dict[city_id]
        cityElement = addSubNode(document, rootElement, "city", "", logMap_city)
        for each_country in country_dict:
            country_id = each_country
            logMap_country = all_area_data_dict[country_id]
            addSubNode(document, cityElement, "country", "", logMap_country)

    # 生成 xml 文件
    with open(xml_path, 'w') as f:
        f.write(document.toprettyxml(indent='\t', encoding='utf-8'))

if __name__ == "__main__":
    # shp_path_provience = r'C:\work_code\shp2xml\shp\GuiZhou_sheng.shp'
    # shp_path_country = r'C:\work_code\shp2xml\shp\GuiZhou_xian.shp'
    # shp_path_city = r'C:\work_code\shp2xml\shp\GuiZhou_shi.shp'
    # xml_path = r'C:\work_code\shp2xml\test004.xml'

    provience = r'C:\Users\lingdequan\Desktop\云南省\云南省\省级数据.shp'
    country = r'C:\Users\lingdequan\Desktop\云南省\云南省\市级数据.shp'
    city = r'C:\Users\lingdequan\Desktop\云南省\云南省\县级数据.shp'
    xml_path = r'C:\work_code\shp2xml\test_yunnan004.xml'


    main(provience, city, country, xml_path)

    # 可以优化的地方，中心纬度和上下左右都可以自己计算出来
    # 读取 shp 信息那一块可以写一个通用的函数，而不需要写三遍，我偷懒了