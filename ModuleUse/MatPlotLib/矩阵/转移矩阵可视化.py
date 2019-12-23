# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import matplotlib.pyplot as plt
import numpy as np


def samplemat(dims):
    """Make a matrix with all zeros and increasing elements on the diagonal"""
    aa = np.zeros(dims)
    for i in range(min(dims)):
        aa[i, i] = i
    return aa


# Display matrix
plt.matshow(samplemat((15, 15)))
x_label = tuple(map(lambda x: '00{0}'.format(x), range(10)))
print(x_label)
# fixme ticks 和 labels 需要成对出现
plt.xticks(ticks=list(range(10)), labels=x_label)

plt.show()
