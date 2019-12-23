# -*- coding: utf-8  -*-
# -*- author: jokker -*-


from skimage import filters
from skimage import data
from skimage import color
import skimage.morphology as sm
import matplotlib.pyplot as plt

# img = data.checkerboard()
img = data.coins()

# dst = sm.dilation(img, sm.square(5))
dst = sm.dilation(img, sm.square(10))

plt.figure('dilation', figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.imshow(img, plt.cm.gray)

plt.subplot(1, 2, 2)
plt.imshow(dst, plt.cm.gray)

plt.show()
