# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import re
import json

class JsonUtil(object):

    @staticmethod
    def save_data_to_json_file(data, json_file_path):
        """将数据保存为 json 文件"""
        try:
            with open(json_file_path, 'w') as json_file:
                json.dump(data, json_file)
            return True
        except:
            return False

    @staticmethod
    def save_data_to_json_str(data):
        """将数据保存为 json 字符串格式"""
        return json.dumps(data)

    @staticmethod
    def load_data_from_json_file(json_file_path):
        """将数据冲json文件中读取出来"""
        try:
            with open(json_file_path, 'r') as json_file:
                return json.load(json_file)
        except:
            pass

    @staticmethod
    def load_data_from_json_str(json_str):
        """从 str 数据格式读取数据"""
        return json.loads(json_str)

class StrTypeChecking(object):

    @staticmethod
    def is_str(check_data):
        return isinstance(check_data, str) or isinstance(check_data, unicode)

    @staticmethod
    def is_in_length_range(check_str, min_num=None, max_num=None):
        """是否符合指定的长度"""
        # ---------------------------------------------
        if min_num:
            if len(check_str) < min_num:
                return False
        # ---------------------------------------------
        if max_num:
            if len(check_str) > max_num:
                return False
        # ---------------------------------------------
        return True

    @staticmethod
    def is_match_compile(check_str, compile_str):
        """是否符合正则表达式"""
        if re.compile(compile_str).match(check_str):
            return True
        else:
            return False

    @staticmethod
    def is_str_float(check_str, decimal_number=None, ignore_0_head=False):
        """是否为浮点型，检查保留的小数位数（3 代表，最多三维小数）,"""
        # ---------------------------------------------
        if not isinstance(check_str, str):
            return False
        # ---------------------------------------------
        if check_str.count('.') != 1:
            """浮点型有且仅有一个点"""
            return False
        # ---------------------------------------------
        if not check_str.replace('.', '').isdigit():
            """去除一个点之后其余的都是数字，就是浮点型"""
            return False
        # ---------------------------------------------
        if decimal_number:
            if len(check_str) - check_str.find('.') > decimal_number + 1:
                """用字符串的长度与点所在位置的关系确定小数位数是否符合"""
                return False
        # ---------------------------------------------
        if not ignore_0_head and check_str.startswith('0') and check_str != '.':
            if check_str[1] != '.':
                """以0开头，第二位必定要是点"""
                return False
        # ---------------------------------------------
        return True

    @staticmethod
    def is_str_int(check_str, ignore_0_head=False):
        # ---------------------------------------------
        if not isinstance(check_str, str):
            return False
        # ---------------------------------------------
        if not check_str.isdigit():
            """int形的数据，全部是数字组成的"""
            return False
        # ---------------------------------------------
        if ignore_0_head and check_str.startswith('0'):
            return False
        # ---------------------------------------------
        return True

    @staticmethod
    def is_str_number(check_str, ignore_0_head=False):
        """是字符串格式的数字"""
        if StrTypeChecking.is_str_float(check_str, ignore_0_head=ignore_0_head) \
                or StrTypeChecking.is_str_int(check_str, ignore_0_head=ignore_0_head):
            return True
        else:
            return False

    @staticmethod
    def is_in_range(check_str, ignore_0_head=False, min_value=None, max_value=None):
        """数值大小是否在指定的范围内"""
        # -----------------------------------------------------------
        # 未指定范围，返回 True
        if min_value is None and max_value is None:
            return True
        # -----------------------------------------------------------
        if StrTypeChecking.is_str_number(check_str, ignore_0_head=ignore_0_head):
            # -------------------------------------------------------
            if ignore_0_head:
                num_value = float(check_str.lstrip('0'))
            else:
                num_value = float(check_str)
            # -------------------------------------------------------
            if min_value is not None and num_value < min_value:
                return False
            # -------------------------------------------------------
            if max_value is not None and num_value > max_value:
                return False
            # -------------------------------------------------------
        return True

class TypeChecking(object):
    """类型检查"""

    def load_model(self):
        """载入模板"""
        pass

    def parse_model(self):
        """解析模板"""
        pass

    def check_structure(self):
        """结构检查"""
        pass

    @staticmethod
    def check_item(check_str, compile_str):
        """条目检查"""
        pass

class TypeCheckingTxt(TypeChecking):
    """TXT 类型检查"""

    @staticmethod
    def _in_and_not_none():
        """存在并且不是none"""

    @staticmethod
    def is_element_match_type_inf(element_str, type_info):
        """元素是否和类型信息匹配"""

        if 'ignore_0_head' not in type_info:
            ignore_0_head = False
        else:
            ignore_0_head = type_info['ignore_0_head']

        # 遍历检查条件字典
        # -----------------------------------------------
        type_str = type_info.setdefault('type', None)
        if type_str:
            # 检查类型
            if type_str == 'str_int':
                if not StrTypeChecking.is_str_int(element_str, ignore_0_head=ignore_0_head):
                    print('check str_int error, element_str : {0}'.format(element_str))
                    return False
            elif type_str == 'str_number':
                if not StrTypeChecking.is_str_number(element_str, ignore_0_head=ignore_0_head):
                    print('check str_number error, element_str : {0}'.format(element_str))
                    return False
            elif type_str == 'str_float':
                if not StrTypeChecking.is_str_float(element_str, ignore_0_head=ignore_0_head):
                    print('check str_float error, element_str : {0}'.format(element_str))
                    return False
        # -----------------------------------------------
        compile_str = type_info.setdefault('compile_str', None)
        if compile_str:
            # 检查类型
            if not StrTypeChecking.is_match_compile(element_str, compile_str):
                print('check compile_str error, compile_str : {0}, element_str : {1}'.format(compile_str, element_str))
                return False
        # -----------------------------------------------
        min_value = type_info.setdefault('min_value', None)
        max_value = type_info.setdefault('max_value', None)
        if min_value is not None and max_value is not None:
            if not StrTypeChecking.is_in_range(element_str, min_value=min_value, max_value=max_value):
                print(
                    'check in_range error, range : min : max = {0}:{1}, element_str : {2}'.format(min_value, max_value,
                                                                                                  element_str))
                return False
        # -----------------------------------------------
        return True

    @staticmethod
    def check_item(check_str, type_info):
        """检查每一行数据"""
        elements = check_str.split(',')
        # -------------------------------------------------------
        if len(elements) > len(type_info):
            print('* less type_info then elements')
            return False
        # -------------------------------------------------------
        for index, each_element in enumerate(elements):
            # 检查每一个元素
            each_element = each_element.strip('\n')
            # -------------------------------------------------------
            if not TypeCheckingTxt.is_element_match_type_inf(each_element, type_info[index]):
                return False
        return True

    @staticmethod
    def main(txt_path, type_info):
        """主函数"""
        # type_info = [
        #     {'type': 'str_int', 'min_value': 1, 'max_value': 100, 'ignore_0_head': None, 'compile_str': '^\d{2,8}$'},
        #     {'type': 'str_float', 'min_value': None, 'max_value': None, 'ignore_0_head': None, 'compile_str': None},
        #     {'type': 'str_int', 'min_value': None, 'max_value': None, 'ignore_0_head': None, 'compile_str': None},
        #     {'type': 'str_int', 'min_value': None, 'max_value': None, 'ignore_0_head': None, 'compile_str': None},
        #     {'type': 'str_int', 'min_value': None, 'max_value': None, 'ignore_0_head': None, 'compile_str': None},
        #     {'type': 'str_int', 'min_value': None, 'max_value': None, 'ignore_0_head': None, 'compile_str': None},
        #     {'type': 'str_int', 'min_value': None, 'max_value': None, 'ignore_0_head': None, 'compile_str': None},
        #     {'type': 'str_int', 'min_value': None, 'max_value': None, 'ignore_0_head': None, 'compile_str': None},
        #     {'type': 'str_int', 'min_value': None, 'max_value': None, 'ignore_0_head': None, 'compile_str': None},
        # ]

        # FIXME 需要增加表头过滤，或者表头检查的功能，表头检查直接跟标准表头进行对比即可
        # --------------------------------------------------------------------------------------------------------------
        with open(txt_path, 'r') as txt_file:
            for each in txt_file:
                print(each.strip('\n'))
                print(TypeCheckingTxt.check_item(each.strip('\n'), type_info))
                print('-' * 100)

class TypeCheckingExcel(TypeChecking):
    """考虑是否检查合并栅格之类的"""

class TypeCheckingXml(TypeChecking):
    """结构比较重要，使用爬虫的相关技术去实现数据的查找，就是用寻找的思路去检查拿出来的数据"""

class TypeCheckingFileName(TypeChecking):
    """文件名检查，根据我们之前出的文件名规范对文件名进行检查，里面只写通用的函数，不需要很细致"""


if __name__ ==  '__main__':

    type_info = JsonUtil.load_data_from_json_file(r'D:\Code\Util_Util\TypeChecking\Model\txt_check_model_test.json')

    txt_path = r'D:\Code\Util_Util\TypeChecking\AuxData\test.txt'

    TypeCheckingTxt.main(txt_path, type_info)



