# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import os
import jieba
import jieba.analyse

# seg_list = jieba.cut('我是来自地球的人类', cut_all=False)  # 返回的是一个可遍历的结构
seg_list = jieba.lcut('我是来自地球的人类', cut_all=False)  # 返回一个 list

b = jieba.analyse.extract_tags('我是来自地球的人类', topK=20, withWeight=False, allowPOS=())  # 分析关键词

# ----------------------------------------------------------------------------------------------------------------------

txt_dir = r'D:\BandIZip\data\txt_data'

all_txt_path = []

for i,j,k in os.walk(txt_dir):
    for each_file in k:

        if not each_file.endswith('.txt'):
            continue

        abs_path = os.path.join(i, each_file)

        all_txt_path.append(abs_path)


for each_file_path in all_txt_path:

    try:

        with open(each_file_path, 'r') as txt_file:
            txt_str = txt_file.readlines()

        txt_str = ''.join(txt_str)

        # seg_list = jieba.cut(txt_str, cut_all=False)  # 返回的是一个可遍历的结构
        seg_list = jieba.lcut(txt_str, cut_all=False)  # 返回一个 list

        b = jieba.analyse.extract_tags(txt_str, topK=20, withWeight=False, allowPOS=())

        print(b)

        # for each in b:
        #     print(each, seg_list.count(each))
        #
        # print('ok')
    except:
        print('error : {0}'.format(each_file_path))


