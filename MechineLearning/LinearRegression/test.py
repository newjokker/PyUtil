# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from sklearn.linear_model import LinearRegression  # 简单线性回归，可以直线拟合，还可以处理多维度的线性回归模型
import numpy as np
import matplotlib.pyplot as plt


# 制造训练数据
rng = np.random.RandomState(1)
x = 10 * rng.rand(50, 1)
y = 2 * x - 5 + rng.randn(50, 1)

# 实验模型
model = LinearRegression(fit_intercept=True)
model.fit(x, y)

slope = model.coef_[0][0]  # 斜率
intercept = model.intercept_[0]  # 截距
print('slope is : {0}, intercept is : {1}'.format(slope, intercept))

# 画出斜线
xfit = np.linspace(0, 10, 1000)
yfit = model.predict((xfit[:, np.newaxis]))  # 预测


plt.scatter(x, y)
plt.plot(xfit, yfit)
plt.show()


