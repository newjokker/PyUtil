# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import datetime
import urllib
from bs4 import BeautifulSoup
from urllib.request import urlopen


def get_need_page_url_from_region_url(url):
    """获得当天的路径"""
    html = urllib.request.urlopen(url)
    bs_obj = BeautifulSoup(html, "html.parser")
    main_content = bs_obj.find('ul', {'class': 'lmcontent_r2_b clear_fix'})
    today_date = main_content.find('a')
    return r'http://www.slfh.gov.cn' + today_date.attrs['href']

def get_word_from_url(url):
    """从 url 得到文字段落"""
    need_word = []
    html = urlopen(url)
    bs_obj = BeautifulSoup(html, "html.parser")
    main_content = bs_obj.find('div', {'class': 'mainContent'})
    for each in main_content.find_all('p'):
        word_text = each.text.strip()
        if word_text:
            need_word.append(word_text)
    return need_word

def load_and_save_pic(url, save_path):
    """下载和保存图片"""
    html = urlopen(url)
    bs_obj = BeautifulSoup(html, "html.parser")
    main_content = bs_obj.find('div', {'class': 'mainContent'})
    pic_url = r'http://www.slfh.gov.cn/' + main_content.find('p', {'style':'text-align: center'}).find('input')['src']
    page = urllib.request.urlopen(pic_url)
    html = page.read()
    with open(save_path, 'wb') as file:
        file.write(html)
    print('* pic have been loaded')


# FIXME 写成 xml
# 页面 url
html = r'http://www.slfh.gov.cn/Category_121/Index.aspx'
page_url = get_need_page_url_from_region_url(html)
# 图片
date_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
load_and_save_pic(page_url, '{0}.gif'.format(date_str))
# 文字
need_word = get_word_from_url(page_url)
print(need_word)
