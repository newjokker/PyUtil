# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import pandas as pd
import numpy as np


# 列表创建
a = pd.Series([0.25, 0.5, 0.75, 1], index=['a', 'b', 'c', 'd'], dtype='object')

# 字典创建
# b = pd.Series({'ldq':27, 'sm':25, 'ldy':28, 'ldx':31})
b = pd.Series({'ldq':27, 'sm':25, 'ldy':28, 'ldx':31}, index=['ldq', 'ldy', 'ldx', 'sm'])  # 可以指定字典的顺序

# 从 numpy 数组创建
c = pd.Series(np.random.random(5), index=['a', 'b', 'c', 'd', 'e'])



print(a)
print(b)
print(c)
