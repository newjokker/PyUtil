# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""高斯朴素贝叶斯，假设每个特征中属于每一类的特征值都符合高斯分布，此方法适合作为初步分类手段"""


from sklearn.datasets import load_iris
from sklearn.naive_bayes import GaussianNB
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# 获取数据
iris = load_iris()
X = iris.data[:,(2,3)]  # length width
Y = iris.target.astype(np.int) # iris setosa
x_train, x_test, y_train, y_test = train_test_split(X, Y, random_state=1)  # 分割测试集和验证集

# 训练预测
model = GaussianNB()  # 不需要设置超参数
model.fit(x_train, y_train)  # 拟合数据
y_model = model.predict(x_test)  # 对新数据进行预测

print(accuracy_score(y_test, y_model))


