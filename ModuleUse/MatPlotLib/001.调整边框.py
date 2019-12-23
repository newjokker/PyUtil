# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import matplotlib.pylab as plt
import numpy as np


fig = plt.figure()
ax = plt.axes()

x = np.linspace(0, 10, 1000)
ax.plot(x, np.sin(x))

# 坐标的上下限
# （1）
# plt.xlim(0, 10)
# plt.ylim(-1.1, 1.1)
# （2）
# plt.axis([0, 10, -2, 2])

# 收紧坐标轴，等宽
plt.axis('tight')
plt.axis('equal')
#
plt.show()
