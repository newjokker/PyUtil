# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import logging
import time

def set_logging_info(logging_path):
    """设置日志信息"""
    time.sleep(0.05)  # 防止打印的检查信息和输出的 log 串了
    # 两个 Handler 在屏幕和文件中分别进行记录
    logger = logging.getLogger()  # 不加名称设置root logger
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s', )

    # 使用FileHandler输出到文件
    fh = logging.FileHandler(logging_path)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    # 使用StreamHandler输出到屏幕
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    # 添加两个Handler
    logger.addHandler(ch)
    logger.addHandler(fh)
    logging.info(u"-" * 50)
    # logging.info(u"start logging")