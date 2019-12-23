# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
sobel   算子：
roberts 算子：
prewitt 算子：
laplace 算子：使用中心为5的8邻域拉普拉斯算子与图像卷积可以达到锐化增强图像的目的。
canny   算子：
"""

from skimage import data, io, filters

# image = data.coins()
image = data.astronaut()


edges = filters.sobel(image[:,:,0])
# edges = filters.sobel_h(image[:,:,0])
# edges = filters.sobel_v(image[:,:,0])

io.imshow(edges)
io.show()
io.imshow(image)
io.show()

