# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from Report.ImageUtil import ImageUtil

narrow = 30
broad = 150

a = ImageUtil(r'C:\Users\Administrator\Desktop\del\test.jpg')

a.add_border_line(1)  # 加上黑线
# a.extend_to_range((narrow, narrow, broad, narrow), (255, 255, 255))

word = ImageUtil.create_word_img(u"少数的资产阶级自由平等", (0, 0, 0), word_size=100, background_color=(255, 255, 255))
word.extend_by_ratio((0, 0, 0.5, 0.5))

word.cat(a, 3)

a.extend_to_range((narrow, narrow, narrow, narrow), (255, 255, 255))

a.add_border_line(1)  # 加上黑线

a.save_to_image(r'C:\Users\Administrator\Desktop\123.png')
word.save_to_image(r'C:\Users\Administrator\Desktop\word.png')
