# -*- coding: utf-8  -*-
# -*- author: jokker -*-

# 参考网址 https://www.cnblogs.com/CJOKER/p/8295272.html

import logging
import logging.config

def main():

    # ------------------------------------------------------------------------------
    # 设置保存的文件和日志的级别
    # logging.basicConfig(filename='app.log', level=logging.NOTSET, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

    # FIXME  这个函数是一次性的，要保证在使用这个函数之前没有任何的 logging.info() 操作，否则会失效
    logging.basicConfig(filename=r'C:\Users\Administrator\Desktop\New_frm_wprd\app.log', level=logging.NOTSET, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    # ------------------------------------------------------------------------------
    # 不保存到文件，直接在屏幕上输出
    # logging.basicConfig(level=logging.NOTSET, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    # ------------------------------------------------------------------------------
    # 日志的五个级别
    logging.debug(u"苍井空")
    logging.info(u"麻生希")
    logging.warning(u"小泽玛利亚")
    logging.error(u"桃谷绘里香")
    logging.critical(u"泷泽萝拉")

def ok():
    logging.info('你调用 ok 啦')

class LogUtil(object):

    @staticmethod
    def log_init(file_path=None, level=None):
        """使用常用的日志格式"""
        logging.basicConfig(filename=file_path, level=level,
                            format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


if __name__ == '__main__':

    main()
    ok()

"""
1. 这个真的是很好的解决了日志记录比较困难的问题，这样的话，没必要一次次传入文件了
2. 只需要在开始的时候告诉 logging 日志保存在哪里，然后不断 logging 就行了。
3. 如果不指定保存的目录只是直接调用 logging 的话，就会打印在屏幕上，天赐神器
"""

