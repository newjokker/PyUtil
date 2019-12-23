# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from Report.ImageUtil import ImageUtil

# fixme 中文生成比较快，但是英文生成非常慢，不知道原因
# fixme 图像不要重采样，会极大的影响品质

# 测试新建文字
word = ImageUtil.create_word_img(u"少数的资产阶级自由平等", (0, 0, 0), word_size=200)
word.save_to_image(r'C:\Users\Administrator\Desktop\word.png')
