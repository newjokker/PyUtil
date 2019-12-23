# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import pathlib

# 参考 ： https://zhuanlan.zhihu.com/p/87940289?utm_source=wechat_session&utm_medium=social&utm_oi=49891858448384


print(pathlib.Path(r'C:\Users\Administrator\Desktop\for6.png').cwd())  # py 文件所在目录
print(pathlib.Path(r'C:\Users\Administrator\Desktop\for6.png').parents[0])  # 第 * 级父目录
print(pathlib.Path(r'C:\Users\Administrator\Desktop\for6.png').name)   # 文件名
print(pathlib.Path(r'C:\Users\Administrator\Desktop\for6.png').suffix)  # 后缀
print(pathlib.Path(r'C:\Users\Administrator\Desktop\for6.png').stem)  # 去掉后缀的文件名

with pathlib.Path(r'C:\Users\Administrator\Desktop\123.txt').open() as txt_file:
    for each in txt_file:
        print(each.strip())
