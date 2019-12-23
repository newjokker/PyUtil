# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
分析电影信息
"""

import pandas as pd

film_info = pd.read_csv(r'E:\Algorithm\Scraping\scraping_with_python\DYTT\film_info_need.csv',index_col=0)
# 筛选出需要的列
film_info = film_info[['豆瓣','IMDB','类别','产地','年代']]
# 去掉有有无效值的行
film_info = film_info.dropna()
# ------------------------------------------------------------------------------
all_film_grade_info = []  # 投票评分信息
for each_line in film_info[['豆瓣','IMDB','类别','产地','年代']].values:
    #
    file_info_temp = {}
    # 豆瓣数据
    d_grade,_,d_num = each_line[0].split(',')
    file_info_temp['豆瓣评分'] = d_grade
    file_info_temp['豆瓣投票人数'] = d_num
    # IMDB数据
    i_grade,_,i_num = each_line[1].split(',')
    file_info_temp['IMDB评分'] = i_grade
    file_info_temp['IMDB投票人数'] = i_num
    # 其他
    file_info_temp['类别'] = '-'.join(map(lambda x:x.strip(), each_line[2].split('/')))
    file_info_temp['产地'] = '-'.join(map(lambda x:x.strip(), each_line[3].split('/')))
    file_info_temp['年代'] = int(each_line[4].split()[0])
    all_film_grade_info.append(file_info_temp)
# ------------------------------------------------------------------------------
film_info = pd.DataFrame(all_film_grade_info, columns=['豆瓣评分','豆瓣投票人数','IMDB评分','IMDB投票人数','类别','产地','年代'])
# ------------------------------------------------------------------------------
print(film_info)

film_info.to_csv(r'.\save_csv\clean_film_info.csv')

