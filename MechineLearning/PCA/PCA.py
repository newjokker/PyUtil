# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""无监督学习，降维，PCA 主成分分析，principal component analysis"""

from sklearn.decomposition import PCA
from sklearn.datasets import load_iris
import numpy as np

iris = load_iris()
X = iris.data[:,(2,3)]  # length width
Y = iris.target.astype(np.int) # iris setosa

model = PCA(n_components=2)  # 设置超参数，初始化模型
model.fit(X)  # 拟合数据
X_2D = model.transform(X)  # 將数据转为二维

