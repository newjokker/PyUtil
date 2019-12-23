# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import os

html = urlopen(r'https://www.dy2018.com/')

bs_obj = BeautifulSoup(html, "html.parser")
# -----------------------------------------------------------------------------------------------
all_url = dict()
# 传入正则表达式
for each in bs_obj.find_all(lambda x:'title' in x.attrs and 'href' in x.attrs):
    href = each.attrs['href']
    title = each.attrs['title']
    if href not in all_url:
        all_url[title] = r'https://www.dy2018.com' + href
# -----------------------------------------------------------------------------------------------
for each in all_url:
    print(each)
    print(all_url[each])
    print('-'*100)
# -----------------------------------------------------------------------------------------------
print(len(all_url))

