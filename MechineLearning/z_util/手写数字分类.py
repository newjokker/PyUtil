# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB   # 高斯朴素贝叶斯
from sklearn.ensemble import RandomForestClassifier  # 随机森林
from sklearn.linear_model import Perceptron
from sklearn.datasets import load_digits
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn

# 载入数据集
digits = load_digits()
X = digits.data  # length width
Y = digits.target.astype(np.int) # iris setosa

# 分割测试集和验证集
x_train, x_test, y_train, y_test = train_test_split(X, Y, random_state=0)

# 训练, TODO 使用线性模型的准确率竟然比高斯朴素贝叶斯的准确率还要高,这是什么鬼?那个线性权静月说是用的神经网络做的
model = GaussianNB()
# model = Perceptron()
# model = RandomForestClassifier()
model.fit(x_train, y_train)


# 精度验证
y_model = model.predict(x_test)
print(accuracy_score(y_test, y_model))

# 计算混淆矩阵
mat = confusion_matrix(y_test, y_model)
seaborn.heatmap(mat, square=True, annot=True, cbar=True)
plt.xlabel('predicted value')
plt.ylabel('true value')
plt.show()

print('ok')



