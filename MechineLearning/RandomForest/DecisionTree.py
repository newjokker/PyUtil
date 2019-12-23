# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""决策树"""

from sklearn.datasets import make_blobs
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier  # 分类器
from sklearn.ensemble import RandomForestRegressor  # 回归
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

def visualize_classifier(model, x, y, ax=None, cmap='rainbow'):
    """对分类结果进行可视化"""

    # 画出训练数据
    ax = ax or plt.gca()  # 这个语法如果 ax 为肯定就选择 ax 否则选择 后面那个
    ax.scatter(x[:, 0], x[:, 1], c=y, s=30, cmap=cmap, clim=(y.min(), y.max()), zorder=3)
    ax.axis('tight')
    ax.axis('off')
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    # 用评估器拟合数据
    model.fit(x, y)
    xx, yy = np.meshgrid(np.linspace(*xlim, num=200), np.linspace(*ylim, num=200))
    z = model.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

    # 结果生成彩色图片
    n_classes = len(np.unique(y))
    comtours = ax.contourf(xx, yy, z, alpha=0.3, levels=np.arange(n_classes+1) - 0.5, cmap=cmap, clim=(y.min(), y.max()), zorder=1)
    ax.set(xlim=xlim, ylim=ylim)
    plt.show()


if __name__ == '__main__':

    x, y = make_blobs(n_samples=300, centers=4, random_state=0, cluster_std=1.0)
    tree = DecisionTreeClassifier().fit(x, y)
    visualize_classifier(DecisionTreeClassifier(), x, y)










