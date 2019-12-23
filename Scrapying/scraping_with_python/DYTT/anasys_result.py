# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import pandas as pd
import numpy as np

film_info = pd.read_csv(r'E:\Algorithm\Scraping\scraping_with_python\DYTT\save_csv\clean_film_info.csv',index_col=0)
# ----------------------------------------------------------------------------------------------------------------------
grade_d = film_info['豆瓣评分']
grade_i = film_info['IMDB评分']
# ----------------------------------------------------------------------------------------------------------------------
c = grade_i - grade_d
d = abs(grade_i - grade_d)
c.name = 'i-d'
c = c.astype(np.float16)
d.name = 'abs(i-d)'
d = d.astype(np.float16)
# 合并数据集
film_info = pd.concat([film_info,c,d], axis=1)
# ----------------------------------------------------------------------------------------------------------------------
# 挑选出有代表性的投票
i_num = film_info['IMDB投票人数']
d_num = film_info['豆瓣投票人数']
a = film_info[np.logical_and(i_num > 300 , d_num > 300)]
# a = a[['豆瓣评分','IMDB评分','类别','产地','年代','i-d','abs(i-d)']]
a = a[['类别','产地','年代','i-d','abs(i-d)']]
# ----------------------------------------------------------------------------------------------------------------------
# 按照评分进行排序
a = a.sort_values('i-d')
print(a)

a.to_csv(r'E:\Algorithm\Scraping\scraping_with_python\DYTT\save_csv\result.csv')

# 在 DataFrame 增加一列


