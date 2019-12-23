# -*-coding:utf-8 -*-
import os
import sys
import datetime
import xml.dom.minidom
from xml.dom.minidom import Document
import datetime
# from Decorator.time_it import time_this


class NcFileToTiff(object):
    """传入 nc 文件，输出 tiff 文件"""

    def __init__(self):
        # 需要处理的文件
        self.files_to_transform = []
        # 保存的路径
        self.save_dir = None
        # 转换用到的 exe
        self.gdal_translate_exe_path = None

    @staticmethod
    def get_file_time(file_path):
        """获取文件的时间，世界时转为北京时"""
        file_base_name = os.path.basename(file_path)  # 文件名
        if 'ASI' in file_base_name:
            UTC_str = file_base_name[-13:-3]
            UTC_time = datetime.datetime.strptime(UTC_str, '%Y%m%d%H')
            CHN_time = UTC_time + datetime.timedelta(hours=-8)
            CHN_str = datetime.datetime.strftime(CHN_time, '%Y%m%d%H')
            return CHN_str
        elif 'CHN' in file_base_name:
            return file_base_name[-13:-3]
        else:
            return

    def get_save_path(self, file_path):
        """根据文件名，得到输出路径"""
        CHN_time_str = self.get_file_time(file_path)  # 获取北京时间

        # 取到文件产品时间之前，
        file_basename = os.path.basename(file_path)
        # 输出文件夹
        out_reladir = os.path.join(CHN_time_str[:6], CHN_time_str[:8])
        out_reladir += r'\NRT' if '_NRT_' in file_basename else r'\RT'
        out_reladir += r'\HOR' if '_HOR-' in file_basename else r'\DAY'
        out_path = os.path.join(self.save_dir, out_reladir)
        # 新建文件夹
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        #
        geotif_name = file_basename[:-13] + CHN_time_str + '.tif'  #  把 basename 的时间统一改为北京时间
        out_geotif = os.path.join(out_path, geotif_name)
        return out_geotif

    def nc_to_tiff(self, nc_file, out_geotif):
        """调用cmd ， nc 文件转为 tiff 文件"""
        cmd_str = self.gdal_translate_exe_path + ' -a_srs WGS84 -of GTiff -sds ' + nc_file + ' ' + out_geotif
        os.system(cmd_str)

    # @time_this
    def do_process(self):
        """主流程"""
        for each_file in self.files_to_transform:
            if not each_file.endswith('.nc'):  # 过滤非 nc 文件
                continue

            # 得到返回值
            save_path = self.get_save_path(each_file)
            # 转换
            self.nc_to_tiff(each_file, save_path)


class Xml_Util(object):

    # ------------------------------ 写 xml ----------------------------------------------------------------------------
    @staticmethod
    def get_document(head_time_str):
        """返回 document, 用于写 xml 文件"""
        document = Document()
        document.appendChild(document.createComment(head_time_str))
        return document

    @staticmethod
    def add_sub_node(document, curNode, nodeKey, nodeValue, nodeAtt=None):
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
            print("* error in add node")
            return None

    @staticmethod
    def save_xml(document, xml_path):
        """将 xml 保存为本地文件"""
        with open(xml_path, 'w') as f:
            f.write(document.toprettyxml(indent='\t', encoding='utf-8'))
    # ------------------------------ 读 xml ----------------------------------------------------------------------------
    @staticmethod
    def get_root_node(xml_path):
        """返回用于读 xml 的 collection"""
        DOMTree = xml.dom.minidom.parse(xml_path)
        root_node = DOMTree.documentElement
        return root_node

    @staticmethod
    def get_info_from_node(eachNode, assign_attr=None):
        """现在只支持 Element"""
        # -----------------------------------------------------------------
        if eachNode.nodeType != 1:
            return
        # -----------------------------------------------------------------
        element_info = {}
        # -----------------------------------------------------------------
        # 获得所有的属性
        attr_dict = {}
        if assign_attr:
            assign_attr = set(assign_attr)
            for each_attr in assign_attr:
                attr_dict[each_attr] = eachNode.getAttribute(each_attr)
        else:
            for each_attr in eachNode.attributes.values():
                attr_dict[each_attr.name] = each_attr.value
        element_info['attr'] = attr_dict
        # -----------------------------------------------------------------
        # 得到值,有子节点就没有值，这一点要注意
        node_value = None
        if len(eachNode.childNodes) == 1:
            if eachNode.childNodes[0].nodeType == 3:
                node_value = eachNode.childNodes[0].nodeValue
        element_info['value'] = node_value
        # -----------------------------------------------------------------
        # 得到子节点
        # child_nodes = eachNode.childNodes
        # -----------------------------------------------------------------
        return element_info
    # ------------------------------ 常用 ------------------------------------------------------------------------------
    @staticmethod
    def xml_parser(xml_path, need_tages, attr="identify"):
        """
        读取xml文件（一个级别），保存为字典
        :param xml_path: xml 文件路径
        :param need_tages: 需要的标签名
        :param attr: 需要的属性名
        :return: {'attr':value}
        """
        def get_key_value(oneNode, attr_temp):
            """读取标签"""
            key = oneNode.getAttribute(attr_temp)
            value = oneNode.childNodes[0].data
            return key, value

        xml_info = {}
        DOMTree = xml.dom.minidom.parse(xml_path)
        collection = DOMTree.documentElement
        # 遍历节点
        for each_tag in need_tages:
            for eachNode in collection.getElementsByTagName(each_tag):
                (info_key, info_value) = get_key_value(eachNode, attr)
                xml_info[info_key] = info_value

        return xml_info



if __name__ == '__main__':

    a = NcFileToTiff()

    # ------------------ 读取 issue 等，解析为需要的文件夹 ------------------------------------

    # xml_path = r'Y:\inputXML\nc\inputXml\201908011259\201908011259.xml'
    xml_path = r'D:\BaiduNetdiskDownload\Algo\201908011239.xml'
    # xml_path = sys.argv[1]

    xml_dict = Xml_Util.xml_parser(xml_path, ['input'])

    save_path_xml = xml_dict['outXMLPath']

    a.save_dir = xml_dict['outFolder']

    a.gdal_translate_exe_path = xml_dict['gdal_translate']
    # a.gdal_translate_exe_path = r'C:\ProgramData\Anaconda2\envs\QingHai\Library\bin\gdal_translate.exe'

    a.files_to_transform = xml_dict['inputFile'].split(',')

    a.do_process()

    try:

        a.do_process()

        status = 'success'

    except:

        status = 'error'


    # ---------------------------------------------------------------------------------
    # 写 output xml 文件


    if status == 'error':
        status, info = '0', 'error'
    else:
        status, info = '1', 'success'

    # 初始化
    document = Xml_Util.get_document('ProcessTime:' + str(datetime.datetime.now()))
    # 添加根节点
    XML = Xml_Util.add_sub_node(document, document, 'XML', '', None)
    # info 信息
    log = Xml_Util.add_sub_node(document, XML, 'log', '', None)
    Xml_Util.add_sub_node(document, log, 'status', status, None)
    Xml_Util.add_sub_node(document, log, 'info', info, None)

    Xml_Util.save_xml(document, save_path_xml)

    print('ok')




