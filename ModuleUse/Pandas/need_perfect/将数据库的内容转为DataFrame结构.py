# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import pandas as pd

data_info = ((1,2,3), (4,5,6))  # 数据库中拿出来的 data_info 是

df = pd.DataFrame(list(map(list, data_info)), columns=[u'csta', u'h11', u'h12', u'h13', u'fbday'], dtype='object')  # 转为 DataFrame

df['fbday'] = pd.to_datetime(df['fbday'], format="%Y-%m-%d")  # 日期转为时间格式


