# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from Report.ImageUtil import ImageUtil

img_path = r'C:\Users\Administrator\Desktop\456.jpg'

# a = ImageUtil(img_path)
a = ImageUtil()

# 新建模板
# a.create_img_mat(3000, 1000, ImageUtil.get_rand_color())
a.create_img_mat(3000, 1000, (0,0,0))
a.save_to_image(r'C:\Users\Administrator\Desktop\JiangSu2.png')
exit()


# 增加边框
a.add_border_line(line_weight=10, line_color=(0, 0, 0), line_inside=False)

# 扩展边界
a.extend_to_range((0, 0, 30, 0), ImageUtil.get_rand_color())

# 根据比例扩展范围
a.extend_by_ratio([0.05] * 4, ImageUtil.get_rand_color())

# 指定大小
a.convert_to_assign_shape((100, 100))

# 新建形状
rect = ImageUtil.create_shape_rect(30, 30, ImageUtil.get_rand_color())

# 画图像到幕布上
a.draw(rect, (20, 20))

# 连接图像
rect = ImageUtil.create_shape_rect(100, 30, (0,0,0))
a.cat(rect, direction=0)

# 去掉边框
# a.cut_border((0,0,0))

c = ImageUtil(img_path)
c.convert_to_assign_shape((300, 250))  # 转变形状
c.draw(a, (0, 0))

# 测试新建文字
word = ImageUtil.create_word_img(u"你说呢", (0, 0, 0))
mask = word.get_assign_color_mask((255,255,255))
word.set_assign_layer_value_by_mask(3, mask, 0)
word.save_to_image(r'C:\Users\Administrator\Desktop\word.png')

# 显示图片
c.show_img()

# 保存为文件
c.save_to_image(r'C:\Users\Administrator\Desktop\445465.jpg')
