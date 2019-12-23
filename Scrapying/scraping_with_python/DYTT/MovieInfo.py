# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import time

def parse_p_info(p_info_str):
    """解析 p 标签的信息"""
    all_info = []
    need_tag = {'译名','片名','年代','产地','类别','语言','字幕','上映','豆瓣','IM','文件','视频','文件','片长',
                '导演','主演','简介','获奖', }
    aa = ''.join(p_info_str).replace('　　', '')
    for each_tag in aa.split('◎'):
        tag_temp = each_tag[:2]
        if tag_temp in need_tag:
            all_info.append(each_tag)
    return all_info

def get_all_url():
    html = urlopen(r'https://www.dy2018.com/', timeout=20)
    bs_obj = BeautifulSoup(html, "html.parser")
    # -----------------------------------------------------------------------------------------------
    all_url = dict()
    # 传入正则表达式
    for each in bs_obj.find_all(lambda x: 'title' in x.attrs and 'href' in x.attrs):
        href = each.attrs['href']
        title = each.attrs['title']
        if href not in all_url:
            # all_url[title] = r'https://www.dy2018.com' + href
            all_url[r'https://www.dy2018.com' + href] = title
    return all_url


# --------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    film_url_dict = dict()

    with open(r'E:\Algorithm\Scraping\scraping_with_python\all_film.txt', 'r', encoding='utf-8') as txt_file:
        for each_line in txt_file:
            split_info = each_line.split(',')
            if len(split_info) > 1:
                film_url_dict[split_info[0]] = split_info[1].strip()

    # film_url_dict = get_all_url()
    for each_url in film_url_dict:
        try:
            html = urlopen(each_url, timeout=20)
            bs_obj = BeautifulSoup(html, "html.parser")
            zoom = bs_obj.find('div', {'id':'Zoom'})
            # -----------------------------------------------------------------------------
            # 下载地址，有好几种地址
            hrefs = []
            if not zoom:
                continue

            for each in zoom.find_all('a'):
                hrefs.append(each['href'])
                # print('href : ', each['href'])
                # print('-'*100)
            # -----------------------------------------------------------------------------
            # 电影图片，第一个是海报，其他的是电影截图
            srcs = set()
            for each in zoom.find_all('img'):
                if each:
                    if 'src' in each.attrs:
                        if each['src'] not in srcs:
                            srcs.add(each['src'] )
                            # print('src : ', each['src'])
                            # print('-'*100)
            srcs = list(srcs)
            # -----------------------------------------------------------------------------
            # 电影信息
            p_infos = []
            for each in zoom.find_all('p'):
                if each:
                    if not each.attrs:
                        # print(each.text)
                        p_infos.append(each.text)
            # -----------------------------------------------------------------------------
            print(each_url)
            try:
                film_name = film_url_dict[each_url]
                film_info = parse_p_info(p_infos)
                if film_info:
                    with open(r'result/{0}.txt'.format(film_name), 'w', encoding='utf-8') as txt_file:
                        txt_file.write(each_url + '\n')
                        txt_file.write('-' * 100 + '\n')
                        for each_info in film_info:
                            txt_file.write(each_info + '\n')
                            txt_file.write('-'*100 + '\n')
            except:
                print('error : {0}'.format(each_url))
            print('-'*100)
        except:
            time.sleep(1)


