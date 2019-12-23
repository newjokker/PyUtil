# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
爬取 Bose 直聘信息，得到想要的岗位的区域分布图
"""

from urllib import urlopen
from bs4 import BeautifulSoup
import re

def get_all_url(url):
    html = urlopen(url)
    bs_obj = BeautifulSoup(html, "html.parser")
    # -----------------------------------------------------------------------------------------------
    # 传入正则表达式

    print(bs_obj)

    for each in bs_obj.find_all(lambda x: 'job_title' in x.attrs):
        print(each)


if __name__ == '__main__':

    url = r'https://www.zhipin.com/job_detail/?query={0}city={1}&industry=&position='.format('python', '101010100')

    url = r'https://www.zhipin.com/job_detail/?query=%E8%AE%A1%E7%AE%97%E6%9C%BA&city=101010100&industry=&position='

    get_all_url(url)







