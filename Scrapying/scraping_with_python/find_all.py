# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen(r'https://www.dy2018.com/')

bs_obj = BeautifulSoup(html, "html.parser")
# -----------------------------------------------------------------------------------------------
# 传入正则表达式
for each in bs_obj.find_all("a",  {"href":re.compile(r'/i/\w{3,10}.html')}):
    print(each.attrs['href'])
    print(each.attrs['title'])
    print('-'*100)
# -----------------------------------------------------------------------------------------------
# 传入函数，接受标签，返回 bool 值
for each in bs_obj.find_all(lambda x: len(x.attrs)==2 and 'title' in x.attrs ):
    print(each)
    print('-'*100)
# -----------------------------------------------------------------------------------------------

