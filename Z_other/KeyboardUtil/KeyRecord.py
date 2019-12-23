# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
记录在不同的应用程序中输入键盘的各个键的使用频次，在使用插值方法做出一个热力图来可视化，将每个键的点用一个坐标来表示，每个坐标的值就是按下去的次数

(1) 用一个字典存储在每一个界面下面输入的文字
(2) 每有一个新的界面，那么就新建这么一个字典
"""

import pythoncom
import pyHook
import os
import re
import time


class KeyRecord(object):
    """键盘记录"""

    def __init__(self, txt_dir):

        # 用于记录的 txt 文件的路径
        self.txt_dir = txt_dir
        # 记录的信息
        self.record_info = {}

    def write_record(self, windows_name):
        """写记录, 清空已经写如文件的记录"""
        try:
            with open(os.path.join(self.txt_dir, windows_name + '.txt'), 'a') as txt_file:
                for each in self.record_info[windows_name]:
                    txt_file.write(' : '.join(each) + '\n')
            self.record_info[windows_name] = []
        except:
            print(os.path.join(self.txt_dir, windows_name + '.txt') + ' error ')
            self.record_info[windows_name] = []

    def onKeyboardEvent(self, event):
        """监听键盘事件"""

        # 对 None 不做处理
        if event.WindowName is None:
            return

        windowName = event.WindowName.decode('GBK')

        try:
            windowNames = re.split('[-_]', windowName)
            if len(windowNames) == 1:
                windowName = windowName.split(r'\\')[-1].strip()
            else:
                windowName = windowNames[-1].strip()
        except:
            print(windowName)

        if windowName in self.record_info:
            self.record_info[windowName].append((str(time.time()), str(event.Key)))
        else:
            self.record_info[windowName] = [(str(time.time()), str(event.Key))]

        # 记录
        if len(self.record_info[windowName]) > 10:
            self.write_record(windowName)

        # 同鼠标事件监听函数的返回值
        return True

    def do_process(self):

        # 创建一个“钩子”管理对象
        hm = pyHook.HookManager()
        # 监听所有键盘事件
        hm.KeyDown = self.onKeyboardEvent
        # 设置键盘“钩子”
        hm.HookKeyboard()

        # 进入循环，如不手动关闭，程序将一直处于监听状态
        pythoncom.PumpMessages()


if __name__ == '__main__':

    # TODO 增加字符统计的功能，时间的统计和每个软件字符量，各个字符使用频率的统计
    # TODO 增加将统计结果做成热力图的功能
    # TODO 编译成 exe 让他在后台运行并增加开机自动启动的功能，这样就完美了，让别人上传收集到的信息，我在服务器上处理成热力图，再返回给他们就行

    a = KeyRecord(r'C:\Users\74722\Desktop\record')
    a.do_process()



