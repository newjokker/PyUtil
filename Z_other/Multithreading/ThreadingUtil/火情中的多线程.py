# -*- coding: utf-8  -*-
# -*- author: jokker -*-

# multiprocessing 文档 ： https://docs.python.org/zh-cn/3/library/multiprocessing.html

import multiprocessing


"""

* 火情中使用的是 multiprocessing 模块进行解决的，是多进程的方法

    multiprocessing.freeze_support()
    
    # 使用多线程,且将线程固定为2个
    p = multiprocessing.Pool(thread_count)
    map(lambda x: pre_data_dict.update(x), p.map(single_band_process, arg_list))
    p.close()  # 关闭进程池，不再接受新的进程
    p.join()  # 主进程阻塞等待子进程的退出

"""
