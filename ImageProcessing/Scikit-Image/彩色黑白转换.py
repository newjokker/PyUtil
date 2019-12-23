# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from skimage import data, color, io

# img = color.rgb2gray(data.chelsea())  # rgb 转为 黑白
img = color.gray2rgb(data.coins())    # 黑白转 rgb

io.imshow(img)
io.show()