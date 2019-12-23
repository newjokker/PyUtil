# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
使用机器学习的方法，预测各个电影的评分
"""
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
import time
import requests
# from ReadData.RandomUtil import RandomUtil
# from Z_for_CSDN.predicte_film_grade.FunctionFilmGrade.ParseFilmInfo import DYTT
# from .FunctionFilmGrade.ParseFilmInfo import DYTT


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


if __name__ == "__main__":

    url = r'https://www.dy2018.com/i/99614.html'
    save_path = r'D:\Code\Util_Util\Z_for_CSDN\predicte_film_grade\aux_data\all_film_url.html'

    while True:
        a = DYTT()
        a.get_all_url_from_local_file(r'D:\Code\Util_Util\Z_for_CSDN\predicte_film_grade\aux_data\all_film_url.txt')

        index = 1

        for each_url in a.file_url:
            print(each_url)
            print(each_url[25:])
            save_path = os.path.join(r'D:\Code\Util_Util\Z_for_CSDN\predicte_film_grade\aux_data\htmls', each_url[25:])
            try:
                if not os.path.exists(save_path):
                    index += 1
                    a.get_url_info_and_save_to_local(each_url, save_path)
                    time.sleep(1)
            except:
                index += 1
                time.sleep(1)
                print('error')

            if index % 20 == 0:
                index += 1
                time.sleep(60)











