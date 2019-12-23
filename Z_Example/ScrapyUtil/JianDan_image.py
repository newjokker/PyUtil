# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
实现煎蛋图片自己爬取的爬虫
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import os
from ReadData.PickleUtil import PickleUtil


def get_page_num(jiandan_url):
    """得到当前页面是多少页"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3676.400 QQBrowser/10.4.3469.400',
        }

    html = requests.get(jiandan_url, timeout=20, headers=headers)
    bs_obj = BeautifulSoup(html.text, 'html.parser')
    return bs_obj.find('span',{'class': 'current-comment-page'}).text.strip('[] ')

def JianDan_image(info_dict=None):
    """煎蛋图片爬虫, 爬取图片的前三页"""

    save_dir = info_dict['out_dir']
    plugin_name = info_dict['plugin_name']
    auxdata_dir = info_dict['auxdata_dir']
    if not os.path.exists(save_dir): os.makedirs(save_dir)
    if not os.path.exists(auxdata_dir): os.makedirs(auxdata_dir)
    # ------------------------------------------------------------------------------------------------------------------
    load_history_path = os.path.join(auxdata_dir, '{0}_load_history.pkl'.format(plugin_name))
    if os.path.exists(load_history_path):
        load_history = PickleUtil.load_data_from_pickle_file(load_history_path)
    else:
        load_history = set()
    # ------------------------------------------------------------------------------------------------------------------
    # 查看最新的界面
    check_head_url = r'http://jandan.net/pic/'
    page_num_now = get_page_num(check_head_url)
    # ------------------------------------------------------------------------------------------------------------------
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3676.400 QQBrowser/10.4.3469.400',
        }
    # 爬取前三页
    for i in range(8):
        page_temp = str(int(page_num_now) - i)
        print('start page {0} : {1}'.format(i, page_temp))
        check_url = r'http://jandan.net/pic/page-{0}#comments'.format(page_temp)
        html = requests.get(check_url, timeout=20, headers=headers)
        bs_obj = BeautifulSoup(html.text, 'html.parser')
        # 遍历找到的图片
        for index, each_tag in enumerate(bs_obj.find_all('a')):
            # 去掉无下载连接的标签
            if 'href' not in each_tag.attrs:
                continue

            # 去掉不是保存在新让网上的标签
            if 'sinaimg.cn' in each_tag['href']:
                href = each_tag['href']
                # 过滤已经下载的文件
                if href in load_history:
                    pass
                    # print('file have been download : {0} '.format(href))
                else:
                    load_history.add(href) # 添加到历史文件中
                    # 打印当前下载的信息内容
                    print('download : {0} '.format(href))
                    # 打开文件
                    pic_data = urlopen(r'http:' + href)
                    # 保存文件
                    with open(os.path.join(save_dir, os.path.split(href)[1]), 'wb') as pic_file:
                        pic_file.write(pic_data.read())
            # time.sleep(1)
    # ------------------------------------------------------------------------------------------------------------------
    PickleUtil.save_data_to_pickle_file(load_history, load_history_path)
    # ------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':

    info_dict = {'out_dir': r'C:\Users\Administrator\Desktop\JD',
                 'plugin_name': 'JD',
                 'auxdata_dir': r'C:\Users\Administrator\Desktop\JD'}

    JianDan_image(info_dict)
















