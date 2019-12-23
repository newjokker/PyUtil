# -*- coding: utf-8  -*-
# -*- author: jokker -*-

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



if __name__ == "__main__":

    a = {'name':'jokker',
         'age': 45,
         'pice': 523,
         }

    JsonUtil.save_data_to_json_file(a, 'b.json')

    print(JsonUtil.load_data_from_json_file('b.json'))




