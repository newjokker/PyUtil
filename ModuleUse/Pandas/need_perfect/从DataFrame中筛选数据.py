# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import pandas as pd
import numpy as np


data_dict = {'age':{'ldq':31, 'ldx':31, 'ldy':28}, 'loc':{'ldq':'nj', 'ldx':'wx', 'ldy':'wx'}, 'phone':{'ldq':'18761609908'}}
df = pd.DataFrame(data_dict)


# 提取其中的某几列, 返回的是 Series 或者 DataFrame，使用 [] 返回的就是 DataFrame 否则就是 Series
# a = df[['age','phone']]
a = df[['age']]

# 提取其中的某几行，
# b = df.values[0:]  # 拿出来的是 ndarry 结构
# b = df[0:1]  # 拿出来的是 Dataframe ，FIXME 必须要有 冒号，否则就变成了 列索引了
# b = df.iloc[:2]  # 使用 iloc 就确定拿的是行，而不是列
b = df.loc[['ldq']]  # 指定拿出的行名，不加 [] 返回的就是 Series 否则返回的就是 DataFrame

# 提取其中的某几行和某几列的并集
c = df[['age','loc']].loc['ldq']  # 先筛选行，得到一个 Dataframe ，再从这个 DataFrame 中选出需要的列

print(a)
print(type(a))
print('-'*100)
print(b)
print(type(b))
print('-'*100)
print(c)
print(type(c))


