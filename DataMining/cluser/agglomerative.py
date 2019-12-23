# -*- coding: utf-8  -*-
# -*- author: jokker -*-

# Python 机器学习基础教程 P_140


# 凝聚聚类
from sklearn.datasets import make_blobs
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt


X, y = make_blobs(random_state=1)
agg = AgglomerativeClustering(n_clusters=3)
aggignment = agg.fit_predict(X)


print(aggignment)


