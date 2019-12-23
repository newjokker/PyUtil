# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""读写 PDF 文件信息"""

# import PDFMiner
import pdfkit


# url页面转化为pdf
# url = r'https://blog.csdn.net/qq_41185868/article/details/79907936#pdfkit%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95'
file_path = r'C:\Users\Administrator\Desktop\SnowDepth.pdf'
# pdfkit.from_url(url, file_path)

# 文本内容转化为pdf
pdfkit.from_string(u"jokker，呵呵，你说呢", file_path)

# # 文件转化为pdf
# pdfkit.from_file(file, file_path)
#
# # 也可以是打开的文件
# with open('file.html') as f:
#     pdfkit.from_file(f, 'out.pdf')
#
# print('OK')






















