# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""DFS，递归"""

import copy


def get_list_element(check_list, result=None):
    """获得列表中的所有子元素"""
    if result is None:
        result = []

    for each in check_list:
        if isinstance(each, list):
            get_list_element(each, result)
        else:
            result.append(each)

"""BFS"""

def print_list_2(a):
    to_add = a

    while to_add:
        wait_loop = copy.deepcopy(to_add)
        to_add = []
        for each in wait_loop:
            if isinstance(each, int):
                print(each)
            else:
                if len(each) == 1 and isinstance(each, list):
                    to_add.append(each[0])
                else:
                    for i in each:
                        if isinstance(i, int):
                            print(i)
                        else:
                            if len(each) == 1 and isinstance(each, list):
                                to_add.append(i[0])
                            else:
                                to_add.append(i)


if __name__ == '__main__':

    a = [[[[[1]], [2]], [3, 4, [5]]]]

    b = []
    get_list_element(a, b)

    print(b)


    # for each in print_list(a):
    #     print(each)

    # print('-'*100)
    #
    # print_list_2(a)
