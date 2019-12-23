# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import copy
from .XmlUtil import XmlUtil


class AreaInfo(object):
    """to storage node attribute and class infomation"""

    def __init__(self, node_id, father_id=None, child_ids=None, attr_dict=None):
        # node attribute
        if attr_dict is None:
            self.__attr_dict = {}
        elif isinstance(attr_dict, dict):
            self.__attr_dict = attr_dict
        #
        if father_id is None:
            self.__father_ID = None
        else:
            if isinstance(father_id, float) or isinstance(father_id, int) or isinstance(father_id, str):
                self.__father_ID = father_id
            else:
                raise TypeError('father_ID can only be int float or str')
        #
        if child_ids is None:
            self.__child_ID = set()
        else:
            if isinstance(child_ids, list) or isinstance(child_ids, set) or isinstance(child_ids, tuple):
                self.__child_ID = set()
                for each_child_id in child_ids:
                    self.add_child_node(each_child_id)
            else:
                raise ValueError('child_IDs is illegal')
        # node_id Used to uniquely identify a node
        if isinstance(node_id, float) or isinstance(node_id, int) or isinstance(node_id, str):
            self.__ID = node_id
        else:
            raise TypeError('ID can only be int float or str')
        # root_node --> 0, middle node --> 1, leaf node --> 2
        self.__element_type = None
        # the node class
        self.__element_class = None
        #
        self.__reflash_element()

    def __reflash_element(self):
        """update node type and class"""
        # update node type
        if self.__father_ID is None:
            self.__element_type = 0  # root node
        elif self.__child_ID is None or len(self.__child_ID) == 0:
            self.__element_type = 2  # leaf node
        else:
            self.__element_type = 1  # middle node
        # update node class ?
        # todo if the function is needed

    # ------------ get infomation ----------------------------------

    def get_attr_info(self, attr_key):
        """get node attribute by key"""
        if attr_key in self.__attr_dict:
            return self.__attr_dict[attr_key]
        else:
            return None

    def get_father_id(self):
        return self.__father_ID

    def get_child_id(self):
        """child_id is a set, return a copy"""
        return self.__child_ID.copy()

    def get_id(self):
        """get self node id"""
        return self.__ID

    def get_element_type(self):
        """get self type"""
        self.__reflash_element()
        return self.__element_type

    # ------------ node structure ----------------------------------

    def add_child_node(self, child_node_id):
        """add child node"""
        if child_node_id == self.__father_ID:
            raise ValueError(u'child ID equal to child ID')  # father id != child id
        else:
            self.__child_ID.add(child_node_id)

    def remove_assign_child_node(self, child_node_id):
        """remove assign child return True if success else False"""
        if child_node_id in self.__child_ID:
            self.__child_ID.remove(child_node_id)
            return True
        else:
            return False

    def remove_all_child_node(self):
        """delete all child"""
        self.__child_ID = set()

    def assign_father_node(self, father_node_id):
        """assign which node self belong"""
        if father_node_id in self.__child_ID:
            raise ValueError(u'child ID equal to child ID')  # father id != child id
        else:
            self.__father_ID = father_node_id

    def remove_father_node(self):
        """delete father node"""
        self.__father_ID = None

    # ------------ attribute operate ------------------------------------

    def add_attr_info(self, key, value):
        """add or update attribute"""
        self.__attr_dict[key] = value

    def remove_attr_info(self, key):
        """delete assign self attribute"""
        if key in self.__attr_dict:
            self.__attr_dict.pop(key)

    def clear_attr_info(self):
        """delete all self attribute"""
        self.__attr_dict = {}


class AreaInfoOperation(object):
    """for operate AreaInfo"""

    def __init__(self, node_dict=None, node_class_dict=None):
        # a dict to storage node infomation
        if node_dict is None:
            self.node_dict = {}
        else:
            self.node_dict = node_dict  # key: node_id, value: AreaInfo

        # for avoid ring
        if node_class_dict is None:
            self.node_class_dict = {}
        else:
            # key: node_id, value: node class, root node class: 0, root-->child node class is 1 and so on
            self.node_class_dict = node_class_dict

    # ---------------------- node operate -------------------------------

    def add_node(self, node):
        """if node id not in self , set it a root node"""

        # type checking
        if not isinstance(node, AreaInfo):
            raise TypeError('need a AreaInfo')

        node_id = node.get_id()
        # ensure uniqueness --> node id
        if node_id in self.node_dict:
            raise ValueError('ID {0} has been in node_dict'.format(node_id))

        # add to node_dict
        self.node_dict[node_id] = node

    def link_two_node(self, father_id, child_id):
        """link two node"""
        if not (father_id in self.node_dict and child_id in self.node_dict):
            raise ValueError('father id or child id not in node_dict')

        father_node = self.node_dict[father_id]
        child_node = self.node_dict[child_id]
        #
        father_node.add_child_node(child_id)
        child_node.assign_father_node(father_id)

    def break_link_between_two_node(self, father_id, child_id):
        """break link between two_node"""

        # TODO just get two node, juge their relationship

        if not (father_id in self.node_dict and child_id in self.node_dict):
            raise ValueError('father id or child id not in node_dict')

        father_node = self.node_dict[father_id]
        child_node = self.node_dict[child_id]
        #
        father_node.remove_assign_child_node(child_id)
        child_node.remove_father_node()

    def insert_node_between_two_node(self, father_id, child_id, new_node):
        """insert node between two node"""

        if not isinstance(new_node, AreaInfo):
            raise TypeError('new_node should be AreaInfo')

        node_id = new_node.get_id()

        if not (father_id in self.node_dict and child_id in self.node_dict):
            raise ValueError('father id or child id not in node_dict')

        if node_id not in self.node_dict:  # new one if not exist
            self.add_node(new_node)

        self.break_link_between_two_node(father_id, child_id)
        self.link_two_node(father_id, node_id)
        self.link_two_node(node_id, child_id)

    def delete_node_between_two_node(self, father_id, child_id):
        """delete node between two node"""

        if not (father_id in self.node_dict and child_id in self.node_dict):
            raise ValueError('father id or child id or new_node_id not in node_dict')

        father_node = self.node_dict[father_id]
        child_node = self.node_dict[child_id]

        if child_node.get_father_id() not in father_node.get_child_id():
            raise ValueError('their no node in father_node and child_node')

        middle_node = self.node_dict[child_node.get_father_id()]
        middle_id = middle_node.get_id()

        self.break_link_between_two_node(father_id, middle_id)
        self.break_link_between_two_node(middle_id, child_id)
        self.link_two_node(father_id, child_id)

    # ---------------------- get node infomation -----------------------

    def get_node_copy(self, node_id):
        """get node copy"""
        if node_id in self.node_dict:
            return copy.deepcopy(self.node_dict[node_id])
        else:
            return None

    def get_child_node_id(self, node_id):
        """get child node id"""
        # node not exist
        if node_id not in self.node_dict:
            return None
        return self.node_dict[node_id].get_child_id()

    def get_father_node_id(self, node_id):
        """得到父节点的 node_id"""
        # if node exist
        if node_id not in self.node_dict:
            return None
        return self.node_dict[node_id].get_father_id()

    def get_brother_node_id(self, node_id):
        """get brother node id"""
        if node_id not in self.node_dict:
            return None

        # find father node
        now_node = self.node_dict[node_id]
        father_id = now_node.get_father_id()

        father_node = None
        if father_id:
            if father_id in self.node_dict:
                father_node = self.node_dict[father_id]
        #
        if not father_node:
            return None
        else:
            res_node = father_node.get_child_id()  # find father node's child node
            res_node.remove(node_id)
            return res_node

    def get_all_child_node_id(self, node_id, algo=None, scan_all=False):
        """get all child node id, algo ==> for filtrate node, 过滤父节点之后是否需要继续遍历子节点"""
        # 节点不存在
        if node_id not in self.node_dict:
            return None

        all_nodes_id = set()
        nodes = [self.node_dict[node_id]]

        while nodes:
            # check_nodes = copy.deepcopy(nodes)
            check_nodes = nodes.copy()
            nodes = []
            if algo is None:  # no filtrate
                for each_node in check_nodes:
                    for node_id_temp in each_node.get_child_id():
                        if node_id_temp in self.node_dict:
                            nodes.append(self.node_dict[node_id_temp])
                            all_nodes_id.add(node_id_temp)
            else:
                for each_node in check_nodes:
                    for node_id_temp in each_node.get_child_id():
                        if node_id_temp in self.node_dict:
                            node_temp = self.get_node_copy(node_id_temp)
                            #
                            if algo(node_temp):
                                nodes.append(self.node_dict[node_id_temp])
                                all_nodes_id.add(node_id_temp)
                            else:
                                if scan_all:
                                    nodes.append(self.node_dict[node_id_temp])
        return list(all_nodes_id)

    # ---------------------- need repair --------------------------------

    def get_relationship_betweent_two_node(self, node_a, node_b):
        """get relationship betweent two node"""
        # if a in all b's childs
        # if b in all a's childs
        # father-child, ancestor-child, no-relation

    def get_all_root_node(self):
        """get all root node"""

    def have_ring(self):
        """find if have a ring"""

    def refresh_node_class(self):
        """refresh node class"""
        # TODO self.have_ring()
        # TODO compute class


def parse_map_info(area_cfg_xml_path):
    """parse geographical xml"""

    def get_child_node_info(node_one):
        """get child node infomation"""
        father_info = XmlUtil.get_info_from_node(node_one)

        if father_info is None:
            return

        father_id = father_info['attr']['id']
        #
        for each_node in node_one.childNodes:
            each_child_info = XmlUtil.get_info_from_node(each_node)
            if each_child_info:
                child_id = each_child_info['attr']['id']
                area_info_0perator.add_node(
                    AreaInfo(child_id, father_id=father_id, attr_dict=each_child_info['attr']))  # add node
                area_info_0perator.link_two_node(father_id, child_id)  # define node relation
            get_child_node_info(each_node)  # do recursion
    # --------------------------------------------------------------------------------------
    area_info_0perator = AreaInfoOperation()
    root = XmlUtil.get_root_node(area_cfg_xml_path)  # root node
    root_info = XmlUtil.get_info_from_node(root)
    root_id = root_info['attr']['id']
    area_info_0perator.add_node(AreaInfo(root_id, attr_dict=root_info['attr']))  # add root node
    get_child_node_info(root)
    return area_info_0perator


if __name__ == '__main__':

    areaXmlPath = r'D:\Code\Util_Util\MapClassInfo\AreaCfg.xml'
    areaInfoOperator = parse_map_info(areaXmlPath)
    city = areaInfoOperator.get_child_node_id('QHS')

    countrys = []
    for each in city:
        countrys.extend(areaInfoOperator.get_child_node_id(each))

    print(len(city))
    print(city)
    print(len(countrys))
    print(countrys)
