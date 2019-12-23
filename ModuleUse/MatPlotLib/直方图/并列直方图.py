# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import numpy as np
import matplotlib.pyplot as plt


def bar(data_list, bar_width, dui_width, xticks_name_list, save_path, col_name, color_list):
    """画需要的直方图"""

    # 中文显示的问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    bar_num = len(data_list[0])  # 一个堆中元素的个数
    dui_num = len(data_list)  # 堆的个数
    x = np.arange(dui_num)*(bar_width * bar_num + dui_width)  # 每一堆第一个元素的横坐标
    xticks_list = x + (bar_num / 2) * bar_width - (bar_width / 2)   # x 轴标签的横坐标

    # 对于每一种类型画一次直方图
    for i in range(bar_num):
        data_temp = list(map(lambda x: x[i], data_list))  # fixme 考虑一下列表套列表的格式是怎么组织的，每一个是一类在所有堆的元素，还是一个堆的所有元素比较好
        plt.bar(x + bar_width*i, data_temp, bar_width, fc=color_list[i])

    plt.xticks(xticks_list, xticks_name_list, rotation=30)  # fixme 支持旋转
    plt.legend(col_name)
    plt.title(u'并列直方图')
    plt.ylim(0, 100)
    plt.savefig(save_path, dpi=300)
    plt.show()



if __name__ == "__main__":

    save_path = r'C:\Users\74722\Desktop\ok.png'
    dataList = [[52, 55, 63, 53], [44, 66, 55, 41], [34, 56, 35, 54], [44, 65, 55, 41],  [44, 65, 55, 41], [52, 55, 63, 53], [44, 66, 55, 41], [34, 56, 35, 54], [44, 65, 55, 41],  [44, 65, 55, 41]]
    color_list = ['lightskyblue', 'orange', 'grey', 'lightskyblue']
    bar(dataList, 1, 3, ('001', '002', '003', '004', '005'), save_path, ['A', 'B', 'C', 'D'], color_list)


