# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""将数据从 [1797, 64] 降维到 [1797, 2]"""

# 参考，Python数据科学手册 5.10 节

from sklearn.manifold import Isomap
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits

# 载入数据集
digits = load_digits()

# 降维
iso = Isomap(n_components=2)
iso.fit(digits.data)
data_projected = iso.transform(digits.data)  # 训练数据和降维数据相一致

# 可视化
plt.scatter(data_projected[:, 0], data_projected[:, 1], c=digits.target, edgecolors='none', alpha=0.5, cmap=plt.cm.get_cmap('Spectral', 10))
plt.colorbar(label='digit label', ticks=range(10))
plt.clim(-0.5, 9.5)
plt.show()
