# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import re
import os
from Report.StrUtil import StrUtil
from ReadData.ScrapyUtil import ScrapyUtil

""""
（1）找到对应的电影介绍界面
（2）找到介绍页面中的图片地址
（3）下载图片到指定文件夹
"""


url = r'https://www.dy2018.com'
bs = ScrapyUtil.get_bs_obj_from_url(url)

# 传入正则表达式，找到存在 title 和 href 属性的 标签
for each in bs.find_all(lambda x: 'title' in x.attrs and 'href' in x.attrs):  # （3）使用 find_all 正则表达式 找到所有需要的标签值
    href = each.attrs['href']
    title = each.attrs['title']
    text = each.text
    url_page = url + href
    # ------------------------------
    each_bs = ScrapyUtil.get_bs_obj_from_url(url_page)
    for tag_index, each_tag in enumerate(each_bs.find_all('img', {'src': re.compile(r'https://img.*')})):  # 找到对应的
        print(each_tag.attrs['src'])
        clean_title = StrUtil.remove_assign_character(title, ['\\', '/', ' '])
        img_url = each_tag.attrs['src']
        save_path = os.path.join(r'C:\Users\Administrator\Desktop\deldeldelde', clean_title + str(tag_index) + '.jpg')

        if os.path.exists(save_path):
            continue

        ScrapyUtil.load_file_from_url(img_url, save_path)  # 下载

