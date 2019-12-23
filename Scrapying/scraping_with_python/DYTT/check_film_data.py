# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import pandas as pd


csv_path = r'/Users/jokkerryou/Documents/Code/Scrapying/scraping_with_python/DYTT/film_info_need.csv'

film_info = pd.read_csv(csv_path,index_col=0)

film_info = film_info.dropna()

film_info = film_info[['IM','豆瓣','类别']]
# film_info = film_info[['IM','豆瓣']]

film_info.to_csv(r'a.csv')


new_df = []

for each_line in film_info[['豆瓣','IM','类别']].values:
    new_df.append(each_line[0].split(' ')[:4:2] + each_line[1].split(' ')[:4:2] + [each_line[2]])

a = pd.DataFrame(new_df, columns=['豆瓣评分','人数','IMDB','人数','类型'])

print(a)

# print(film_info)
