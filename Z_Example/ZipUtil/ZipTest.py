# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from Report.ZipUtil import ZipUtil


folder_path = r'C:\Users\Administrator\Desktop\青海服务器账号密码'
save_path = r'C:\Users\Administrator\Desktop\del\del_ningan\deldel.zip'
un_zip_path = r'C:\Users\Administrator\Desktop\del\del_ningan'

# 压缩一个文件夹、
ZipUtil.zip_folder(folder_path, save_path, 'test_folder')
# 解压一个文件年
ZipUtil.unzip_file(save_path, un_zip_path)

