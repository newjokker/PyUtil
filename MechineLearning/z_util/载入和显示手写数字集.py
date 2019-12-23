# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""载入和显示手写数字集"""

import matplotlib.pyplot as plt
from sklearn.datasets import load_digits

digits = load_digits()  # 载入数据集

fig, axes = plt.subplots(10, 10, figsize=(18, 18), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))  # 定义坐标轴

# 每一个数字图像放在坐标轴里面
for i, ax, in enumerate(axes.flat):
    ax.imshow(digits.images[i], cmap='binary', interpolation='nearest')
    ax.text(0.05, 0.05, str(digits.target[i]), transform=ax.transAxes, color='green')

plt.show()