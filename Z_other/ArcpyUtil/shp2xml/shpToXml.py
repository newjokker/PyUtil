# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import arcpy
import copy
from xml.dom.minidom import Document

class ShpToXml:

    def __init__(self, provienceShpPath, cityShpPath, countryShpPath, xmlPath, tempPath):
        self.__provienceShpPath = provienceShpPath
        self.__cityShpPath = cityShpPath
        self.__countryShpPath = countryShpPath

        self.__xmlPath = xmlPath
        self.__tempPath = tempPath

        self.__fieldNameStr = {"provience":"name", "city":"name", "country":"name"} # name 在属性表中的 表头的名字 #FIXME 有的情况，在不同的 shp 中 name 不是同一个字段那就恶心了(先放弃这个功能)
        self.__fieldIdStr   = {"provience":"id", "city":"id", "country":"id"} # id 在属性表中的 表头的名字

        self.__shpClassDict = {}  # {provienceId: {cityId: [countryId]}} # 等级信息
        self.__shpInfoDict  = {}  # {id : {id: info}}  # 属性信息

        self.__needCalculateFieldNames = ["lon", "lat", "right", "left", "top", "bottom", "area"] # 需要计算的属性 []
        # self.__needCalculateFieldNames = ["lon", "lat", "right", "left", "top", "bottom","area"] # 需要计算的属性 []

        # FIXME 需要转为以度为单位的形式，而不是米
        self.__attributeDict = {"lon":"!SHAPE.CENTROID.X!",     "lat":"!SHAPE.CENTROID.Y!",
                                "left":"!shape.extent.xmin!",   "right":"!shape.extent.xmax!",
                                "bottom":"!shape.extent.ymin!", "top":"!shape.extent.ymax!",
                                "area":"!shape.area!",
                                }

    def __arcpy_init(self):
        """初始化arcpy"""
        arcpy.gp.overwriteOutput = True
        arcpy.CheckOutExtension("spatial")
        arcpy.env.workspace = self.__tempPath

    def set__fieldNameStr(self, shpFieldName, shpClass):
        """设置 自定义 name 字段"""
        if shpClass in self.__fieldNameStr:
            self.__fieldNameStr[shpClass] = shpFieldName.lower()

    def set__fieldIdStr(self, shpIdName, shpClass):
        """设置 自定义 id 字段"""
        if shpClass in self.__fieldIdStr:
            self.__fieldIdStr[shpClass] = shpIdName

    def __check_shp_attribure(self, shpPath, shpClass):
        """检查数据是否已准备完善"""
        # 检查是否包含 name 和 id 字段, 或者自定义 name id 字段
        needField = [self.__fieldNameStr[shpClass], self.__fieldIdStr[shpClass]]
        desc = arcpy.Describe(shpPath)

        for field in desc.fields:
            # print(field.name)
            if field.name.lower() in needField:
                needField.remove(field.name.lower())

        if needField:
            print("图层 {0} 没有需要的 id 或 name 属性，不可用".format(shpPath))
            return False
        else:
            print("图层 {0} 检查完毕，符合出xml要求".format(shpPath))
            return True

    def __fix_shp_attr(self, shpPath):
        """修复 shp 的属性表"""
        # 0. 查看是否有需要的字段，因为不能新建相同的字段
        needCalculateFieldNames = copy.deepcopy(self.__needCalculateFieldNames) # 为了不让修改原值，使用深拷贝

        desc = arcpy.Describe(shpPath)
        for field in desc.fields:
            if field.name in needCalculateFieldNames:
                needCalculateFieldNames.remove(field.name)

        # 1. 增加缺失字段(中心经纬度，上下左右极值)
        for eachFieldName in needCalculateFieldNames:
            arcpy.AddField_management(shpPath, eachFieldName, "DOUBLE", 18, 11)

        # 2. 计算得到缺失的字段(单位设为度)
        for eachFieldName in needCalculateFieldNames:
            arcpy.CalculateField_management(shpPath, eachFieldName, self.__attributeDict[eachFieldName], "Python_9.3")

        print("图层 {0} 修复完成".format(str(shpPath)))

    def __get_shp_info(self, shpPath, shpClass, classStr):
        """获取 shp 的属性信息"""
        # 需要获取的信息比需要计算的信息多两个
        # needGetFieldNames = [self.__fieldIdStr[shpClass], self.__fieldNameStr[shpClass]] + self.__needCalculateFieldNames
        # FIXME 这里有时候是 shape_Area 或者  shapeArea
        needGetFieldNames = [self.__fieldIdStr[shpClass], self.__fieldNameStr[shpClass], 'area'] + self.__needCalculateFieldNames

        for shpAttrLine in arcpy.da.SearchCursor(shpPath, needGetFieldNames):
        # for shpAttrLine in arcpy.da.SearchCursor(shpPath, ['id', 'name']):
            print(shpAttrLine)
            areaId   = unicode(shpAttrLine[0])
            infoDictTemp = dict()
            for eachFieldIndex in range(len(needGetFieldNames)):
                infoDictTemp[needGetFieldNames[eachFieldIndex]] = unicode(shpAttrLine[eachFieldIndex]) # FIXME 编码问题找时间解决一下

            # 将自定义属性改为 id
            if not self.__fieldIdStr[shpClass] == "id":
                infoDictTemp["id"] = infoDictTemp[self.__fieldIdStr[shpClass]]
                infoDictTemp.pop(self.__fieldIdStr[shpClass])

            # 将自定义属性改为 name
            if not self.__fieldNameStr[shpClass] == "name":
                infoDictTemp["name"] = infoDictTemp[self.__fieldNameStr[shpClass]]
                infoDictTemp.pop(self.__fieldNameStr[shpClass])

            # 增加等级信息 class
            infoDictTemp["class"] = str(classStr)

            self.__shpInfoDict[areaId] = infoDictTemp
        print("成功获取 {0} 图层属性信息".format(str(shpPath)))

    def __get_class_info(self):
        """ 获取等级信息 """
        # FIXME 这个设定为获取最小级别的数据的等级信息，这边现在还不能做到通用，需要继续优化
        # 1. 读取省的信息
        needGetFieldNames =  [self.__fieldIdStr["provience"], self.__fieldNameStr["provience"]] + self.__needCalculateFieldNames
        for shpAttrLine in arcpy.da.SearchCursor(self.__provienceShpPath, needGetFieldNames):
            provienceId = str(shpAttrLine[0])
            self.__shpClassDict[provienceId] = {}

        # 2. 读取市的信息
        needGetFieldNames =  [self.__fieldIdStr["city"], self.__fieldNameStr["city"]] + self.__needCalculateFieldNames
        for shpAttrLine in arcpy.da.SearchCursor(self.__cityShpPath, needGetFieldNames):
            cityId      = str(shpAttrLine[0])
            # -----------------------------------------------------------------------------------
            provienceId = cityId[:2] + "0"*10
            # provienceId = cityId[:1] + "0"*5
            # provienceId = 'QHS'
            # -----------------------------------------------------------------------------------
            # provienceId = cityId[:4] +   "00000000"
            # -----------------------------------------------------------------------------------
            if not provienceId in self.__shpClassDict: # 字典中没有添加当前省的信息
                self.__shpClassDict[provienceId] = {}

            self.__shpClassDict[provienceId][cityId] = []

        # 3. 读取县的信息
        needGetFieldNames =  [self.__fieldIdStr["country"], self.__fieldNameStr["country"]] + self.__needCalculateFieldNames
        for shpAttrLine in arcpy.da.SearchCursor(self.__countryShpPath, needGetFieldNames):
            countryId   = str(shpAttrLine[0])
            # -----------------------------------------------------------------------------------
            cityId      = countryId[:4] + "0"*8
            provienceId = countryId[:2] + "0"*10
            # -----------------------------------------------------------------------------------
            # cityId      = countryId[:3] + "0"*3
            # provienceId = countryId[:1] + "0"*5
            # -----------------------------------------------------------------------------------
            # cityId      = countryId[:1] + "0"*5
            # provienceId = 'QHS'
            # -----------------------------------------------------------------------------------

            if not provienceId in self.__shpClassDict: # 字典中没有添加当前省的信息
                self.__shpClassDict[provienceId] = {}

            if not cityId in self.__shpClassDict[provienceId]: # 字典中没有添加当前市的信息
                self.__shpClassDict[provienceId][cityId] = []

            self.__shpClassDict[provienceId][cityId].append(countryId)

        print("成功获取等级信息 ")

    def __get_xml(self):
        """根据计算出来的信息得到 xml """
        # 1. 生成 xml 节点信息
        document = Document()
        region = None

        for num, eachProvienceId in enumerate(self.__shpClassDict):
            # 1.1 添加省节点, 当只有一个省的时候省作为根节点，多个省nation作为根节点（因为xml中只有一个根节点，所以要）
            if len(self.__shpClassDict) > 1 and num == 0: # 当有多个省的数据的时候，在遍历第一个省的时候增加区域节点
                region = self.addSubNode(document, document, "nation", "", {})  # 添加区域节点（多个省的集合）

            # 1.1.1 对于多个省的情况，region 作为根节点
            if len(self.__shpClassDict) > 1:
                procienceNodeTemp = self.addSubNode(document, region, "provience", "", self.__shpInfoDict[eachProvienceId])
            # 1.1.2 对于一个省的情况，省节点作为跟节点
            else:
                procienceNodeTemp = self.addSubNode(document, document, "provience", "", self.__shpInfoDict[eachProvienceId])

            for eachCityId in self.__shpClassDict[eachProvienceId]:
                # 1.2 添加市节点
                try:
                    cityNodeTemp = self.addSubNode(document, procienceNodeTemp, "city", "", self.__shpInfoDict[eachCityId])
                    for eachCountryId in self.__shpClassDict[eachProvienceId][eachCityId]:
                        # 1.3 添加县节点
                        self.addSubNode(document, cityNodeTemp, "country", "", self.__shpInfoDict[eachCountryId])
                except:
                    print('没有这个市')
        # 2. 写 xml 文件
        with open(self.__xmlPath, 'w') as f:
            f.write(document.toprettyxml(indent='\t', encoding='utf-8'))

    @staticmethod
    def addSubNode(document, curNode, nodeKey, nodeValue, nodeAtt={}):
        """在节点下添加子节点信息"""
        if nodeAtt is None:
            nodeAtt = {}
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
            return child

        except:
            print("添加节点错误")
            return None

    def do_process(self):
        """ 流程 """
        # 1. 初始化，检查参数等
        self.__arcpy_init()

        if not(self.__check_shp_attribure(self.__countryShpPath, "country") and
               self.__check_shp_attribure(self.__cityShpPath, "city") and
               self.__check_shp_attribure(self.__provienceShpPath, "provience")):
            print("输入图层属性有误，需手动修正")
            return False
        print("-"*100)

        # 2. 修复图层
        self.__fix_shp_attr(self.__cityShpPath)
        self.__fix_shp_attr(self.__countryShpPath)
        self.__fix_shp_attr(self.__provienceShpPath)
        print("-"*100)

        # 3. 获取图层信息，等级信息
        self.__get_class_info()
        self.__get_shp_info(self.__countryShpPath, "country", 3)
        self.__get_shp_info(self.__cityShpPath, "city", 2)
        self.__get_shp_info(self.__provienceShpPath, "provience", 1)
        print("-"*100)

        # 4. 生成xml
        self.__get_xml()
        print("xml 已生成")
        return True


if __name__ == "__main__":

    # provience   = r'C:\Users\Administrator\Desktop\依赖注入\del_shp\province.shp'
    # city        = r'C:\Users\Administrator\Desktop\依赖注入\del_shp\city.shp'
    # country     = r'C:\Users\Administrator\Desktop\依赖注入\del_shp\country.shp'

    # provience   = r'C:\Users\Administrator\Desktop\GZ_shp_xml\AreaProvince.shp'
    # city        = r'C:\Users\Administrator\Desktop\GZ_shp_xml\AreaCity.shp'
    # country     = r'C:\Users\Administrator\Desktop\GZ_shp_xml\AreaCounty.shp'

    provience   = r'C:\Users\Administrator\Desktop\china_shp\CompShp\AreaProvince.shp'
    city        = r'C:\Users\Administrator\Desktop\china_shp\CompShp\AreaCity.shp'
    country     = r'C:\Users\Administrator\Desktop\china_shp\CompShp\AreaCounty.shp'

    xml_path     = r'C:\Users\Administrator\Desktop\GZ.xml'
    temp_path    = r"C:\Users\lingdequan\Desktop\del"

    a = ShpToXml(provienceShpPath=provience, cityShpPath=city, countryShpPath=country, xmlPath=xml_path, tempPath=temp_path)

    a.set__fieldNameStr("NAME", "provience")
    a.set__fieldNameStr("NAME", "city")
    a.set__fieldNameStr("NAME", "country")

    a.set__fieldIdStr("id", "provience")
    a.set__fieldIdStr("id", "city")
    a.set__fieldIdStr("id", "country")

    a.do_process()

    # FIXME 下一版本的更新，只用一个 shp 进行转换的时候，需要知道其他高级区域的名字，id是可以推断的，但是名字不行（想办法解决）
    # FIXME 不适用于需要推断的字段，必须严格符合省市县 id 的逻辑才行
    # FIXME 增加 region 属性内容，可以将 省 shp 合并之后获取各个属性，regionId、regionName 需要提前设置，或者生成后手动修改

