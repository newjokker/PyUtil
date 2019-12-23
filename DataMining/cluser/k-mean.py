# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import matplotlib as mpl

# K-means聚类

# 自己写可以设定阈值的

data = [(1, 1), (1, 1.5), (1, 3), (1, 4), (3, 3), (3, 4), (-1, 0.2)]

kmeans = KMeans(n_clusters=2, random_state=10).fit_predict(data)

print(kmeans)

