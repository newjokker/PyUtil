# -*- coding: utf-8  -*-
# -*- author: jokker -*-

# 筛选需要的地区
need_area = data_frame_choose_date['csta'] == area
data_frame_choose_date_area = data_frame_choose_date[need_area]

# 筛选需要的列
list(data_frame_choose_date_area[['h11', 'h12', 'h13']].values[0])