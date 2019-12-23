# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB   # 高斯朴素贝叶斯
from sklearn.datasets import load_digits
import numpy as np
from sklearn.metrics import accuracy_score

# 载入数据集
digits = load_digits()
X = digits.data  # length width
Y = digits.target.astype(np.int) # iris setosa

# 分割测试集和验证集
x_train, x_test, y_train, y_test = train_test_split(X, Y, random_state=0)

# 训练
model = GaussianNB()
model.fit(x_train, y_train)

# ----------------------------------------------------------------
# 精度验证
y_model = model.predict(x_test)
print(accuracy_score(y_test, y_model))
# ----------------------------------------------------------------
