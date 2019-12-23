# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from sklearn.preprocessing import Imputer
import numpy as np

"""简单的方法可以使用 均值，中位数，众数 进行替换"""


x = np.array([[np.nan, 1, 2, 3], [4, 5, 6, np.nan], [4,5,6,12]])

imp = Imputer(strategy='mean')  # 使用列的均值，填充无效值
x2 = imp.fit_transform(x)

print(x2)

