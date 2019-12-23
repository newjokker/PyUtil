# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import time


def get_film_info_urls_from_url(url):
    """重输入的 url 找到电影详情 url"""
    url_dict = dict()
    try:
        html = urlopen(url)
        bs_obj = BeautifulSoup(html, "html.parser")
        for each in bs_obj.find('div', {'class': 'co_content8'}).find_all('table'):
            url_info = each.find('a', {'href':re.compile(r'/./\d{2,10}.html')})
            if 'href' in url_info.attrs and 'title' in url_info.attrs:
                url_temp = r'https://www.dy2018.com' + url_info['href']
                url_dict[url_temp] = url_info['title']
    except:
        print('error')
    return url_dict


# 所有电影的信息
all_film_dict = dict()

for type_num in range(1, 20):
    print('当前抓取第 {0} 个类型'.format(type_num))
    # 找到当前类型第一页
    url_origin = r'https://www.dy2018.com/{0}/'.format(type_num)
    html = urlopen(url_origin)
    bs_obj = BeautifulSoup(html, "html.parser")
    # 找到一共有多少页面
    page_num_str = bs_obj.find('div', {'class': 'co_content8'}).find('div', {'class': 'x'}).find('p').text
    page_num = int(re.compile(r'(\d{1,4})\/(\d{1,4})').search(page_num_str).group(2))
    # 解析第一页
    all_film_dict.update(get_film_info_urls_from_url(url_origin))
    # 遍历后面每个页面
    for page_i in range(2, page_num+1):
    # for page_i in range(2, 15):
        print('当前解析第 {0} 个页面'.format(page_i))
        url_temp = r'https://www.dy2018.com/{0}/index_{1}.html'.format(type_num, page_i)

        film_url_dict_temp = get_film_info_urls_from_url(url_temp)

        if film_url_dict_temp:
            all_film_dict.update(film_url_dict_temp)
        else:
            with open(r'film_page_error.txt', 'a', encoding='utf-8') as txt_file:
                txt_file.write(url_temp)
                txt_file.write('\n')

        with open(r'all_film.txt', 'a', encoding='utf-8') as txt_file:
            for each in all_film_dict:
                txt_file.write(each)
                txt_file.write(',')
                txt_file.write(all_film_dict[each])
                txt_file.write('\n')
                txt_file.write('-'*100)
                txt_file.write('\n')
            all_film_dict = dict()
        print('-'*100)
    time.sleep(3)

# -----------------------------------------------------------------------------------------------
print(len(all_film_dict))
