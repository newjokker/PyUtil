# -*- coding: utf-8  -*-
# -*- author: jokker -*-



from bs4 import BeautifulSoup
from ReadData.PickleUtil import PickleUtil
from Report.StrUtil import StrUtil
from urllib.request import urlopen
import os
import time
import requests
import re


class ParseFilmInfo(object):
    """解析电影信息"""

    def __init__(self):
        self.config_dir = None
        self.film_types = set()

    def load_config_info(self):
        """加载配置信息"""
        # 读取电影类型信息
        film_types_path = os.path.join(self.config_dir, 'film_types.txt')
        #
        with open(film_types_path, 'r', encoding='utf-8') as txt_file:
            for each_line in txt_file:
                for each_type in each_line.strip().split(','):
                    if each_type.strip():
                        self.film_types.add(each_type.strip())

    @staticmethod
    def parse_p_info(p_info_str):
        """解析 p 标签的信息"""
        all_info = {}
        try:
            need_tag = {'译名', '片名', '年代', '产地', '类别', '语言', '字幕', '上映', '豆瓣', 'IM', '文件', '视频', '文件', '片长',
                        '导演', '主演', '简介', '获奖', }
            aa = ''.join(p_info_str).replace('　　', '')
            for each_tag in aa.split('◎'):
                tag_temp = each_tag[:2]
                if tag_temp in need_tag:
                    all_info[tag_temp] = each_tag
        except:
            print('parse error')

        return all_info

    def parse_film_info_001(self, html_path):
        """解析 html 中的电影信息"""
        with open(html_path, 'rb') as html_file:
            bs_obj = BeautifulSoup(html_file, "html.parser")
        zoom = bs_obj.find('div', {'id': 'Zoom'})
        # 挑选 p 标签
        p_infos = []
        for each in zoom.find_all('p'):
            if each:
                if not each.attrs:
                    p_infos.append(each.text)
        # 解析 p 标签
        film_info = self.parse_p_info(p_infos)
        return film_info
    # -------------------------- 各种类型的解析 --------------------------------
    def parse_age(self, film_info):
        """解析电影的年代"""
        if u'年代' in film_info:
            ym_str = film_info[u'年代']
            im_info = StrUtil.split(ym_str, ['\u3000', u'年代'])[-1].strip()[:4]
            return im_info
        else:
            return ''

    def parse_film_name(self, film_info):
        """解析电影名"""
        if u'片名' in film_info:
            ym_str = film_info[u'片名']
            # im_info = StrUtil.split(ym_str, ['\u3000', u'片名'])[-1].split('/')
            im_info = StrUtil.split(ym_str, ['\u3000', u'片名'])[-1].strip()
            return im_info
        else:
            return ''

    def parse_translation(self, film_info):
        """解析电影译名"""
        if u'译名' in film_info:
            ym_str = film_info[u'译名']
            # im_info = StrUtil.split(ym_str, ['\u3000', u'译名'])[-1].split('/')
            im_info = StrUtil.split(ym_str, ['\u3000', u'译名'])[-1].strip()
            return im_info
        else:
            return ''

    def parse_imdb(self, film_info):
        """解析 IMDB 信息"""
        if 'IM' in film_info:
            im_str = film_info['IM']
            im_info = im_str.split('\u3000')[-1]
            # 这个是完整的数据, 不完整的数据使用
            search_info = re.search(re.compile(r'(\d\.\d)\/10 from (.*) users'), im_info)
            if search_info:
                return search_info.groups()
            else:
                print(im_str)
                return '-1', '-1'
        else:
            return '-1', '-1'

    def parse_db(self, film_info):
        """解析豆瓣评分信息"""
        if '豆瓣' in film_info:
            db_str = film_info['豆瓣']
            im_info = db_str.split('\u3000')[-1]
            # 这个是完整的数据, 不完整的数据使用
            search_info = re.search(re.compile(r'(\d\.\d)\/10 from (.*) users'), im_info)
            if search_info:
                # print(str(search_info.groups()))
                return search_info.groups()
            else:
                print(db_str)
                return '-1', '-1'
        else:
            return '-1', '-1'

    def parse_film_type(self, film_info):
        """解析电影类型"""
        if '类别' in film_info:
            type_str = film_info['类别']
            type_info = StrUtil.split(type_str.strip(), ['\u3000', '\xa0', ' ', '/'])
            type_info = list(filter(lambda x: x in self.film_types, type_info))
            return '/'.join(type_info)
        else:
            return ''

    def parse_release_date(self, film_ifo):
        """解析上映时间"""
        # DS ==> [('2018', '10', '19', '中国大陆'), ('2018', '01', '20', '昂热电影节'), ('2018', '01', '26', '英国')]
        if '上映' in film_ifo:
            release_date_str = film_ifo['上映']
            date_info = re.findall(re.compile('(\d{4}).{1}(\d{1,2}).{1}(\d{2}).{,2}\((.{,10})\)'), release_date_str)
            return date_info
        else:
            return []
    # --------------------------------------------------------------------------
    def get_film_info_from_film_dict(self, film_info):
        """规范化获取的电影信息"""
        if film_info:
            # print('-'*100)
            # print('上映 : ', self.parse_release_date(film_info))
            # print('类型 : ', self.parse_film_type(film_info))
            # print('豆瓣 : ', self.parse_db(film_info))
            # print('IMDB : ', self.parse_imdb(film_info))
            # print('译名', self.parse_translation(film_info))
            # print('片名', self.parse_film_name(film_info))
            # print('年代', self.parse_age(film_info))

            film_type = self.parse_film_type(film_info)
            db_grade, db_num = self.parse_db(film_info)
            imdb_grade, imdb_num = self.parse_imdb(film_info)
            translation = self.parse_translation(film_info)
            film_name = self.parse_film_name(film_info)
            age = self.parse_age(film_info)

            return {'type': film_type,
                    'douban_grade': db_grade,
                    'douban_num': db_num,
                    'imdb_grade': imdb_grade,
                    'imdb_num': imdb_num,
                    'translation': translation,
                    'name': film_name,
                    'age': age}


class DYTT(object):

    def __init__(self):
        self.file_url = set()

        self.head = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.'
                              '0.3538.25 Safari/537.36 Core/1.70.3676.400 QQBrowser/10.4.3469.400',
                }

    def get_url_info_and_save_to_local(self, url, save_path):
        """获取 url 对应的信息，保存为本地文件"""
        html = urlopen(url).read()
        # html = requests.get(url, timeout=20, headers=self.head).text
        with open(save_path, 'wb') as html_file:
            html_file.write(html)


    def get_all_url_from_local_file(self, txt_path):
        """从本地读取 url 数据"""
        with open(txt_path, 'r') as txt_file:
            for each_line in txt_file:
                self.file_url.add(each_line.strip())

