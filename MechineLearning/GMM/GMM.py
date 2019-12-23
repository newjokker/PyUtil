# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""高斯混合模型，Gaussian mixure model（GMM），聚类，试图将数据构造成符合高斯分布的概率密度函数簇"""

import numpy as np
from sklearn.datasets import load_iris
from sklearn.mixture import GaussianMixture

iris = load_iris()
X = iris.data[:,(2,3)]  # length width
Y = iris.target.astype(np.int) # iris setosa

model = GaussianMixture(n_components=3, covariance_type='full')
model.fit(X)
y_gmm = model.predict(X)

print('ok')










