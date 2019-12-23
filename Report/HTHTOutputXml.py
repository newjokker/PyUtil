# -*- coding: utf-8  -*-
# -*- author: jokker -*-


"""
用于生成 out_put_xml 的示例
"""

import os
from Report.XmlUtil import XmlUtil


class HTHTOutputXml(object):
    """生成 output_xml """

    def __init__(self, xml_save_path):
        self.status = '0'
        self.xml_save_path = xml_save_path
        self.out_files = {}
        self.table_info = []
        self.user_defined = {}
        self.xml_info = {'out_files': self.out_files,
                         'table_info': self.table_info,
                         'user_defined': self.user_defined}

    def create_output_xml(self):
        """create out put xml"""
        # DS: {'status':0, 'save_path':save_path, 'out_files':{'region_id':[]}},
        # 'table_info':[{'table_name': 'table_value':[[], [], []]}, {}]}, 'user_defind':{'tag':{'identify', 'value'}}

        xml_info = self.xml_info

        status = self.status
        # save_path = xml_info['save_path']
        out_file_info = xml_info['out_files']
        table_info = xml_info['table_info']
        user_defined_info = xml_info['user_defined']
        #
        document = XmlUtil.get_document()
        xml_node = XmlUtil.add_sub_node(document, document, 'XML', '', None)

        # write run status
        log = XmlUtil.add_sub_node(document, xml_node, 'log', '', None)
        info = 'success' if status is not '0' else 'failed'
        XmlUtil.add_sub_node(document, log, 'status', status, None)
        XmlUtil.add_sub_node(document, log, 'info', info, None)

        # write file in xml
        if out_file_info:
            out_files = XmlUtil.add_sub_node(document, xml_node, 'outFiles', '', None)
            for each_file in out_file_info:
                region_node = XmlUtil.add_sub_node(document, out_files, 'region', '', {'identify': each_file})
                for each_file_path in out_file_info[each_file]:
                    XmlUtil.add_sub_node(document, region_node, 'file', each_file_path, None)

        if table_info:
            # write table in xml
            tables = XmlUtil.add_sub_node(document, xml_node, 'tables', '', None)
            for each_table in table_info:
                table_name = each_table['table_name']
                table_value = each_table['table_value']
                each_table = XmlUtil.add_sub_node(document, tables, 'table', '', {'identify': table_name})
                for each_table_line in table_value:
                    table_line_str = ','.join(map(str, each_table_line))
                    XmlUtil.add_sub_node(document, each_table, 'values', table_line_str, None)

        if user_defined_info:
            # write user_defined_info
            user_defined = XmlUtil.add_sub_node(document, xml_node, 'user_defined', '', None)
            for each_tag_name in user_defined_info:
                each_tag_info = user_defined_info[each_tag_name]
                XmlUtil.add_sub_node(document, user_defined, each_tag_name, str(each_tag_info['value']),
                                     {'identify': each_tag_info['identify']})

        # save file
        XmlUtil.save_xml(document, self.xml_save_path)

        if os.path.exists(self.xml_save_path):
            print('save out_put_xml success')
        else:
            print('save out_put_xml failed -->  {0}'.format(self.xml_save_path))

    def add_file(self, region_id, file_list):
        """增加一个文件"""
        if region_id in self.out_files:
            self.out_files[region_id].extend(file_list)
        else:
            self.out_files[region_id] = file_list

    def add_table(self, table_name, table_value):
        """增加一个表格"""
        self.table_info.append({'table_name': table_name, 'table_value': table_value})

    def add_user_defined(self, tag_name, identify, value):
        """增加一个自定义结构"""
        self.user_defined[tag_name] = {'identify': identify, 'value': value}

    def update_status(self, status):
        """更新执行状态"""
        self.status = status

    def do_process(self):
        """主流程"""
        # todo 出 xml 之前的值检查
        self.create_output_xml()


if __name__ == '__main__':

    a = HTHTOutputXml(r'C:\Users\Administrator\Desktop\for6.xml')
    a.add_file('20100', list(os.listdir(r'C:\Users\Administrator\Desktop\fire_report_modis_npp\out')))
    a.add_table('table_name_test', [[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    a.add_user_defined('test_tag_name', 'identify', 'hehe')
    a.update_status('1')
    a.do_process()
