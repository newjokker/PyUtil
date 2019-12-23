# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import time
from ReadData.PickleUtil import PickleUtil


class Test(object):

    def __init__(self):
        self.a = None
        self.b = None
        self.num = None

    def task_001(self, a):
        print('task_001 .... waiting for 5 s')
        time.sleep(5)
        self.a = a

    def task_002(self, b):
        print('task_002 .... waiting for 5 s')
        time.sleep(5)
        self.b = b

    def task_003(self, status=1):

        # fixme bug 1
        if status:
            raise ValueError('error')

        if self.a is None or self.b is None:
            raise ValueError('attr a and b can not be None')

        # fixme bug 2
        if status:
            raise ValueError('error')

        time.sleep(2)

        print(self.a + self.b)


if __name__ == "__main__":

    a = Test()
    a.task_001(12)
    a.task_002(13)
    a.task_003()

    save_path = r'E:\Algorithm\Util_Util\Z_for_code_zc\002\data\object_a.pkl'
    PickleUtil.save_data_to_pickle_file(a, save_path)


    # a = PickleUtil.load_data_from_pickle_file(save_path)
    # a.task_003()








