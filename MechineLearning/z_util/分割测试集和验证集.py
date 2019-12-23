# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import numpy as np

iris = load_iris()
X = iris.data[:,(2,3)]  # length width
Y = iris.target.astype(np.int) # iris setosa


x_train, x_test, y_train, y_test = train_test_split(X, Y, random_state=1)  # 分割测试集和验证集

print('ok')
