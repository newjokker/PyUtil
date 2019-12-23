# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import os
import pandas as pd
import re


# 将爬取的信息进行规范化

def parse_film_info(one_info):
    """解析电影信息"""

    one_info = one_info.replace(r'\\u3000', '')
    one_info = one_info.replace(r'\\xa06', '')
    one_info = one_info.replace(r'\\xa08', '')

    if one_info[:2] in {'译名', '片名', '年代', '产地', '类别'}:
        key = one_info[:2]
        one_info = one_info.replace(r'{0}'.format(key), '')
        value = one_info.strip()
        # value = re.sub(['(\u3000)\n(\xa06)(\xa0){0}'.format(str(key))], one_info, '')
    elif one_info[:2] in {'IM', '豆瓣'}:
        if one_info[:2] == 'IM':
            key = 'IMDB'
        else:
            key = '豆瓣'
        need_str_imdb = re.compile('.*(\d\.\d)/(.*)from(.*)users').findall(one_info)
        # 不能匹配
        if need_str_imdb:
            need_str_imdb = need_str_imdb[0]
        else:
            return {}
        # 需要的字符串
        need_str_imdb = map(lambda x: x.replace(',', '').strip(), need_str_imdb)
        need_str_imdb = ','.join(need_str_imdb)
        value = need_str_imdb
    else:
        return {}

    return {key: value}


file_dir = r'E:\Algorithm\Scraping\scraping_with_python\DYTT\result'

all_film_info = []

for each_file in os.listdir(file_dir):
    abs_path = os.path.join(file_dir, each_file)
    film_info_temp = {}
    with open(abs_path, 'r', encoding='utf-8') as txt_file:
        url_path = txt_file.readline().strip()
        film_info_temp['url'] = url_path
        # print(url_path)
        for each_line in txt_file:
            if each_line[:2] in {'译名', '片名', '年代', '产地', '类别', '豆瓣', 'IM'}:
                # print(each_line.strip())
                # film_info_temp[each_line[:2]] = each_line.strip()
                piece_of_file_info = parse_film_info(each_line)
                film_info_temp.update(piece_of_file_info)

    all_film_info.append(film_info_temp)
    # print(film_info_temp)

print('ok')

df = pd.DataFrame(all_film_info)

print(df)

df.to_csv(r'film_info_need.csv')

print('-' * 100)
