# -*- coding: utf-8  -*-
# -*- author: jokker -*-


from bs4 import BeautifulSoup
from urllib.request import urlopen
from Assist.chinese_num_to_arabic_num import changeChineseNumToArab
import os
import time
import copy


class NovelParse(object):

    def __init__(self):
        self.save_dir = None
        self.novel_url = None
        self.novel_name = None
        self.chapter_dir = None

    def get_chapter_info_from_url(self, charper_url):
        """获取章节信息"""
        html = urlopen(charper_url).read()
        bs_obj = BeautifulSoup(html, "html.parser")
        book_name = bs_obj.find('h1', {'id': 'BookName'}).text.strip('正文 ')
        content = bs_obj.find('span', {'id': 'Content'}).text.replace('\xa0', '')
        return {'book_name': book_name, 'content': content}

    def get_chapter_urls_and_novel_info(self, url):
        """获取章节 url"""
        chapter_urls = []
        html = urlopen(url).read()
        bs_obj = BeautifulSoup(html, "html.parser")
        # 获取章节 url
        for each_td in bs_obj.find_all('td', {'width': '33%'}):
            for each_a in each_td.find_all('a'):
                href = each_a.attrs['href']
                href_abs = 'http://m.dxsxs.com/' + href
                chapter_urls.append(href_abs)
        # 获取小说信息
        book_name = bs_obj.find('td', {'id': 'BookName'}).text
        author = bs_obj.find('p', {'id': 'Author'}).text
        class_name = bs_obj.find('p', {'id': 'ClassName'}).text
        file_size = bs_obj.find('p', {'id': 'FileSize'}).text
        self.novel_name = book_name
        self.chapter_dir = os.path.join(self.save_dir, self.novel_name, 'chapter')
        return {'chapter_urls': chapter_urls, 'author': author, 'class_name': class_name,
                'file_size': file_size, 'book_name': book_name}

    def save_chapter_info_to_local(self, chapter_info):
        """保存章节信息到本地"""
        save_dir = self.chapter_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        book_name = chapter_info['book_name']
        content = chapter_info['content']
        # 说名中的中文数字转为阿拉伯文数字
        book_name = changeChineseNumToArab(book_name)
        save_path = os.path.join(save_dir, book_name + '.txt')
        if not os.path.exists(save_path):
            with open(save_path, 'w') as txt_file:
                txt_file.write(content)

    def load_novel_from_url(self, assign_loop_time=3):
        """从 url 下载数据"""
        novel_info = self.get_chapter_urls_and_novel_info(self.novel_url)
        chapter_urls = novel_info['chapter_urls']

        # 报错的话就重复去跑，指定重复去跑的次数
        loop_times = 0
        while len(chapter_urls):
            loop_times += 1
            if loop_times > assign_loop_time:
                break
            loop_url = copy.copy(chapter_urls)
            chapter_urls = []
            for each_url in loop_url:
                try:
                    chapter_info = self.get_chapter_info_from_url(each_url)
                    print(chapter_info['book_name'])
                    self.save_chapter_info_to_local(chapter_info)
                    time.sleep(0.1)
                except:
                    chapter_urls.append(each_url)
                    print('error : {0}'.format(each_url))

    @staticmethod
    def read_txt_info(txt_path):
        """读取 txt 信息"""
        with open(txt_path, 'r') as txt_file:
            return txt_file.readlines()

    def merge_chapter(self):
        """将各个章节记性合并，得到合并后的文本"""
        chapter_txts = os.listdir(self.chapter_dir)
        chapter_txts = list(map(lambda x: os.path.join(self.chapter_dir, x), chapter_txts))

        txt_name = os.path.join(self.save_dir, self.novel_name, self.novel_name + '.txt')
        with open(txt_name, 'w') as txt_file:
            for each_txt in chapter_txts:
                for each_line in self.read_txt_info(each_txt):
                    txt_file.write(each_line)


if __name__ == "__main__":

    # todo 如何按照规定的顺序进行合并，提取其中显示章节的数字，对数字进行排序，但是因为有很多种情况，所以还是需要人工参与的
    # todo 如何去掉文中插入的关键字（大学生小说网）

    a = NovelParse()
    a.save_dir = r'C:\Users\Administrator\Desktop\deldeldel'
    # a.novel_url = r'http://m.dxsxs.com/wuxia/881/'
    a.novel_url = r'http://m.dxsxs.com/wuxia/888/'
    a.load_novel_from_url()
    a.merge_chapter()

