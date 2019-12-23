# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
文件下载模块，用于下载指定的链接对应的文件
"""

import requests


class LoadUtil(object):

    @staticmethod
    def load_file_from_url(url, save_path):
        """从 url 下载数据"""
        f = requests.get(url)
        with open(save_path, "wb") as file_url:
            file_url.write(f.content)


if __name__ == "__main__":

    pass

