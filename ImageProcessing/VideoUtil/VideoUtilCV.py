# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import cv2
import os
import matplotlib.pyplot as plt


class VideoUtilCV(object):

    def __init__(self, vedio_path):
        self.__vc = cv2.VideoCapture(vedio_path)

    def get_frame_img_in_assign_time(self, save_dir, hours=0, minutes=0, seconds=0, assign_frame_num=10, frame_rate=24):
        """获取指定时间范围内的指定帧，可以指定获取的帧的数目"""
        frame_start_num = (hours * 3600 + minutes * 60 + seconds) * frame_rate - int(assign_frame_num/2)
        frame_start_num = 0 if frame_start_num < 0 else frame_start_num
        self.__vc.set(cv2.CAP_PROP_POS_FRAMES, frame_start_num)  # 指定帧

        index = 0
        while True:
            read_res = self.__vc.read()  # 读取一帧影像
            cv2.imwrite(os.path.join(save_dir, '{0}.jpg'.format(index)), read_res[1])  # 将数据写到本地
            index += 1
            if index >= assign_frame_num:
                break


if __name__ == '__main__':

    a = VideoUtilCV(r'D:\000_缓存\Thunder\辛普森一家.The.Simpsons.S30E20.中英字幕.WEBrip.720P-人人影视.mp4')
    save_folder = r'C:\Users\Administrator\Desktop\del\deldel'
    a.get_frame_img_in_assign_time(save_folder, minutes=6, seconds=12, assign_frame_num=10)





