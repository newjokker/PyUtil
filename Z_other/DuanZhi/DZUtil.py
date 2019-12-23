# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from ReadData.JsonUtil import JsonUtil
from ReadData.OCRUtil import OCRUtil
from Report.MySqlUtil import MySqlUtil
# import jieba
# import jieba.analyse
#

class DZ(object):

    def __init__(self, save_path=None):

        self.dz_sql = None
        self.connect_to_mysql()  # 连接数据库

        # self.save_path = save_path  # 段子的保存路径
        # if save_path is not None:
        #     self.load_dz_from_json(save_path)

    def add_dz_to_db(self, content, tags=None, key_words=None):
        """往数据库中添加段子"""
        if key_words is None:
            key_words = DZ.__get_key_word_from_dz(content)  # 结巴分词获取关键词

        self.dz_data.append({'content': content, 'tags': tags, 'key_words': key_words})

    def connect_to_mysql(self):
        """连接数据库"""
        self.dz_sql = MySqlUtil()
        host, port, user, passwd, db_name = 'localhost', 3306, 'root', '747225581', "jokker"
        self.dz_sql.conoect_mysql(host, port, user, passwd, db_name)

    def close_connect(self):
        """关闭数据库"""
        self.dz_sql = None

    def get_dz_by_key_word(self, key_words):
        """输入关键词，返回对应的前 n 个段子"""
        # for each_dz in self.dz_data:
        #     if set(each_dz['key_words']).intersection(key_words):
        #         self.print_dz(each_dz)
        #         print('-'*100)

    def get_dz_by_content(self, content_keys):
        """根据内容获取段子"""

        # FIXME 关键词在开头或者结尾就不行了，必须要在中间，看看有没有办法进行改进

        if isinstance(content_keys, str):
            content_keys = [content_keys]

        re_dz = []
        for each_content in content_keys:
            re_dz.extend(self.dz_sql.select_info_from_database(['content'], 'duanzi', ['content like "%{0}%"'.format(each_content)]))
        return re_dz

    @staticmethod
    def get_dz_from_pic(pic_path, lauguage='chi_sim', replace_n=False):
        """从图片中识别段子"""
        #FIXME 有一个参数就是输入里面大概有多少字，这样就能很好的对图片进行重采样，这样能提高速度
        content = OCRUtil.get_words_from_image(pic_path, lauguage)  # 将图片转为文字
        # 对得到的文字进行简单的处理
        content = content.replace('\n\n', '')   # 去掉换行符
        content = content.replace(' ', '')      # 去掉空格
        if replace_n:
            return content.replace('\n', '')
        return content

    @staticmethod
    def __get_key_word_from_dz(content):
        """给段子使用结巴分词得到关键词"""
        # FIXME 用全模式，拿到20个关键词
        # key_words = jieba.analyse.extract_tags(content, topK=20, withWeight=False, allowPOS=())
        # return key_words

    def load_dz_from_json(self, file_path):
        """从 json 结构读取段子信息"""
        self.dz_data = JsonUtil.load_data_from_json_file(file_path)

    def save_dz_to_json(self, save_path):
        """将段子保存为需要的格式"""
        JsonUtil.save_data_to_json_file(self.dz_data, save_path)

    def re_fresh_dz(self):
        """对段子进行刷新"""
        new_dz = []
        for index, each_dz in enumerate(self.dz_data):
            each_content = each_dz['content']
            each_tags = each_dz['tags']
            each_key_words = each_dz['key_words']

            # 段子内容小于15个字符，自动删除
            if len(each_content) < 15:
                continue

            # 去掉段子中的 \n 字符
            each_content = each_content.strip('\n ')

            # 无标签，自动生成标签
            if each_key_words is None:
                each_key_words = DZ.__get_key_word_from_dz(each_content)

            new_dz.append({'content': each_content, 'tags': each_tags, 'key_words': each_key_words})
            self.dz_data = new_dz
    # ------------------------------------------------------------------------------------------------------------------
    def get_same_dz(self):
        """找到重复度很高的段子"""

    def get_near_dz(self):
        """找到重复度很高的段子，和相似度有一些区别的"""
    # ------------------------------------------------------------------------------------------------------------------
    def save_file(self):
        """执行被关闭时候的操作"""
        self.save_dz_to_json(self.save_path)

    def save_copy_file_to(self, save_path):
        """副本保存在另外一个地方"""
        self.save_dz_to_json(save_path)

    @staticmethod
    def print_dz(dz_info):
        """打印段子"""
        print('content : {0}'.format(dz_info['content']))
        print('tags : {0}'.format(dz_info['tags']))
        print('key_words : {0}'.format(dz_info['key_words']))

    def __del__(self):
        """析构函数, 用于被删除的时候保存文件并不可行"""
        self.close_connect()
        # JsonUtil.save_data_to_json_file(self.dz_data, self.save_path)


if __name__ == '__main__':

    a = DZ(r'E:\Algorithm\Util_Util\Z_other\DuanZhi\AuxData\dz.json')

    # a.re_fresh_dz()
    #
    # a.save_dz_to_json(r'E:\Algorithm\Util_Util\Z_other\DuanZhi\AuxData\dz.json')

    a.save_path = r'E:\Algorithm\Util_Util\Z_other\DuanZhi\AuxData\jokker.json'

    a.save_file()

    # key_words = {'禅师', '大师'}
    key_words = {'妹子'}
    a.get_dz_by_key_word(key_words)

    # a.get_dz_by_content(key_words)

    print('ok')
