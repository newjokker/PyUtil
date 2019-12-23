# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import pandas as pd
import numpy as np


# 从列表创建
a = pd.DataFrame([[1,2,3,4], [5,6,7,8], [9,10,11,12]], index=['a', 'b', 'c'], columns=['A', 'B', 'C', 'D'])

# 从 numpy 创建
b = pd.DataFrame(np.zeros((10, 5)))

# 从字典创建  # FIXME 缺失值会被当做为 None
data_dict = {'age':{'ldq':31, 'ldx':31, 'ldy':28}, 'loc':{'ldq':'nj', 'ldx':'wx', 'ldy':'wx'}, 'phone':{'ldq':'18761609908'}}
c = pd.DataFrame(data_dict)

print(a)
print(b)
print(c)



