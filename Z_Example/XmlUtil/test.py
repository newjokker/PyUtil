# -*- coding: utf-8  -*-
# -*- author: jokker -*-


from Report.XmlUtil import XmlUtil

product_info = {}
root = XmlUtil.get_root_node(r'C:\Users\Administrator\Desktop\VegdriCfg.xml')
for each_node in root.childNodes:
    if XmlUtil.get_info_from_node(each_node):
        node_name = each_node.nodeName

        node_info = XmlUtil.get_info_from_node(each_node)

        if node_info['attr']['identify'] == 'VEGDRI':

            for each_node_2 in each_node.childNodes:

                node_info_2 = XmlUtil.get_info_from_node(each_node_2)

                if node_info_2:
                    print('-'*100)

                    for each_node_3 in each_node_2.childNodes:

                        node_info_3 = XmlUtil.get_info_from_node(each_node_3)

                        if node_info_3:

                            print(node_info_3)
